import asyncpg
import logging
from uuid import UUID
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


async def store_file_metadata(
    conn: asyncpg.Connection, file_data: Dict[str, Any], chat_id: Optional[UUID] = None
) -> Optional[UUID]:
    """
    Store file metadata in the database

    Args:
        conn: Database connection
        file_data: File metadata from R2 upload
        chat_id: Optional chat ID to associate file with

    Returns:
        File UUID if successful, None otherwise
    """
    try:
        file_id = await conn.fetchval(
            """
            INSERT INTO files (file_key, original_filename, content_type, file_size, user_id, chat_id)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
            """,
            file_data["file_key"],
            file_data["original_filename"],
            file_data["content_type"],
            file_data.get("file_size", file_data.get("size", 0)),
            file_data.get("user_id"),
            chat_id,
        )
        return file_id
    except Exception as e:
        logger.error(f"Error storing file metadata: {e}")
        return None


async def get_chat_files(
    conn: asyncpg.Connection, chat_id: UUID
) -> List[Dict[str, Any]]:
    """
    Get all files associated with a chat

    Args:
        conn: Database connection
        chat_id: Chat UUID

    Returns:
        List of file metadata dictionaries
    """
    try:
        rows = await conn.fetch(
            """
            SELECT id, file_key, original_filename, content_type, file_size, created_at
            FROM files
            WHERE chat_id = $1
            ORDER BY created_at ASC
            """,
            chat_id,
        )
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error fetching chat files: {e}")
        return []


async def get_file_by_id(
    conn: asyncpg.Connection, file_id: UUID
) -> Optional[Dict[str, Any]]:
    """
    Get file metadata by file ID

    Args:
        conn: Database connection
        file_id: File UUID

    Returns:
        File metadata dictionary or None
    """
    try:
        row = await conn.fetchrow(
            """
            SELECT id, file_key, original_filename, content_type, file_size, user_id, chat_id, created_at
            FROM files
            WHERE id = $1
            """,
            file_id,
        )
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error fetching file by ID: {e}")
        return None


async def delete_file_metadata(conn: asyncpg.Connection, file_id: UUID) -> bool:
    """
    Delete file metadata from database

    Args:
        conn: Database connection
        file_id: File UUID

    Returns:
        True if successful, False otherwise
    """
    try:
        await conn.execute("DELETE FROM files WHERE id = $1", file_id)
        return True
    except Exception as e:
        logger.error(f"Error deleting file metadata: {e}")
        return False


async def get_chat_file_keys(conn: asyncpg.Connection, chat_id: UUID) -> List[str]:
    """
    Get all file keys for a chat (for R2 cleanup)

    Args:
        conn: Database connection
        chat_id: Chat UUID

    Returns:
        List of file keys
    """
    try:
        rows = await conn.fetch(
            "SELECT file_key FROM files WHERE chat_id = $1", chat_id
        )
        return [row["file_key"] for row in rows]
    except Exception as e:
        logger.error(f"Error fetching chat file keys: {e}")
        return []


async def get_user_file_keys(conn: asyncpg.Connection, user_id: str) -> List[str]:
    """
    Get all file keys for a user (for R2 cleanup)

    Args:
        conn: Database connection
        user_id: User ID

    Returns:
        List of file keys
    """
    try:
        rows = await conn.fetch(
            "SELECT file_key FROM files WHERE user_id = $1", user_id
        )
        return [row["file_key"] for row in rows]
    except Exception as e:
        logger.error(f"Error fetching user file keys: {e}")
        return []
