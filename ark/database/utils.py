import asyncpg
from dotenv import load_dotenv
import os
from typing import Optional, List, Dict, Any, Union
import json
from datetime import datetime, timezone
import base64
import reflex as rx


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
    conn = None
    try:
        conn = await get_connection()
        
        # First check if the chat exists and belongs to the user
        chat_check = await conn.fetchval(
            """
            SELECT COUNT(*) FROM chats 
            WHERE id = $1::UUID AND user_id = $2
            """,
            chat_id, user_id
        )
        
        if chat_check == 0:
            print(f"Chat {chat_id} not found or does not belong to user {user_id}")
            return False
        
        # Delete the chat - CASCADE will handle messages automatically
        result = await conn.execute(
            """
            DELETE FROM chats 
            WHERE id = $1::UUID AND user_id = $2
            """,
            chat_id, user_id
        )
        
        # Parse the result string (e.g., "DELETE 1" -> 1 row affected)
        rows_affected = int(result.split()[-1]) if result else 0
        success = rows_affected > 0
        
        if success:
            print(f"Successfully deleted chat {chat_id}")
        else:
            print(f"Failed to delete chat {chat_id} - no rows affected")
            
        return success
        
    except Exception as e:
        print(f"Error deleting chat {chat_id}: {e}")
        return False
    finally:
        if conn:
            await conn.close()


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
    success = await save_message(
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
    
    # If message has files and this is a user message, handle R2 metadata saving
    if success and message_dict.get("files") and message_dict.get("role") == "user":
        try:
            user_id = message_dict.get("user_id")
            if user_id:
                # Separate R2 files (already uploaded) from legacy files (need upload)
                r2_files = [f for f in message_dict.get("files", []) if f.get("file_key")]
                legacy_files = [f for f in message_dict.get("files", []) if not f.get("file_key") and f.get("filename")]
                
                # Save metadata for R2 files that are already uploaded
                if r2_files:
                    await _save_r2_file_metadata(chat_id, r2_files, user_id)
                
                # Upload legacy files to R2 (fallback case)
                if legacy_files:
                    await _upload_files_to_r2_and_save(chat_id, legacy_files, user_id)
                    
        except Exception as e:
            print(f"Error handling file metadata: {e}")
            # Don't fail the entire operation for file upload errors
    
    return success


async def _save_r2_file_metadata(chat_id: str, r2_files: List[Dict[str, Any]], user_id: str):
    """
    Save metadata for R2 files that are already uploaded
    
    Args:
        chat_id: The chat ID to associate files with
        r2_files: List of R2 FileReference dicts with file_key, original_filename, etc.
        user_id: The user ID for file organization
    """
    from ark.database.file_utils import store_file_metadata
    
    conn = await get_connection()
    try:
        for file_ref in r2_files:
            if file_ref.get("file_key"):
                # Convert FileReference to metadata format for database
                r2_metadata = {
                    'file_key': file_ref['file_key'],
                    'original_filename': file_ref.get('original_filename', 'unknown'),
                    'content_type': file_ref.get('content_type', 'application/octet-stream'),
                    'file_size': file_ref.get('file_size', 0),
                    'user_id': user_id
                }
                
                file_id = await store_file_metadata(conn, r2_metadata, chat_id)
                if file_id:
                    print(f"Saved R2 file metadata: {file_ref.get('original_filename')}")
                else:
                    print(f"Failed to save metadata for R2 file: {file_ref.get('original_filename')}")
    finally:
        await conn.close()


async def _upload_files_to_r2_and_save(chat_id: str, files_metadata: List[Dict[str, Any]], user_id: str):
    """
    Upload files from local storage to R2 and save metadata to database
    
    Args:
        chat_id: The chat ID to associate files with
        files_metadata: List of file metadata dicts with filename, content_type, type
        user_id: The user ID for file organization
    """
    from ark.services.r2_storage import upload_file, generate_presigned_url
    from ark.database.file_utils import store_file_metadata
    
    conn = await get_connection()
    try:
        upload_dir = rx.get_upload_dir()
        
        for file_meta in files_metadata:
            filename = file_meta.get("filename")
            content_type = file_meta.get("content_type", "application/octet-stream")
            
            # Skip if filename is None or empty
            if not filename:
                print(f"Invalid filename in file metadata, skipping R2 upload: {file_meta}")
                continue
            
            # Read file from local storage
            file_path = upload_dir / filename
            if not file_path.exists():
                print(f"File {filename} not found in local storage, skipping R2 upload")
                continue
                
            try:
                with open(file_path, "rb") as f:
                    file_content = f.read()
                
                # Upload to R2
                r2_metadata = upload_file(
                    file_path=filename,
                    file_content=file_content,
                    content_type=content_type,
                    user_id=user_id
                )
                
                if r2_metadata:
                    # Store metadata in database
                    r2_metadata['user_id'] = user_id
                    file_id = await store_file_metadata(conn, r2_metadata, chat_id)
                    
                    if file_id:
                        print(f"Successfully uploaded {filename} to R2 and saved metadata")
                    else:
                        print(f"Failed to save metadata for {filename}")
                else:
                    print(f"Failed to upload {filename} to R2")
                    
                # Clean up local file after successful R2 upload
                if r2_metadata:
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Could not remove local file {filename}: {e}")
                        
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                
    finally:
        await conn.close()


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
