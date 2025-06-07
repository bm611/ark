import reflex as rx
from typing import Dict, Any


def format_time(time_str: str) -> str:
    """Formats a time string (e.g., '07:50 PM') to a shorter format ('7:50 PM')."""
    if time_str.startswith("0"):
        return time_str[1:]
    return time_str


def get_weather_icon(weather_main: str, is_sunny: bool) -> str:
    """Returns a weather icon based on the weather condition."""
    if is_sunny:
        return "sun"
    weather_icons = {
        "Haze": "cloud-sun",
        "Clear": "sun",
        "Clouds": "cloud",
        "Rain": "cloud-rain",
        "Drizzle": "cloud-drizzle",
        "Thunderstorm": "cloud-lightning",
        "Snow": "cloud-snow",
    }
    return weather_icons.get(weather_main, "cloud")


def get_weather_gradient(weather_main: str, is_sunny: bool) -> str:
    """Returns a gradient background class based on the weather condition."""
    if is_sunny or weather_main == "Clear":
        return "bg-gradient-to-br from-amber-300 to-orange-400"

    weather_gradients = {
        "Haze": "bg-gradient-to-br from-gray-300 to-gray-400",
        "Clouds": "bg-gradient-to-br from-slate-300 to-slate-500",
        "Rain": "bg-gradient-to-br from-blue-400 to-blue-600",
        "Drizzle": "bg-gradient-to-br from-blue-300 to-blue-500",
        "Thunderstorm": "bg-gradient-to-br from-gray-400 to-gray-6 00",
        "Snow": "bg-gradient-to-br from-blue-100 to-blue-300",
    }
    return weather_gradients.get(
        weather_main, "bg-gradient-to-br from-gray-300 to-gray-500"
    )


def weather_card(weather_data: Dict[str, Any]) -> rx.Component:
    """
    A beautifully designed weather UI component that displays current weather
    and a 6-day forecast. This component is designed to be easily integrated
    into your existing application, matching your established styles for a
    consistent look and feel.

    Args:
        weather_data: A dictionary containing the weather information.

    Returns:
        A Reflex component that visually represents the weather data.
    """
    current_temp = f"{weather_data['current']['temperature']}{weather_data['units']['temperature']}"
    current_time = format_time(weather_data["timestamp"]["current_time"])
    current_day = weather_data["timestamp"]["current_day"]
    current_weather = weather_data["current"]["weather_main"]
    is_sunny = weather_data["current"]["is_sunny"]
    high_temp = f"{weather_data['daily_forecast'][0]['high_temp']}"
    low_temp = f"{weather_data['daily_forecast'][0]['low_temp']}"
    gradient_class = get_weather_gradient(current_weather, is_sunny)

    return rx.box(
        rx.vstack(
            # Top Section: Current Weather
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            get_weather_icon(current_weather, is_sunny),
                            size=32,
                            class_name="text-black sm:w-12 sm:h-12",
                        ),
                        rx.text(
                            current_temp,
                            class_name="font-[dm] text-3xl sm:text-5xl font-bold text-black",
                        ),
                        align="center",
                    ),
                    rx.text(
                        f"{current_weather}",
                        class_name="font-[dm] text-lg sm:text-2xl text-black font-medium",
                    ),
                    align="start",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text(
                        f"{weather_data['location']['city']}, {weather_data['location']['country']}",
                        class_name="font-[dm] text-sm sm:text-xl text-black font-medium text-right",
                    ),
                    rx.text(
                        f"{current_day}, {current_time}",
                        class_name="font-[dm] text-xs sm:text-lg text-black text-right",
                    ),
                    rx.text(
                        f"H: {high_temp}° L: {low_temp}°",
                        class_name="font-[dm] text-xs sm:text-lg text-black text-right",
                    ),
                    align="end",
                ),
                class_name="w-full items-center",
                spacing="2",
            ),
            # Bottom Section: 6-Day Forecast
            rx.box(
                rx.hstack(
                    *[
                        rx.vstack(
                            rx.text(
                                day["day_short"],
                                class_name="font-[dm] text-sm sm:text-lg text-black font-medium",
                            ),
                            rx.icon(
                                get_weather_icon(day["weather_main"], day["is_sunny"]),
                                size=24,
                                class_name="text-black my-1 sm:my-2 w-6 h-6 sm:w-8 sm:h-8",
                            ),
                            rx.text(
                                f"{day['high_temp']}°",
                                class_name="font-[dm] text-lg sm:text-xl text-black font-bold",
                            ),
                            rx.text(
                                f"{day['low_temp']}°",
                                class_name="font-[dm] text-md sm:text-lg text-black",
                            ),
                            align="center",
                            class_name="flex-shrink-0 gap-1 w-16 md:w-1/6",
                        )
                        for day in weather_data["daily_forecast"]
                    ],
                    class_name="gap-0",
                ),
                class_name="w-full pt-4 overflow-x-auto",
            ),
            class_name="w-full",
            spacing="6",
        ),
        class_name=f"{gradient_class} p-6 rounded-3xl shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] border-4 border-black",
        width="100%",
        max_width="700px",
    )


def weather_demo() -> rx.Component:
    """Demo component with sample weather data"""
    sample_data = {
        "location": {
            "city": "San Jose",
            "state": "",
            "country": "US",
            "coordinates": {"lat": 37.3394, "lon": -121.895},
        },
        "current": {
            "temperature": 69,
            "feels_like": 69,
            "weather_main": "Thunderstorm",
            "weather_description": "Sunny",
            "weather_icon": "50d",
            "is_sunny": False,
            "humidity": 64,
            "pressure": 1010,
            "visibility": 10.0,
            "uv_index": None,
            "wind_speed": 12.66,
            "wind_direction": 340,
        },
        "timestamp": {
            "current_time": "07:50 PM",
            "current_day": "Wednesday",
            "current_date": "June 04, 2025",
            "timezone_offset": -25200,
        },
        "daily_forecast": [
            {
                "day": "Today",
                "day_short": "Wed",
                "date": "2025-06-04",
                "high_temp": 73,
                "low_temp": 64,
                "weather_main": "Haze",
                "weather_description": "Haze",
                "weather_icon": "50d",
                "is_sunny": False,
            },
            {
                "day": "Thursday",
                "day_short": "Thu",
                "date": "2025-06-05",
                "high_temp": 88,
                "low_temp": 55,
                "weather_main": "Clear",
                "weather_description": "Clear Sky",
                "weather_icon": "01n",
                "is_sunny": True,
            },
            {
                "day": "Friday",
                "day_short": "Fri",
                "date": "2025-06-06",
                "high_temp": 92,
                "low_temp": 56,
                "weather_main": "Clear",
                "weather_description": "Clear Sky",
                "weather_icon": "01n",
                "is_sunny": True,
            },
            {
                "day": "Saturday",
                "day_short": "Sat",
                "date": "2025-06-07",
                "high_temp": 92,
                "low_temp": 60,
                "weather_main": "Clear",
                "weather_description": "Clear Sky",
                "weather_icon": "01n",
                "is_sunny": True,
            },
            {
                "day": "Sunday",
                "day_short": "Sun",
                "date": "2025-06-08",
                "high_temp": 92,
                "low_temp": 61,
                "weather_main": "Clear",
                "weather_description": "Clear Sky",
                "weather_icon": "01n",
                "is_sunny": True,
            },
            {
                "day": "Monday",
                "day_short": "Mon",
                "date": "2025-06-09",
                "high_temp": 97,
                "low_temp": 61,
                "weather_main": "Clear",
                "weather_description": "Clear Sky",
                "weather_icon": "01n",
                "is_sunny": True,
            },
        ],
        "hourly_forecast": [
            {
                "time": "8 PM",
                "time_24": "20:00",
                "temperature": 69,
                "weather_main": "Clear",
                "weather_icon": "01d",
                "timestamp": 1749092400,
            },
            {
                "time": "11 PM",
                "time_24": "23:00",
                "temperature": 66,
                "weather_main": "Clear",
                "weather_icon": "01n",
                "timestamp": 1749103200,
            },
            {
                "time": "2 AM",
                "time_24": "02:00",
                "temperature": 60,
                "weather_main": "Clear",
                "weather_icon": "01n",
                "timestamp": 1749114000,
            },
            {
                "time": "5 AM",
                "time_24": "05:00",
                "temperature": 55,
                "weather_main": "Clouds",
                "weather_icon": "02n",
                "timestamp": 1749124800,
            },
            {
                "time": "8 AM",
                "time_24": "08:00",
                "temperature": 58,
                "weather_main": "Clouds",
                "weather_icon": "02d",
                "timestamp": 1749135600,
            },
            {
                "time": "11 AM",
                "time_24": "11:00",
                "temperature": 72,
                "weather_main": "Clear",
                "weather_icon": "01d",
                "timestamp": 1749146400,
            },
            {
                "time": "2 PM",
                "time_24": "14:00",
                "temperature": 88,
                "weather_main": "Clear",
                "weather_icon": "01d",
                "timestamp": 1749157200,
            },
            {
                "time": "5 PM",
                "time_24": "17:00",
                "temperature": 87,
                "weather_main": "Clear",
                "weather_icon": "01d",
                "timestamp": 1749168000,
            },
            {
                "time": "8 PM",
                "time_24": "20:00",
                "temperature": 72,
                "weather_main": "Clear",
                "weather_icon": "01d",
                "timestamp": 1749178800,
            },
            {
                "time": "11 PM",
                "time_24": "23:00",
                "temperature": 60,
                "weather_main": "Clear",
                "weather_icon": "01n",
                "timestamp": 1749189600,
            },
            {
                "time": "2 AM",
                "time_24": "02:00",
                "temperature": 57,
                "weather_main": "Clear",
                "weather_icon": "01n",
                "timestamp": 1749200400,
            },
            {
                "time": "5 AM",
                "time_24": "05:00",
                "temperature": 56,
                "weather_main": "Clear",
                "weather_icon": "01n",
                "timestamp": 1749211200,
            },
        ],
        "units": {
            "temperature": "°F",
            "wind_speed": "mph",
            "pressure": "hPa",
            "visibility": "km",
        },
        "api_info": {
            "provider": "OpenWeatherMap",
            "last_updated": "2025-06-04T19:50:16.850724",
            "units_system": "imperial",
        },
    }

    return weather_card(sample_data)
