import reflex as rx
import time
from tbd.services import openrouter


class State(rx.State):
    prompt: str = ""
    messages: list[dict[str, str]] = []
    is_gen: bool = False
    selected_action: str = ""
    
    # Thinking section expansion state
    thinking_expanded: dict[int, bool] = {}
    # Citations section expansion state
    citations_expanded: dict[int, bool] = {}

    # Provider and model selection
    selected_provider: str = "openrouter"  # Default to openrouter
    selected_model: str = "google/gemini-2.0-flash-001"  # default model

    @rx.var
    def current_url(self) -> str:
        return self.router.page.path

    def set_prompt(self, value: str):
        self.prompt = value

    def set_provider_and_model(self, provider: str, model: str = ""):
        """Set the selected provider and model from offline models selection"""
        self.selected_provider = provider
        self.selected_model = model
        print(f"Provider set to: {provider}, Model: {model or 'default'}")

    def handle_generation(self):
        self.is_gen = True
        self.messages.append({"role": "user", "content": self.prompt})
        self.prompt = ""

    def reset_chat(self):
        self.messages = []
        self.is_gen = False
        self.selected_provider = "openrouter"
        self.selected_model = "google/gemini-2.0-flash-001"
        self.selected_action = ""
        self.thinking_expanded = {}
        self.citations_expanded = {}

    def toggle_thinking(self, message_index: int):
        """Toggle the thinking section for a specific message"""
        if message_index in self.thinking_expanded:
            self.thinking_expanded[message_index] = not self.thinking_expanded[message_index]
        else:
            self.thinking_expanded[message_index] = True

    def toggle_citations(self, message_index: int):
        """Toggle the citations section for a specific message"""
        if message_index in self.citations_expanded:
            self.citations_expanded[message_index] = not self.citations_expanded[message_index]
        else:
            self.citations_expanded[message_index] = True

    def send_message(self):
        # Record start time for response generation
        start_time = time.time()

        # Determine which model to use based on action and selection
        if self.selected_action == "Search":
            # For search, use Perplexity if on OpenRouter, otherwise use selected provider
            if self.selected_provider == "openrouter":
                response = openrouter.ask(
                    self.messages,
                    model=self.selected_model,
                    provider=self.selected_provider,
                )
                citations = response.citations
            else:
                # Use the selected offline provider for search
                model = self.selected_model if self.selected_model else None
                response = openrouter.ask(
                    self.messages, model=model, provider=self.selected_provider
                )
                citations = []
        else:
            # For regular chat, use the selected provider and model
            model = self.selected_model if self.selected_model else None
            response = openrouter.ask(
                self.messages, model=model, provider=self.selected_provider
            )
            citations = []

        # Calculate response generation time
        end_time = time.time()
        generation_time_seconds = round(end_time - start_time, 2)
        generation_time = f"{generation_time_seconds}s"

        # Extract token usage information
        total_tokens = (
            response.usage.total_tokens
            if hasattr(response, "usage") and response.usage
            else 0
        )
        tokens_per_second = (
            round(total_tokens / generation_time_seconds, 2)
            if generation_time_seconds > 0
            else 0
        )

        self.is_gen = False
        response_text = response.choices[0].message.content

        # Extract thinking tokens if they exist
        thinking_content = None
        actual_response = response_text
        
        # Check for thinking tokens in the format <think>...</think>
        import re
        think_pattern = r'<think>(.*?)</think>'
        think_match = re.search(think_pattern, response_text, re.DOTALL)
        
        if think_match:
            thinking_content = think_match.group(1).strip()
            # Remove the thinking tokens from the actual response
            actual_response = re.sub(think_pattern, '', response_text, flags=re.DOTALL).strip()

        # Prepare the message dictionary
        message_dict = {
            "role": "assistant",
            "content": actual_response,
            "citations": citations,
            "generation_time": generation_time,
            "total_tokens": total_tokens,
            "tokens_per_second": tokens_per_second,
        }
        
        # Add thinking content if it exists
        if thinking_content:
            message_dict["thinking"] = thinking_content

        # Add assistant response with generation time and token metrics
        self.messages.append(message_dict)

    def select_action(self, action: str):
        if self.selected_action == action:
            self.selected_action = ""
        else:
            self.selected_action = action
