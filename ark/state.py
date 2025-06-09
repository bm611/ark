import reflex as rx
from typing import List, Optional
from ark.models import WeatherData, ChatMessage
from ark.handlers.message_handler import message_handler


# Model Configuration Constants
class ModelConfig:
    DEFAULT_PROVIDER = "openrouter"
    CHAT_MODEL = "google/gemini-2.5-flash-preview"
    SEARCH_MODEL = "perplexity/sonar"
    TURBO_MODEL = "qwen/qwen3-32b"


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
    selected_provider: str = ModelConfig.DEFAULT_PROVIDER
    selected_model: str = ModelConfig.CHAT_MODEL

    # Weather-related state variables
    weather_data: Optional[WeatherData] = None
    weather_location: str = ""

    # Theme state
    is_dark_theme: bool = False

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
        self.selected_provider = ModelConfig.DEFAULT_PROVIDER
        self.selected_model = ModelConfig.CHAT_MODEL
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
        message_dict, new_weather_data, new_weather_location = (
            message_handler.process_message(
                messages=self.messages,
                provider=self.selected_provider,
                model=model,
                action=self.selected_action,
                weather_data=self.weather_data,
                weather_location=self.weather_location,
            )
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
            if self.selected_provider == ModelConfig.DEFAULT_PROVIDER:
                return ModelConfig.SEARCH_MODEL
            # For offline providers, use their selected model
            return self.selected_model if self.selected_model else None
        elif self.selected_action == "Turbo":
            if self.selected_provider == ModelConfig.DEFAULT_PROVIDER:
                return ModelConfig.TURBO_MODEL
            return self.selected_model if self.selected_model else None
        else:
            # Regular chat - use selected model
            return self.selected_model if self.selected_model else None

    def select_action(self, action: str):
        if self.selected_action == action:
            # Deactivating the current action - reset to defaults
            self.selected_action = ""
            self.selected_provider = ModelConfig.DEFAULT_PROVIDER
            self.selected_model = ModelConfig.CHAT_MODEL
        else:
            self.selected_action = action

    def handle_search_click(self):
        """Handle search button click - toggle action and set/reset model accordingly"""
        if self.selected_action == "Search":
            # Deactivating search - reset to defaults
            self.selected_action = ""
            self.selected_provider = ModelConfig.DEFAULT_PROVIDER
            self.selected_model = ModelConfig.CHAT_MODEL
        else:
            # Activating search - set search model
            self.selected_action = "Search"
            self.selected_provider = ModelConfig.DEFAULT_PROVIDER
            self.selected_model = ModelConfig.SEARCH_MODEL

    def handle_turbo_click(self):
        """Handle turbo button click - toggle action and set/reset model accordingly"""
        if self.selected_action == "Turbo":
            # Deactivating turbo - reset to defaults
            self.selected_action = ""
            self.selected_provider = ModelConfig.DEFAULT_PROVIDER
            self.selected_model = ModelConfig.CHAT_MODEL
        else:
            # Activating turbo - set turbo model
            self.selected_action = "Turbo"
            self.selected_provider = ModelConfig.DEFAULT_PROVIDER
            self.selected_model = ModelConfig.TURBO_MODEL

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.is_dark_theme = not self.is_dark_theme
