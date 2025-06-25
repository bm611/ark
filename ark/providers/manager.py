"""
Provider manager for centralized AI provider handling.
"""

from typing import Optional, List, Dict, Any
from .base import ProviderRegistry, BaseProvider
from .openrouter import OpenRouterProvider
from .ollama import OllamaProvider
from .lmstudio import LMStudioProvider
from .prompt import system_message_prompt


class ProviderManager:
    """Centralized manager for AI providers."""

    def __init__(self):
        self.registry = ProviderRegistry()
        self._initialize_providers()
        self._default_system_message = system_message_prompt

    def _initialize_providers(self):
        """Initialize and register all providers."""
        self.registry.register("openrouter", OpenRouterProvider())
        self.registry.register("ollama", OllamaProvider())
        self.registry.register("lmstudio", LMStudioProvider())

    def get_provider(self, name: str) -> Optional[BaseProvider]:
        """Get a provider by name."""
        return self.registry.get(name)

    def list_providers(self) -> List[str]:
        """List all provider names."""
        return self.registry.list_providers()

    def get_available_providers(self) -> List[str]:
        """Get providers that are currently available."""
        return self.registry.get_available_providers()

    def get_models_for_provider(self, provider_name: str) -> List[str]:
        """Get available models for a specific provider."""
        provider = self.get_provider(provider_name)
        if provider:
            return provider.get_available_models()
        return []

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        provider_name: str = "openrouter",
        model: Optional[str] = None,
        **kwargs,
    ):
        """Create a chat completion using specified provider."""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError(f"Provider '{provider_name}' not found")

        # Prepend system message if not already present
        full_messages = messages.copy()
        if not full_messages or full_messages[0]["role"] != "system":
            full_messages.insert(
                0, {"role": "system", "content": self._default_system_message}
            )

        return provider.chat_completion(
            messages=full_messages, model=model, **kwargs
        )
    
    def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        provider_name: str = "openrouter",
        model: Optional[str] = None,
        **kwargs,
    ):
        """Create a streaming chat completion using specified provider."""
        provider = self.get_provider(provider_name)
        if not provider:
            raise ValueError(f"Provider '{provider_name}' not found")

        # Prepend system message if not already present
        full_messages = messages.copy()
        if not full_messages or full_messages[0]["role"] != "system":
            full_messages.insert(
                0, {"role": "system", "content": self._default_system_message}
            )

        return provider.chat_completion_stream(
            messages=full_messages, model=model, **kwargs
        )

    def is_provider_available(self, provider_name: str) -> bool:
        """Check if a provider is available."""
        provider = self.get_provider(provider_name)
        return provider.is_connected() if provider else False


# Global provider manager instance
provider_manager = ProviderManager()
