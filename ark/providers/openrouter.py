"""
OpenRouter provider implementation.
"""

import os
from typing import List
from ark.models.provider import ProviderConfig
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

    def chat_completion_with_fallback(
        self, 
        messages: List, 
        model: str,
        fallback_model: str,
        **kwargs
    ):
        """Create a chat completion with fallback model support using OpenRouter's extra_body."""
        completion_kwargs = {
            "model": model,
            "messages": messages,
            "extra_body": {
                "models": [fallback_model],
            },
            **kwargs
        }
        
        return self.client.chat.completions.create(**completion_kwargs)
    
    def chat_completion_stream_with_fallback(
        self, 
        messages: List, 
        model: str,
        fallback_model: str,
        **kwargs
    ):
        """Create a streaming chat completion with fallback model support using OpenRouter's extra_body."""
        completion_kwargs = {
            "model": model,
            "messages": messages,
            "stream": True,
            "extra_body": {
                "models": [fallback_model],
            },
            **kwargs
        }
        
        return self.client.chat.completions.create(**completion_kwargs)
