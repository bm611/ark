import asyncpg
from dotenv import load_dotenv
import os
from typing import Optional, List, Dict, Any, Union
import json
from datetime import datetime, timezone


load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")


def format_time_ago(timestamp):
    """
    Convert timestamp to human readable format like '2 hours ago', '3 days ago'
    
    Args:
        timestamp: datetime object with timezone info
        
    Returns:
        str: Human readable time format
    """
    if not timestamp:
        return "unknown"
    
    now = datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    
    diff = now - timestamp
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:  # less than 1 hour
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:  # less than 1 day
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:  # less than 1 week
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2419200:  # less than 4 weeks
        weeks = int(seconds // 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        months = int(seconds // 2419200)
        return f"{months} month{'s' if months != 1 else ''} ago"


async def get_connection():
    """Get database connection"""
    return await asyncpg.connect(DB_URL)


# CHAT FUNCTIONS

async def create_chat(
    chat_id: str,
    user_id: str,
    title: str,
    initial_provider: str = "openrouter",
    initial_model: str = "google/gemini-2.5-flash"
) -> bool:
    """
    Create a new chat record in the database
    
    Args:
        chat_id: UUID string for the chat
        user_id: User ID from Clerk authentication 
        title: Chat title (typically from first user message)
        initial_provider: Provider used when chat started
        initial_model: Model used when chat started
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = await get_connection()
        await conn.execute(
            """
            INSERT INTO chats (id, user_id, title, initial_provider, initial_model, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
            """,
            chat_id, user_id, title, initial_provider, initial_model
        )
        await conn.close()
        return True
    except Exception as e:
        print(f"Error creating chat: {e}")
        return False


async def get_chat(chat_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific chat by ID
    
    Args:
        chat_id: UUID string for the chat
        
    Returns:
        Dict with chat data or None if not found
    """
    try:
        conn = await get_connection()
        row = await conn.fetchrow(
            """
            SELECT id, user_id, title, initial_provider, initial_model, created_at, updated_at
            FROM chats 
            WHERE id = $1
            """,
            chat_id
        )
        await conn.close()
        
        if row:
            return dict(row)
        return None
    except Exception as e:
        print(f"Error fetching chat: {e}")
        return None


async def get_user_chats(user_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Get all chats for a specific user, ordered by most recent first
    
    Args:
        user_id: User ID from Clerk authentication
        limit: Maximum number of chats to return
        offset: Number of chats to skip (for pagination)
        
    Returns:
        List of chat dictionaries
    """
    try:
        conn = await get_connection()
        rows = await conn.fetch(
            """
            SELECT id, user_id, title, initial_provider, initial_model, created_at, updated_at
            FROM chats 
            WHERE user_id = $1
            ORDER BY updated_at DESC
            LIMIT $2 OFFSET $3
            """,
            user_id, limit, offset
        )
        await conn.close()
        
        chats = []
        for row in rows:
            chat = dict(row)
            chat['updated_at'] = format_time_ago(chat['updated_at'])
            chats.append(chat)
        
        return chats
    except Exception as e:
        print(f"Error fetching user chats: {e}")
        return []


async def update_chat_title(chat_id: str, title: str) -> bool:
    """
    Update the title of a chat
    
    Args:
        chat_id: UUID string for the chat
        title: New title for the chat
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = await get_connection()
        result = await conn.execute(
            """
            UPDATE chats 
            SET title = $1, updated_at = NOW()
            WHERE id = $2
            """,
            title, chat_id
        )
        await conn.close()
        
        # Check if any row was updated
        return result.split()[-1] == "1"
    except Exception as e:
        print(f"Error updating chat title: {e}")
        return False


async def update_chat_timestamp(chat_id: str) -> bool:
    """
    Update the updated_at timestamp for a chat (called when new messages are added)
    
    Args:
        chat_id: UUID string for the chat
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = await get_connection()
        result = await conn.execute(
            """
            UPDATE chats 
            SET updated_at = NOW()
            WHERE id = $1
            """,
            chat_id
        )
        await conn.close()
        
        return result.split()[-1] == "1"
    except Exception as e:
        print(f"Error updating chat timestamp: {e}")
        return False


async def delete_chat(chat_id: str, user_id: str) -> bool:
    """
    Delete a chat (with user verification for security)
    
    Args:
        chat_id: UUID string for the chat
        user_id: User ID to verify ownership
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = await get_connection()
        result = await conn.execute(
            """
            DELETE FROM chats 
            WHERE id = $1 AND user_id = $2
            """,
            chat_id, user_id
        )
        await conn.close()
        
        return result.split()[-1] == "1"
    except Exception as e:
        print(f"Error deleting chat: {e}")
        return False


async def chat_exists(chat_id: str, user_id: str) -> bool:
    """
    Check if a chat exists and belongs to the specified user
    
    Args:
        chat_id: UUID string for the chat
        user_id: User ID to verify ownership
        
    Returns:
        bool: True if chat exists and belongs to user, False otherwise
    """
    try:
        conn = await get_connection()
        row = await conn.fetchrow(
            """
            SELECT 1 FROM chats 
            WHERE id = $1 AND user_id = $2
            """,
            chat_id, user_id
        )
        await conn.close()
        
        return row is not None
    except Exception as e:
        print(f"Error checking chat existence: {e}")
        return False


# UTILITY FUNCTIONS

async def init_user_if_not_exists(user_id: str, first_name: str = "") -> bool:
    """
    Create a user record if it doesn't exist (for Clerk integration)
    
    Args:
        user_id: User ID from Clerk
        first_name: User's first name
        
    Returns:
        bool: True if user exists or was created successfully
    """
    try:
        conn = await get_connection()
        
        # Check if user exists
        exists = await conn.fetchrow(
            "SELECT 1 FROM users WHERE id = $1",
            user_id
        )
        
        if not exists:
            # Create users table if it doesn't exist
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(255) PRIMARY KEY,
                    first_name VARCHAR(255),
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )
            
            # Insert new user
            await conn.execute(
                """
                INSERT INTO users (id, first_name, created_at)
                VALUES ($1, $2, NOW())
                """,
                user_id, first_name
            )
        
        await conn.close()
        return True
    except Exception as e:
        print(f"Error initializing user: {e}")
        return False


# MESSAGE FUNCTIONS

async def save_message(
    chat_id: str,
    message_order: int,
    role: str,
    content: Union[str, List[Dict]],
    display_text: str = "",
    thinking: str = "",
    citations: Optional[List[str]] = None,
    generation_time: str = "",
    total_tokens: int = 0,
    tokens_per_second: float = 0.0
) -> bool:
    """
    Save a message to the database
    
    Args:
        chat_id: UUID string for the chat
        message_order: Order of the message in the conversation
        role: 'user' or 'assistant'
        content: Message content (string or list of dicts for multimodal)
        display_text: Text to display (extracted from content)
        thinking: Assistant's thinking process
        citations: List of citations
        generation_time: Time taken to generate response
        total_tokens: Number of tokens used
        tokens_per_second: Generation speed
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = await get_connection()
        
        # Convert content to JSON if it's a list
        content_json = json.dumps(content) if isinstance(content, list) else json.dumps([{"type": "text", "text": content}])
        citations_json = json.dumps(citations) if citations else None
        
        await conn.execute(
            """
            INSERT INTO messages (
                chat_id, message_order, role, content, display_text,
                thinking, citations, generation_time, total_tokens, tokens_per_second, created_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, NOW())
            """,
            chat_id, message_order, role, content_json, display_text,
            thinking or None, citations_json, generation_time or None, 
            total_tokens if total_tokens > 0 else None, 
            tokens_per_second if tokens_per_second > 0 else None
        )
        
        # Update chat timestamp
        await conn.execute(
            "UPDATE chats SET updated_at = NOW() WHERE id = $1",
            chat_id
        )
        
        await conn.close()
        return True
    except Exception as e:
        print(f"Error saving message: {e}")
        return False


async def save_message_from_dict(chat_id: str, message_order: int, message_dict: Dict[str, Any]) -> bool:
    """
    Save a message from a ChatMessage dictionary (convenient wrapper)
    
    Args:
        chat_id: UUID string for the chat
        message_order: Order of the message in the conversation
        message_dict: ChatMessage dictionary from your state
        
    Returns:
        bool: True if successful, False otherwise
    """
    return await save_message(
        chat_id=chat_id,
        message_order=message_order,
        role=message_dict.get("role", ""),
        content=message_dict.get("content", ""),
        display_text=message_dict.get("display_text", ""),
        thinking=message_dict.get("thinking", ""),
        citations=message_dict.get("citations", []),
        generation_time=message_dict.get("generation_time", ""),
        total_tokens=message_dict.get("total_tokens", 0),
        tokens_per_second=message_dict.get("tokens_per_second", 0.0)
    )


async def get_chat_messages(chat_id: str) -> List[Dict[str, Any]]:
    """
    Get all messages for a specific chat, ordered by message_order
    
    Args:
        chat_id: UUID string for the chat
        
    Returns:
        List of message dictionaries in order
    """
    try:
        conn = await get_connection()
        rows = await conn.fetch(
            """
            SELECT id, chat_id, message_order, role, content, display_text,
                   thinking, citations, generation_time, total_tokens, tokens_per_second, created_at
            FROM messages 
            WHERE chat_id = $1
            ORDER BY message_order ASC
            """,
            chat_id
        )
        await conn.close()
        
        messages = []
        for row in rows:
            message = dict(row)
            # Parse JSON fields back to Python objects
            message['content'] = json.loads(message['content']) if message['content'] else []
            message['citations'] = json.loads(message['citations']) if message['citations'] else []
            messages.append(message)
        
        return messages
    except Exception as e:
        print(f"Error fetching chat messages: {e}")
        return []


async def save_all_messages(chat_id: str, messages: List[Dict[str, Any]], start_order: int = 0) -> bool:
    """
    Save all messages from a conversation (batch operation)
    
    Args:
        chat_id: UUID string for the chat
        messages: List of ChatMessage dictionaries
        start_order: Starting message order number (default: 0)
        
    Returns:
        bool: True if all successful, False otherwise
    """
    try:
        success_count = 0
        for i, message in enumerate(messages):
            success = await save_message_from_dict(chat_id, start_order + i, message)
            if success:
                success_count += 1
        
        return success_count == len(messages)
    except Exception as e:
        print(f"Error saving all messages: {e}")
        return False


async def delete_message(chat_id: str, message_order: int) -> bool:
    """
    Delete a specific message from a chat
    
    Args:
        chat_id: UUID string for the chat
        message_order: Order of the message to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = await get_connection()
        result = await conn.execute(
            """
            DELETE FROM messages 
            WHERE chat_id = $1 AND message_order = $2
            """,
            chat_id, message_order
        )
        await conn.close()
        
        return result.split()[-1] == "1"
    except Exception as e:
        print(f"Error deleting message: {e}")
        return False


async def get_message_count(chat_id: str) -> int:
    """
    Get the number of messages in a chat
    
    Args:
        chat_id: UUID string for the chat
        
    Returns:
        int: Number of messages
    """
    try:
        conn = await get_connection()
        count = await conn.fetchval(
            "SELECT COUNT(*) FROM messages WHERE chat_id = $1",
            chat_id
        )
        await conn.close()
        
        return count or 0
    except Exception as e:
        print(f"Error getting message count: {e}")
        return 0


async def get_next_message_order(chat_id: str) -> int:
    """
    Get the next message order number for a chat
    
    Args:
        chat_id: UUID string for the chat
        
    Returns:
        int: Next message order number
    """
    try:
        conn = await get_connection()
        max_order = await conn.fetchval(
            "SELECT COALESCE(MAX(message_order), -1) + 1 FROM messages WHERE chat_id = $1",
            chat_id
        )
        await conn.close()
        
        return max_order or 0
    except Exception as e:
        print(f"Error getting next message order: {e}")
        return 0


async def save_message_auto_order(chat_id: str, message_dict: Dict[str, Any]) -> bool:
    """
    Save a message with automatic order assignment
    
    Args:
        chat_id: UUID string for the chat
        message_dict: ChatMessage dictionary from your state
        
    Returns:
        bool: True if successful, False otherwise
    """
    next_order = await get_next_message_order(chat_id)
    return await save_message_from_dict(chat_id, next_order, message_dict)
