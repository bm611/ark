#!/usr/bin/env python3
"""
Test script for database utility functions
"""
import asyncio
import uuid
from utils import (
    create_chat, 
    get_chat, 
    get_user_chats, 
    update_chat_title,
    delete_chat,
    chat_exists,
    init_user_if_not_exists
)


async def test_database_functions():
    """Test all the database functions"""
    print("🧪 Testing database functions...")
    
    # Test data
    test_user_id = "test_user_123"
    test_chat_id = str(uuid.uuid4())
    test_first_name = "Test User"
    
    try:
        # 1. Test user initialization
        print("\n1. Testing user initialization...")
        success = await init_user_if_not_exists(test_user_id, test_first_name)
        print(f"✅ User init: {success}")
        
        # 2. Test chat creation
        print("\n2. Testing chat creation...")
        success = await create_chat(
            chat_id=test_chat_id,
            user_id=test_user_id,
            title="Test Chat Title",
            initial_provider="openrouter",
            initial_model="google/gemini-2.5-flash"
        )
        print(f"✅ Chat created: {success}")
        
        # 3. Test chat retrieval
        print("\n3. Testing chat retrieval...")
        chat = await get_chat(test_chat_id)
        print(f"✅ Chat retrieved: {chat is not None}")
        if chat:
            print(f"   Title: {chat['title']}")
            print(f"   User ID: {chat['user_id']}")
            print(f"   Provider: {chat['initial_provider']}")
        
        # 4. Test chat existence check
        print("\n4. Testing chat existence...")
        exists = await chat_exists(test_chat_id, test_user_id)
        print(f"✅ Chat exists: {exists}")
        
        # 5. Test getting user chats
        print("\n5. Testing user chats retrieval...")
        user_chats = await get_user_chats(test_user_id)
        print(f"✅ User chats count: {len(user_chats)}")
        
        # 6. Test chat title update
        print("\n6. Testing chat title update...")
        success = await update_chat_title(test_chat_id, "Updated Test Title")
        print(f"✅ Title updated: {success}")
        
        # Verify the update
        updated_chat = await get_chat(test_chat_id)
        if updated_chat:
            print(f"   New title: {updated_chat['title']}")
        
        # 7. Test chat deletion
        print("\n7. Testing chat deletion...")
        success = await delete_chat(test_chat_id, test_user_id)
        print(f"✅ Chat deleted: {success}")
        
        # Verify deletion
        deleted_chat = await get_chat(test_chat_id)
        print(f"✅ Chat no longer exists: {deleted_chat is None}")
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")


if __name__ == "__main__":
    asyncio.run(test_database_functions())
