"""
OpenRouter provider implementation.
"""

import os
from typing import List
from ark.models import ProviderConfig
from .base import BaseProvider


class OpenRouterProvider(BaseProvider):
    """OpenRouter AI provider."""

    def __init__(self):
        config: ProviderConfig = {
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": os.environ.get("OPENROUTER_API_KEY", ""),
            "default_model": "google/gemini-2.0-flash-001",
        }
        super().__init__(config)

    def get_available_models(self) -> List[str]:
        """Get available OpenRouter models."""
        # For OpenRouter, we can define common models or fetch from API
        return [
            "google/gemini-2.0-flash-001",
            "perplexity/sonar",
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4",
        ]

    def is_connected(self) -> bool:
        """Check if OpenRouter is available."""
        return bool(self.config["api_key"])

    def supports_tools(self, model: str) -> bool:
        """Check if a model supports tool calling."""
        # Perplexity models don't support tools
        return not ("perplexity" in model.lower() or "sonar" in model.lower())
