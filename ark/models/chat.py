"""
Chat message model definition.
"""
from typing import TypedDict, List, Union, Optional


class FileReference(TypedDict, total=False):
    """Reference to a file stored in R2 or base64 data"""
    file_id: Optional[str]
    file_key: Optional[str] 
    original_filename: Optional[str]
    filename: Optional[str]  # For base64 files
    content_type: str
    file_size: Optional[int]
    type: Optional[str]  # "image" or "pdf"
    presigned_url: Optional[str]  # For R2 files
    base64_url: Optional[str]  # For base64 files


class ChatMessage(TypedDict, total=False):
    role: str
    content: Union[str, List[dict]]
    display_text: str
    citations: List[str]
    generation_time: str
    total_tokens: int
    tokens_per_second: float
    thinking: str
    files: List[FileReference]  # File references instead of embedded base64