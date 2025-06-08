"""
Message handling logic for AI interactions.
"""
import time
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from ark.models import ChatMessage, WeatherData
from ark.providers.manager import provider_manager
from ark.tools.manager import tool_manager


class MessageHandler:
    """Handles message processing and AI interactions."""
    
    def __init__(self):
        self.provider_manager = provider_manager
        self.tool_manager = tool_manager
    
    def process_message(
        self,
        messages: List[Dict[str, str]],
        provider: str = "openrouter",
        model: Optional[str] = None,
        action: str = "",
        weather_data: Optional[WeatherData] = None,
        weather_location: str = ""
    ) -> Tuple[ChatMessage, Optional[WeatherData], str]:
        """
        Process a message and return the response with metadata.
        
        Returns:
            Tuple of (message_dict, weather_data, weather_location)
        """
        start_time = time.time()
        
        # Get tools for the completion
        tools = self._get_tools_for_model(model, provider)
        
        # Make the API call
        response = self.provider_manager.chat_completion(
            messages=messages,
            provider_name=provider,
            model=model,
            tools=tools
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
        
        # Handle tool calls
        tool_name, tool_args, new_weather_data, new_weather_location = self._handle_tool_calls(
            response, weather_data, weather_location
        )
        
        # Build message dictionary
        message_dict = self._build_message_dict(
            actual_response=actual_response,
            generation_time=generation_time,
            current_response_tokens=current_response_tokens,
            tokens_per_second=tokens_per_second,
            thinking_content=thinking_content,
            tool_name=tool_name,
            tool_args=tool_args,
            weather_data=new_weather_data,
            weather_location=new_weather_location,
            response=response
        )
        
        return message_dict, new_weather_data, new_weather_location
    
    def _get_tools_for_model(self, model: Optional[str], provider: str) -> Optional[List[Dict[str, Any]]]:
        """Get tools based on model and provider capabilities."""
        provider_obj = self.provider_manager.get_provider(provider)
        if not provider_obj or not hasattr(provider_obj, 'supports_tools'):
            return self.tool_manager.get_tool_schemas()
        
        model_name = model or provider_obj.config.get("default_model", "")
        if provider_obj.supports_tools(model_name):
            return self.tool_manager.get_tool_schemas()
        
        return None
    
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
        actual_response = response_text
        
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
    
    def _handle_tool_calls(
        self, 
        response, 
        current_weather_data: Optional[WeatherData], 
        current_weather_location: str
    ) -> Tuple[Optional[str], Optional[str], Optional[WeatherData], str]:
        """Handle tool calls from the response."""
        tool_name = None
        tool_args = None
        weather_data = current_weather_data
        weather_location = current_weather_location
        
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args_dict = json.loads(tool_call.function.arguments)
            tool_args = json.dumps(tool_args_dict, indent=2) if tool_args_dict else "{}"
            
            # Execute the tool
            if tool_name == "get_weather_data":
                weather_result = self.tool_manager.execute_tool(
                    tool_name, 
                    location=tool_args_dict["location"], 
                    units=tool_args_dict.get("units", "imperial")
                )
                
                if not weather_result.get("error", False):
                    weather_data = weather_result
                    weather_location = tool_args_dict["location"]
                else:
                    weather_data = None
                    weather_location = tool_args_dict["location"]
        
        return tool_name, tool_args, weather_data, weather_location
    
    def _build_message_dict(
        self,
        actual_response: str,
        generation_time: str,
        current_response_tokens: int,
        tokens_per_second: float,
        thinking_content: Optional[str],
        tool_name: Optional[str],
        tool_args: Optional[str],
        weather_data: Optional[WeatherData],
        weather_location: str,
        response
    ) -> ChatMessage:
        """Build the message dictionary."""
        # Get citations if available
        citations = getattr(response, "citations", [])
        
        message_dict: ChatMessage = {
            "role": "assistant",
            "content": actual_response,
            "citations": citations,
            "generation_time": generation_time,
            "total_tokens": current_response_tokens,
            "tokens_per_second": tokens_per_second,
        }
        
        if thinking_content:
            message_dict["thinking"] = thinking_content
        
        if tool_name:
            message_dict["tool_name"] = tool_name
            message_dict["tool_args"] = tool_args or "{}"
        
        if weather_data:
            message_dict["weather_data"] = weather_data
            message_dict["weather_location"] = weather_location
        
        return message_dict


# Global message handler instance
message_handler = MessageHandler()