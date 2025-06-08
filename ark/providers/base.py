"""
Base provider interface and common functionality.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from openai import OpenAI
from ark.models import ProviderConfig


class BaseProvider(ABC):
    """Base class for AI providers."""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.client = OpenAI(
            base_url=config["base_url"],
            api_key=config["api_key"],
        )
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models for this provider."""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if the provider is connected and available."""
        pass
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ):
        """Create a chat completion."""
        model = model or self.config["default_model"]
        
        if model is None:
            raise ValueError(f"Model selection is required for {self.__class__.__name__}")
        
        completion_kwargs = {
            "model": model,
            "messages": messages,
            **kwargs
        }
        
        if tools:
            completion_kwargs["tools"] = tools
            completion_kwargs["tool_choice"] = "auto"
        
        return self.client.chat.completions.create(**completion_kwargs)


class ProviderRegistry:
    """Registry for managing AI providers."""
    
    def __init__(self):
        self._providers = {}
    
    def register(self, name: str, provider: BaseProvider):
        """Register a provider."""
        self._providers[name] = provider
    
    def get(self, name: str) -> Optional[BaseProvider]:
        """Get a provider by name."""
        return self._providers.get(name)
    
    def list_providers(self) -> List[str]:
        """List all registered provider names."""
        return list(self._providers.keys())
    
    def get_available_providers(self) -> List[str]:
        """Get list of providers that are currently available."""
        return [
            name for name, provider in self._providers.items()
            if provider.is_connected()
        ]