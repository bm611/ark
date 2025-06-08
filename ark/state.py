import reflex as rx
import time
from typing import TypedDict, List, Optional
from ark.services import openrouter
from ark.services.weather import get_weather_data
import json


# Define the structure for weather coordinates
class WeatherCoordinates(TypedDict):
    lat: float
    lon: float


# Define the structure for weather location
class WeatherLocation(TypedDict):
    city: str
    state: str
    country: str
    coordinates: WeatherCoordinates


# Define the structure for current weather
class CurrentWeather(TypedDict):
    temperature: int | float
    feels_like: int | float
    weather_main: str
    weather_description: str
    weather_icon: str
    is_sunny: bool
    humidity: int
    pressure: int
    visibility: float
    uv_index: int | None
    wind_speed: float
    wind_direction: int


# Define the structure for timestamp
class WeatherTimestamp(TypedDict):
    current_time: str
    current_day: str
    current_date: str
    timezone_offset: int


# Define the structure for daily forecast item
class DailyForecast(TypedDict):
    day: str
    day_short: str
    date: str
    high_temp: int
    low_temp: int
    weather_main: str
    weather_description: str
    weather_icon: str
    is_sunny: bool


# Define the structure for hourly forecast item
class HourlyForecast(TypedDict):
    time: str
    time_24: str
    temperature: int
    weather_main: str
    weather_icon: str
    timestamp: int


# Define the structure for weather units
class WeatherUnits(TypedDict):
    temperature: str
    wind_speed: str
    pressure: str
    visibility: str


# Define the structure for API info
class WeatherApiInfo(TypedDict):
    provider: str
    last_updated: str
    units_system: str


# Define the complete weather data structure
class WeatherData(TypedDict):
    location: WeatherLocation
    current: CurrentWeather
    timestamp: WeatherTimestamp
    daily_forecast: List[DailyForecast]
    hourly_forecast: List[HourlyForecast]
    units: WeatherUnits
    api_info: WeatherApiInfo


class State(rx.State):
    prompt: str = ""
    messages: list[dict[str, str]] = []
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
                # Safely get citations if they exist
                citations = getattr(response, "citations", [])
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

        # Extract token usage information - use completion_tokens (output only) for accurate per-response metrics
        current_response_tokens = (
            response.usage.completion_tokens
            if hasattr(response, "usage")
            and response.usage
            and hasattr(response.usage, "completion_tokens")
            else 0
        )

        tokens_per_second = (
            round(current_response_tokens / generation_time_seconds, 2)
            if generation_time_seconds > 0 and current_response_tokens > 0
            else 0
        )

        self.is_gen = False
        response_text = response.choices[0].message.content

        # check if tools were used [TODO: using first index]
        tool_name = None
        tool_args = None
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            self.is_tool_use = True
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            if tool_name == "get_weather_data":
                weather_result = get_weather_data(
                    tool_args["location"], tool_args.get("units", "imperial")
                )
                # Only set weather_data if it's not an error response
                if not weather_result.get("error", False):
                    self.weather_data = weather_result
                    self.weather_location = tool_args["location"]
                else:
                    # Keep weather_data as None when there's an error
                    self.weather_data = None
                    self.weather_location = tool_args["location"]
        else:
            self.is_tool_use = False

        # Extract thinking tokens if they exist
        thinking_content = None
        actual_response = response_text

        # Method 1: Check for thinking tokens in the format <think>...</think>
        import re

        think_pattern = r"<think>(.*?)</think>"
        think_match = re.search(think_pattern, response_text, re.DOTALL)

        if think_match:
            thinking_content = think_match.group(1).strip()
            # Remove the thinking tokens from the actual response
            actual_response = re.sub(
                think_pattern, "", response_text, flags=re.DOTALL
            ).strip()
        # Method 2: Check for reasoning parameter in OpenRouter responses
        elif (
            hasattr(response.choices[0].message, "reasoning")
            and response.choices[0].message.reasoning
        ):
            thinking_content = response.choices[0].message.reasoning.strip()
            # The actual response is already clean in this case

        # Prepare the message dictionary
        message_dict = {
            "role": "assistant",
            "content": actual_response,
            "citations": citations,
            "generation_time": generation_time,
            "total_tokens": current_response_tokens,  # Show tokens for this response only
            "tokens_per_second": tokens_per_second,
        }

        # Add thinking content if it exists
        if thinking_content:
            message_dict["thinking"] = thinking_content

        # Add tool information if tools were used
        if tool_name:
            message_dict["tool_name"] = tool_name
            message_dict["tool_args"] = (
                json.dumps(tool_args, indent=2) if tool_args else "{}"
            )

        # Add weather data if available
        if self.weather_data:
            message_dict["weather_data"] = self.weather_data
            message_dict["weather_location"] = self.weather_location

        # Add assistant response with generation time and token metrics
        self.messages.append(message_dict)

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
