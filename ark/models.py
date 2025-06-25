"""
Data models and type definitions for the Ark application.
"""
from typing import TypedDict, List, Optional, Union




class ChatMessage(TypedDict, total=False):
    role: str
    content: Union[str, List[dict]]
    display_text: str
    citations: List[str]
    generation_time: str
    total_tokens: int
    tokens_per_second: float
    thinking: str


class ProviderConfig(TypedDict):
    base_url: str
    api_key: str
    default_model: Optional[str]