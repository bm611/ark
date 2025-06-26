"""
Chat message model definition.
"""
from typing import TypedDict, List, Union


class ChatMessage(TypedDict, total=False):
    role: str
    content: Union[str, List[dict]]
    display_text: str
    citations: List[str]
    generation_time: str
    total_tokens: int
    tokens_per_second: float
    thinking: str