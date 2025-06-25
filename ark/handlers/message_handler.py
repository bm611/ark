"""
Message handling logic for AI interactions.
"""
import time
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from ark.models import ChatMessage
from ark.providers.manager import provider_manager


class MessageHandler:
    """Handles message processing and AI interactions."""
    
    def __init__(self):
        self.provider_manager = provider_manager
    
    def process_message(
        self,
        messages: List[Dict[str, str]],
        provider: str = "openrouter",
        model: Optional[str] = None,
        action: str = ""
    ) -> ChatMessage:
        """
        Process a message and return the response with metadata.
        
        Returns:
            ChatMessage dictionary
        """
        start_time = time.time()
        
        # Make the API call
        response = self.provider_manager.chat_completion(
            messages=messages,
            provider_name=provider,
            model=model
        )
        
        # Calculate timing metrics
        end_time = time.time()
        generation_time_seconds = round(end_time - start_time, 2)
        generation_time = f"{generation_time_seconds}s"
        
        # Extract token usage
        current_response_tokens = self._extract_tokens(response)
        tokens_per_second = self._calculate_tokens_per_second(
            current_response_tokens, generation_time_seconds
        )
        
        # Process response content
        response_text = response.choices[0].message.content
        thinking_content, actual_response = self._extract_thinking(response_text, response)
        
        
        # Build message dictionary
        message_dict = self._build_message_dict(
            actual_response=actual_response,
            generation_time=generation_time,
            current_response_tokens=current_response_tokens,
            tokens_per_second=tokens_per_second,
            thinking_content=thinking_content,
            response=response
        )
        
        return message_dict
    
    async def process_message_stream(
        self,
        messages: List[Dict[str, str]],
        provider: str = "openrouter",
        model: Optional[str] = None,
        action: str = ""
    ):
        """
        Process a message with streaming and yield partial responses.
        
        Yields:
            Tuple of (partial_message_dict, is_complete)
        """
        start_time = time.time()
        
        # Make the streaming API call
        stream = self.provider_manager.chat_completion_stream(
            messages=messages,
            provider_name=provider,
            model=model
        )
        
        # Initialize accumulation variables
        accumulated_content = ""
        accumulated_reasoning = ""
        accumulated_annotations = []
        usage_info = None
        final_response_message = None
        
        # Process the stream
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                choice = chunk.choices[0]
                delta = choice.delta
                
                # Check if this is the end of the stream
                finish_reason = getattr(choice, 'finish_reason', None)
                
                # Accumulate content
                if hasattr(delta, 'content') and delta.content:
                    accumulated_content += delta.content
                    
                    # Build partial message for streaming display
                    partial_message = {
                        "role": "assistant",
                        "content": accumulated_content,
                        "display_text": accumulated_content,
                    }
                    
                    if accumulated_reasoning:
                        partial_message["thinking"] = accumulated_reasoning
                    
                    # Yield partial update only when we have new content
                    yield partial_message, False
                
                # Accumulate reasoning (for OpenRouter models)
                if hasattr(delta, 'reasoning') and delta.reasoning:
                    accumulated_reasoning += delta.reasoning
                
                
                # If stream is finished, capture the final message for annotations
                if finish_reason:
                    if hasattr(choice, 'message'):
                        final_response_message = choice.message
                    print(f"Stream finished with reason: {finish_reason}")
                    break
            
            # Capture usage info if available
            if hasattr(chunk, 'usage') and chunk.usage:
                usage_info = chunk.usage
        
        # Calculate final timing metrics
        end_time = time.time()
        generation_time_seconds = round(end_time - start_time, 2)
        generation_time = f"{generation_time_seconds}s"
        
        # Extract final token usage
        current_response_tokens = (
            usage_info.completion_tokens
            if usage_info and hasattr(usage_info, 'completion_tokens')
            else len(accumulated_content.split()) # Rough estimate if no usage info
        )
        
        tokens_per_second = self._calculate_tokens_per_second(
            current_response_tokens, generation_time_seconds
        )
        
        # Process thinking content
        thinking_content = None
        actual_response = accumulated_content
        
        if accumulated_reasoning:
            thinking_content = accumulated_reasoning.strip()
        else:
            # Check for <think> tags in content only (no response object available in streaming)
            think_pattern = r"<think>(.*?)</think>"
            think_match = re.search(think_pattern, accumulated_content, re.DOTALL)
            
            if think_match:
                thinking_content = think_match.group(1).strip()
                actual_response = re.sub(
                    think_pattern, "", accumulated_content, flags=re.DOTALL
                ).strip()
            else:
                thinking_content = None
        
        
        # Extract citations from annotations in the final message
        citations = []
        if final_response_message and hasattr(final_response_message, 'annotations'):
            annotations = final_response_message.annotations or []
            print(f"Found {len(annotations)} annotations in final message")
            
            # Convert OpenRouter annotations to citation URLs
            for annotation in annotations:
                if (hasattr(annotation, 'type') and annotation.type == 'url_citation' and 
                    hasattr(annotation, 'url_citation') and hasattr(annotation.url_citation, 'url')):
                    citations.append(annotation.url_citation.url)
                    print(f"Extracted citation: {annotation.url_citation.url}")
        
        # If no citations found in streaming, try a non-streaming call ONLY for search models that should have citations
        if (not citations and model and 
            ("perplexity" in model.lower() or "sonar" in model.lower()) and 
            action == "Search"):
            print("No citations in streaming response for search model, making non-streaming call to get annotations...")
            try:
                non_stream_response = self.provider_manager.chat_completion(
                    messages=messages,
                    provider_name=provider,
                    model=model,
                    tools=None  # Don't include tools for citation-only call
                )
                
                if (hasattr(non_stream_response, 'choices') and non_stream_response.choices and
                    hasattr(non_stream_response.choices[0], 'message') and
                    hasattr(non_stream_response.choices[0].message, 'annotations')):
                    
                    annotations = non_stream_response.choices[0].message.annotations or []
                    print(f"Found {len(annotations)} annotations in non-streaming response")
                    
                    for annotation in annotations:
                        if (hasattr(annotation, 'type') and annotation.type == 'url_citation' and 
                            hasattr(annotation, 'url_citation') and hasattr(annotation.url_citation, 'url')):
                            citations.append(annotation.url_citation.url)
                            print(f"Extracted citation from non-streaming: {annotation.url_citation.url}")
                            
            except Exception as e:
                print(f"Failed to get annotations from non-streaming call: {e}")
        elif not citations:
            print("No citations expected for this model/action combination")
        
        # Build final message dictionary manually for streaming
        final_message: ChatMessage = {
            "role": "assistant",
            "content": actual_response,
            "display_text": actual_response,
            "citations": citations,
            "generation_time": generation_time,
            "total_tokens": current_response_tokens,
            "tokens_per_second": tokens_per_second,
        }
        
        if thinking_content:
            final_message["thinking"] = thinking_content
        
        # Yield final complete message
        yield final_message, True
    
    
    def _extract_tokens(self, response) -> int:
        """Extract token count from response."""
        return (
            response.usage.completion_tokens
            if hasattr(response, "usage")
            and response.usage
            and hasattr(response.usage, "completion_tokens")
            else 0
        )
    
    def _calculate_tokens_per_second(self, tokens: int, time_seconds: float) -> float:
        """Calculate tokens per second."""
        return (
            round(tokens / time_seconds, 2)
            if time_seconds > 0 and tokens > 0
            else 0
        )
    
    def _extract_thinking(self, response_text: str, response) -> Tuple[Optional[str], str]:
        """Extract thinking content and actual response."""
        thinking_content = None
        actual_response = response_text or ""
        
        # Handle None response_text
        if response_text is None:
            return thinking_content, actual_response
        
        # Method 1: Check for thinking tokens in the format <think>...</think>
        think_pattern = r"<think>(.*?)</think>"
        think_match = re.search(think_pattern, response_text, re.DOTALL)
        
        if think_match:
            thinking_content = think_match.group(1).strip()
            actual_response = re.sub(
                think_pattern, "", response_text, flags=re.DOTALL
            ).strip()
        # Method 2: Check for reasoning parameter in OpenRouter responses
        elif (
            hasattr(response.choices[0].message, "reasoning")
            and response.choices[0].message.reasoning
        ):
            thinking_content = response.choices[0].message.reasoning.strip()
        
        return thinking_content, actual_response
    
    
    def _build_message_dict(
        self,
        actual_response: str,
        generation_time: str,
        current_response_tokens: int,
        tokens_per_second: float,
        thinking_content: Optional[str],
        response
    ) -> ChatMessage:
        """Build the message dictionary."""
        # Get citations if available
        citations = getattr(response, "citations", [])
        
        message_dict: ChatMessage = {
            "role": "assistant",
            "content": actual_response,  # Keep as string for UI compatibility
            "display_text": actual_response,  # Add display_text field
            "citations": citations,
            "generation_time": generation_time,
            "total_tokens": current_response_tokens,
            "tokens_per_second": tokens_per_second,
        }
        
        if thinking_content:
            message_dict["thinking"] = thinking_content
        
        return message_dict


# Global message handler instance
message_handler = MessageHandler()