"""
Weather tool implementation.
"""
from typing import Dict, Any
from .base import BaseTool
from ark.services.weather import get_weather_data


class WeatherTool(BaseTool):
    """Weather information tool."""
    
    @property
    def name(self) -> str:
        return "get_weather_data"
    
    @property
    def description(self) -> str:
        return "Get current weather information for a specific location. Only use when the user explicitly asks about weather, temperature, or weather conditions."
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for OpenAI function calling."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": 'Location query (e.g., "Campbell", "Campbell,CA", "Campbell,CA,US")',
                        },
                        "units": {
                            "type": "string",
                            "description": "Temperature units - 'imperial' (°F), 'metric' (°C), 'kelvin')",
                            "default": "imperial",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    
    def execute(self, location: str, units: str = "imperial") -> Dict[str, Any]:
        """Execute the weather tool."""
        return get_weather_data(location, units)