#!/usr/bin/env python3
"""
Test script for message database functions
"""
import asyncio
import uuid
from utils import (
    # Chat functions
    create_chat, 
    init_user_if_not_exists,
    delete_chat,
    # Message functions
    save_message,
    save_message_from_dict,
    get_chat_messages,
    save_all_messages,
    get_message_count,
    delete_message
)


async def test_message_functions():
    """Test all the message database functions"""
    print("🧪 Testing message database functions...")
    
    # Test data
    test_user_id = "test_user_msg_123"
    test_chat_id = str(uuid.uuid4())
    test_first_name = "Test User"
    
    try:
        # Setup: Create user and chat
        print("\n📝 Setting up test data...")
        await init_user_if_not_exists(test_user_id, test_first_name)
        await create_chat(
            chat_id=test_chat_id,
            user_id=test_user_id,
            title="Test Chat for Messages",
        )
        print(f"✅ Created test chat: {test_chat_id}")
        
        # 1. Test saving individual messages
        print("\n1. Testing save_message...")
        
        # Save user message
        user_success = await save_message(
            chat_id=test_chat_id,
            message_order=0,
            role="user",
            content="Hello, this is a test message",
            display_text="Hello, this is a test message"
        )
        print(f"✅ User message saved: {user_success}")
        
        # Save assistant message with all metadata
        assistant_success = await save_message(
            chat_id=test_chat_id,
            message_order=1,
            role="assistant",
            content="Hello! How can I help you today?",
            display_text="Hello! How can I help you today?",
            thinking="The user is greeting me, I should respond politely",
            citations=["source1.com", "source2.com"],
            generation_time="1.2s",
            total_tokens=150,
            tokens_per_second=125.0,
            tool_name="search",
            tool_args="query='test'",
            weather_location="New York"
        )
        print(f"✅ Assistant message saved: {assistant_success}")
        
        # 2. Test getting messages
        print("\n2. Testing get_chat_messages...")
        messages = await get_chat_messages(test_chat_id)
        print(f"✅ Retrieved {len(messages)} messages")
        
        if messages:
            for i, msg in enumerate(messages):
                print(f"   Message {i}: {msg['role']} - {msg['display_text'][:50]}...")
                if msg['citations']:
                    print(f"      Citations: {msg['citations']}")
                if msg['thinking']:
                    print(f"      Thinking: {msg['thinking'][:50]}...")
        
        # 3. Test message count
        print("\n3. Testing get_message_count...")
        count = await get_message_count(test_chat_id)
        print(f"✅ Message count: {count}")
        
        # 4. Test save_message_from_dict
        print("\n4. Testing save_message_from_dict...")
        message_dict = {
            "role": "user",
            "content": [{"type": "text", "text": "This is a multimodal message"}],
            "display_text": "This is a multimodal message",
            "citations": [],
            "total_tokens": 50
        }
        dict_success = await save_message_from_dict(test_chat_id, 2, message_dict)
        print(f"✅ Message from dict saved: {dict_success}")
        
        # 5. Test batch save
        print("\n5. Testing save_all_messages...")
        batch_messages = [
            {
                "role": "user",
                "content": "First batch message",
                "display_text": "First batch message"
            },
            {
                "role": "assistant", 
                "content": "First batch response",
                "display_text": "First batch response",
                "thinking": "Responding to batch message"
            }
        ]
        # Note: This will save as message orders 3 and 4
        batch_success = await save_all_messages(test_chat_id, batch_messages)
        print(f"✅ Batch messages saved: {batch_success}")
        
        # 6. Test final message retrieval
        print("\n6. Testing final message retrieval...")
        final_messages = await get_chat_messages(test_chat_id)
        print(f"✅ Total messages now: {len(final_messages)}")
        
        # 7. Test message deletion
        print("\n7. Testing delete_message...")
        delete_success = await delete_message(test_chat_id, 2)  # Delete the multimodal message
        print(f"✅ Message deleted: {delete_success}")
        
        # Verify deletion
        after_delete = await get_chat_messages(test_chat_id)
        print(f"✅ Messages after deletion: {len(after_delete)}")
        
        # Cleanup
        print("\n🧹 Cleaning up...")
        cleanup_success = await delete_chat(test_chat_id, test_user_id)
        print(f"✅ Cleanup successful: {cleanup_success}")
        
        print("\n🎉 All message tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_message_functions())
