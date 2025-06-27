import asyncpg
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")


async def test_connection():
    conn = await asyncpg.connect(DB_URL)
    
    # Create users table first (referenced by chats)
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY, -- Clerk user_id
            first_name VARCHAR(255),
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
        """
    )
    print("Users Table Created")
    
    # Create chats table
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id UUID PRIMARY KEY, -- This corresponds to your state's `chat_id`
            user_id VARCHAR(255) NOT NULL, -- Foreign key to the user who initiated the chat
            title VARCHAR(255) NOT NULL, -- A title for the chat (e.g., the first user prompt)
            initial_provider VARCHAR(50), -- The provider used when the chat started (e.g., 'openrouter')
            initial_model VARCHAR(100), -- The model used when the chat started
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(), -- Useful for ordering the user's chat list
            
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    print("Chat Table Created")
    
    # Create messages table
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY, -- Auto-incrementing primary key for each message
            chat_id UUID NOT NULL, -- Foreign key to the chat this message belongs to
            message_order INT NOT NULL, -- To preserve the exact order of conversation (e.g., 0, 1, 2, ...)

            -- Core message content
            role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
            content JSONB NOT NULL, -- Stores the flexible content array: [{"type": "text", ...}, {"type": "image_url", ...}]
            display_text TEXT, -- The main text content for easy display without parsing JSON

            -- Assistant-specific metadata (nullable)
            thinking TEXT,
            citations JSONB, -- Storing the list of citation dictionaries
            generation_time VARCHAR(20),
            total_tokens INT,
            tokens_per_second REAL,


            created_at TIMESTAMPTZ DEFAULT NOW(),

            FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
            UNIQUE (chat_id, message_order) -- Ensures message order is unique within a chat
        )
        """
    )
    print("Messages Table Created")
    
    # Create files table for R2 storage references
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            file_key VARCHAR(500) NOT NULL UNIQUE, -- R2 object key
            original_filename VARCHAR(255) NOT NULL,
            content_type VARCHAR(100) NOT NULL,
            file_size BIGINT NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            chat_id UUID, -- Optional: link to specific chat
            created_at TIMESTAMPTZ DEFAULT NOW(),
            
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
        )
        """
    )
    print("Files Table Created")
    
    # Create indexes for performance
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_chats_on_user_id ON chats (user_id)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_on_chat_id_and_order ON messages (chat_id, message_order)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_files_on_user_id ON files (user_id)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_files_on_chat_id ON files (chat_id)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_files_on_file_key ON files (file_key)")
    print("Indexes Created")
    
    await conn.close()


if __name__ == "__main__":
    asyncio.run(test_connection())
