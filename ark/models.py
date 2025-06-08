"""
Data models and type definitions for the Ark application.
"""
from typing import TypedDict, List, Optional


class WeatherCoordinates(TypedDict):
    lat: float
    lon: float


class WeatherLocation(TypedDict):
    city: str
    state: str
    country: str
    coordinates: WeatherCoordinates


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


class WeatherTimestamp(TypedDict):
    current_time: str
    current_day: str
    current_date: str
    timezone_offset: int


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


class HourlyForecast(TypedDict):
    time: str
    time_24: str
    temperature: int
    weather_main: str
    weather_icon: str
    timestamp: int


class WeatherUnits(TypedDict):
    temperature: str
    wind_speed: str
    pressure: str
    visibility: str


class WeatherApiInfo(TypedDict):
    provider: str
    last_updated: str
    units_system: str


class WeatherData(TypedDict):
    location: WeatherLocation
    current: CurrentWeather
    timestamp: WeatherTimestamp
    daily_forecast: List[DailyForecast]
    hourly_forecast: List[HourlyForecast]
    units: WeatherUnits
    api_info: WeatherApiInfo


class ChatMessage(TypedDict, total=False):
    role: str
    content: str
    citations: List[str]
    generation_time: str
    total_tokens: int
    tokens_per_second: float
    thinking: str
    tool_name: str
    tool_args: str
    weather_data: WeatherData
    weather_location: str


class ProviderConfig(TypedDict):
    base_url: str
    api_key: str
    default_model: Optional[str]