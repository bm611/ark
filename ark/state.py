import reflex as rx
from typing import List, Optional
from ark.models import WeatherData, ChatMessage
from ark.handlers.message_handler import message_handler


class State(rx.State):
    prompt: str = ""
    messages: List[ChatMessage] = []
    is_gen: bool = False
    selected_action: str = ""
    is_tool_use: bool = False

    # Thinking section expansion state
    thinking_expanded: dict[int, bool] = {}
    # Citations section expansion state
    citations_expanded: dict[int, bool] = {}
    # Tool section expansion state
    tool_expanded: dict[int, bool] = {}

    # Provider and model selection
    selected_provider: str = "openrouter"  # Default to openrouter
    selected_model: str = "google/gemini-2.0-flash-001"  # default model

    # Weather-related state variables
    weather_data: Optional[WeatherData] = None
    weather_location: str = ""

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
        self.tool_expanded = {}
        self.weather_data = None
        self.weather_location = ""

    def toggle_thinking(self, message_index: int):
        """Toggle the thinking section for a specific message"""
        if message_index in self.thinking_expanded:
            self.thinking_expanded[message_index] = not self.thinking_expanded[
                message_index
            ]
        else:
            self.thinking_expanded[message_index] = True

    def toggle_citations(self, message_index: int):
        """Toggle the citations section for a specific message"""
        if message_index in self.citations_expanded:
            self.citations_expanded[message_index] = not self.citations_expanded[
                message_index
            ]
        else:
            self.citations_expanded[message_index] = True

    def toggle_tool(self, message_index: int):
        """Toggle the tool section for a specific message"""
        if message_index in self.tool_expanded:
            self.tool_expanded[message_index] = not self.tool_expanded[message_index]
        else:
            self.tool_expanded[message_index] = True

    def send_message(self):
        """Send message using the new message handler."""
        # Determine model based on action and selection
        model = self._get_model_for_action()
        
        # Process the message
        message_dict, new_weather_data, new_weather_location = message_handler.process_message(
            messages=self.messages,
            provider=self.selected_provider,
            model=model,
            action=self.selected_action,
            weather_data=self.weather_data,
            weather_location=self.weather_location
        )
        
        # Update state
        self.is_gen = False
        self.is_tool_use = bool(message_dict.get("tool_name"))
        
        if new_weather_data:
            self.weather_data = new_weather_data
            self.weather_location = new_weather_location
        
        # Add the message to the conversation
        self.messages.append(message_dict)

    def _get_model_for_action(self) -> str:
        """Get the appropriate model based on the selected action."""
        if self.selected_action == "Search":
            if self.selected_provider == "openrouter":
                return "perplexity/sonar"
            # For offline providers, use their selected model
            return self.selected_model if self.selected_model else None
        elif self.selected_action == "Turbo":
            if self.selected_provider == "openrouter":
                return "qwen/qwen3-32b"
            return self.selected_model if self.selected_model else None
        else:
            # Regular chat - use selected model
            return self.selected_model if self.selected_model else None

    def select_action(self, action: str):
        if self.selected_action == action:
            # Deactivating the current action - reset to defaults
            self.selected_action = ""
            self.selected_provider = "openrouter"
            self.selected_model = "google/gemini-2.0-flash-001"
        else:
            self.selected_action = action

    def handle_search_click(self):
        """Handle search button click - toggle action and set/reset model accordingly"""
        if self.selected_action == "Search":
            # Deactivating search - reset to defaults
            self.selected_action = ""
            self.selected_provider = "openrouter"
            self.selected_model = "google/gemini-2.0-flash-001"
        else:
            # Activating search - set search model
            self.selected_action = "Search"
            self.selected_provider = "openrouter"
            self.selected_model = "perplexity/sonar"

    def handle_turbo_click(self):
        """Handle turbo button click - toggle action and set/reset model accordingly"""
        if self.selected_action == "Turbo":
            # Deactivating turbo - reset to defaults
            self.selected_action = ""
            self.selected_provider = "openrouter"
            self.selected_model = "google/gemini-2.0-flash-001"
        else:
            # Activating turbo - set turbo model
            self.selected_action = "Turbo"
            self.selected_provider = "openrouter"
            self.selected_model = "qwen/qwen3-32b"