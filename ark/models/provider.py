"""
Provider configuration model definition.
"""
from typing import TypedDict, Optional


class ProviderConfig(TypedDict):
    base_url: str
    api_key: str
    default_model: Optional[str]