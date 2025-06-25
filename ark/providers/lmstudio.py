"""
LM Studio provider implementation.
"""
from typing import List
from ark.models.provider import ProviderConfig
from .base import BaseProvider


class LMStudioProvider(BaseProvider):
    """LM Studio local AI provider."""
    
    def __init__(self):
        config: ProviderConfig = {
            "base_url": "http://localhost:1234/v1",
            "api_key": "lmstudio",
            "default_model": None,
        }
        super().__init__(config)
    
    def get_available_models(self) -> List[str]:
        """Get available LM Studio models."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            print(f"Error fetching LM Studio models: {e}")
            return []
    
    def is_connected(self) -> bool:
        """Check if LM Studio is available."""
        try:
            self.client.models.list()
            return True
        except Exception:
            return False
    
    def supports_tools(self, model: str) -> bool:
        """Check if a model supports tool calling."""
        # Most LM Studio models support tools, but this could be more specific
        return True