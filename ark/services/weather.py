import requests
from datetime import datetime
import os


def get_weather_data(city, state=None, country=None, units="imperial"):
    """
    Fetch weather data from OpenWeatherMap API for UI display

    Args:
        city (str): City name (e.g., "Campbell")
        state (str, optional): State code (e.g., "CA")
        country (str, optional): Country code (e.g., "US")
        units (str): Temperature units - 'imperial' (°F), 'metric' (°C), 'kelvin'

    Returns:
        dict: Weather data formatted for UI display
    """

    # Build location query
    location_query = city
    if state:
        location_query += f",{state}"
    if country:
        location_query += f",{country}"

    # API endpoints
    current_url = "https://api.openweathermap.org/data/2.5/weather"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    # Parameters
    params = {
        "q": location_query,
        "appid": os.environ["OPENWEATHER_API_KEY"],
        "units": units,
    }

    try:
        # Get current weather
        current_response = requests.get(current_url, params=params)
        current_response.raise_for_status()
        current_data = current_response.json()

        # Get 5-day forecast
        forecast_response = requests.get(forecast_url, params=params)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Process current weather
        current_temp = round(current_data["main"]["temp"])
        feels_like = round(current_data["main"]["feels_like"])
        weather_main = current_data["weather"][0]["main"]
        weather_description = current_data["weather"][0]["description"].title()
        weather_icon = current_data["weather"][0]["icon"]

        # Get current time info
        current_time = datetime.now()
        timezone_offset = current_data.get("timezone", 0)

        # Process daily forecasts (next 6 days including today)
        daily_forecasts = []
        processed_dates = set()

        # Add today's data first
        today_date = current_time.strftime("%Y-%m-%d")
        daily_forecasts.append(
            {
                "day": "Today",
                "day_short": current_time.strftime("%a"),
                "date": today_date,
                "high_temp": round(current_data["main"]["temp_max"]),
                "low_temp": round(current_data["main"]["temp_min"]),
                "weather_main": weather_main,
                "weather_description": weather_description,
                "weather_icon": weather_icon,
                "is_sunny": weather_main.lower() in ["clear", "sunny"],
            }
        )
        processed_dates.add(today_date)

        # Process forecast data for next days
        for item in forecast_data["list"]:
            forecast_date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")

            if forecast_date not in processed_dates and len(daily_forecasts) < 6:
                forecast_time = datetime.fromtimestamp(item["dt"])

                # Find min/max temps for the day
                day_temps = []
                for forecast_item in forecast_data["list"]:
                    forecast_item_date = datetime.fromtimestamp(
                        forecast_item["dt"]
                    ).strftime("%Y-%m-%d")
                    if forecast_item_date == forecast_date:
                        day_temps.append(forecast_item["main"]["temp"])

                daily_forecasts.append(
                    {
                        "day": forecast_time.strftime("%A"),
                        "day_short": forecast_time.strftime("%a"),
                        "date": forecast_date,
                        "high_temp": round(max(day_temps))
                        if day_temps
                        else round(item["main"]["temp"]),
                        "low_temp": round(min(day_temps))
                        if day_temps
                        else round(item["main"]["temp"]),
                        "weather_main": item["weather"][0]["main"],
                        "weather_description": item["weather"][0][
                            "description"
                        ].title(),
                        "weather_icon": item["weather"][0]["icon"],
                        "is_sunny": item["weather"][0]["main"].lower()
                        in ["clear", "sunny"],
                    }
                )
                processed_dates.add(forecast_date)

        # Get hourly forecast for today (next 12 hours)
        hourly_forecasts = []
        current_hour = current_time.hour

        for i, item in enumerate(
            forecast_data["list"][:12]
        ):  # Next 12 forecast points (36 hours)
            forecast_time = datetime.fromtimestamp(item["dt"])

            hourly_forecasts.append(
                {
                    "time": forecast_time.strftime("%I %p").lstrip("0"),
                    "time_24": forecast_time.strftime("%H:%M"),
                    "temperature": round(item["main"]["temp"]),
                    "weather_main": item["weather"][0]["main"],
                    "weather_icon": item["weather"][0]["icon"],
                    "timestamp": item["dt"],
                }
            )

        # Build the complete weather data dictionary
        weather_data = {
            "location": {
                "city": current_data["name"],
                "state": state or "",
                "country": current_data["sys"]["country"],
                "coordinates": {
                    "lat": current_data["coord"]["lat"],
                    "lon": current_data["coord"]["lon"],
                },
            },
            "current": {
                "temperature": current_temp,
                "feels_like": feels_like,
                "weather_main": weather_main,
                "weather_description": weather_description,
                "weather_icon": weather_icon,
                "is_sunny": weather_main.lower() in ["clear", "sunny"],
                "humidity": current_data["main"]["humidity"],
                "pressure": current_data["main"]["pressure"],
                "visibility": current_data.get("visibility", 0) / 1000,  # Convert to km
                "uv_index": None,  # Would need separate UV API call
                "wind_speed": current_data["wind"]["speed"],
                "wind_direction": current_data["wind"].get("deg", 0),
            },
            "timestamp": {
                "current_time": current_time.strftime("%I:%M %p"),
                "current_day": current_time.strftime("%A"),
                "current_date": current_time.strftime("%B %d, %Y"),
                "timezone_offset": timezone_offset,
            },
            "daily_forecast": daily_forecasts,
            "hourly_forecast": hourly_forecasts,
            "units": {
                "temperature": "°F"
                if units == "imperial"
                else "°C"
                if units == "metric"
                else "K",
                "wind_speed": "mph" if units == "imperial" else "m/s",
                "pressure": "hPa",
                "visibility": "km",
            },
            "api_info": {
                "provider": "OpenWeatherMap",
                "last_updated": datetime.now().isoformat(),
                "units_system": units,
            },
        }

        return weather_data

    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "message": f"API request failed: {str(e)}",
            "error_type": "network_error",
        }
    except KeyError as e:
        return {
            "error": True,
            "message": f"Unexpected API response format: {str(e)}",
            "error_type": "data_error",
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Unexpected error: {str(e)}",
            "error_type": "unknown_error",
        }


def schema():
    """
    Returns a tool schema for the get_weather_data function.
    """
    return {
        "type": "function",
        "function": {
            "name": "get_weather_data",
            "description": "Fetch weather data from OpenWeatherMap API for UI display",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": 'City name (e.g., "Campbell")',
                    },
                    "state": {
                        "type": "string",
                        "description": 'State code (e.g., "CA")',
                    },
                    "country": {
                        "type": "string",
                        "description": 'Country code (e.g., "US")',
                    },
                    "units": {
                        "type": "string",
                        "description": "Temperature units - 'imperial' (°F), 'metric' (°C), 'kelvin')",
                        "default": "imperial",
                    },
                },
                "required": ["city"],
            },
        },
    }
