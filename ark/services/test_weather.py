from weather import get_weather_data


def test_weather():
    """
    Test function to fetch weather data - replace API_KEY with your actual key
    """

    # Test basic weather fetch
    result = get_weather_data(
        city="Campbell", state="CA", country="US", units="imperial"
    )

    if result.get("error"):
        print(f"Error fetching weather: {result['message']}")
        return False

    # Print current weather info
    current = result["current"]
    location = result["location"]

    print(f"Weather for {location['city']}, {location['state']} {location['country']}")
    print(f"Current: {current['temperature']}°F, {current['weather_description']}")
    print(f"Feels like: {current['feels_like']}°F")
    print(f"Humidity: {current['humidity']}%")

    # Print daily forecast
    print("\n5-Day Forecast:")
    for day in result["daily_forecast"]:
        print(
            f"{day['day']}: {day['high_temp']}°/{day['low_temp']}° - {day['weather_description']}"
        )

    return True


if __name__ == "__main__":
    test_weather()
