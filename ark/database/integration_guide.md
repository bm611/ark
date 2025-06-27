# Chat History Integration Guide

## 🎯 Overview

You now have a complete backend for chat history with the following components:

### Database Tables
- **`users`** - Stores Clerk user information
- **`chats`** - Stores chat sessions with metadata  
- **`messages`** - Stores individual messages with full metadata

### Key Functions Available
- **Chat Functions**: `create_chat`, `get_chat`, `get_user_chats`, `update_chat_title`, `delete_chat`
- **Message Functions**: `save_message_auto_order`, `get_chat_messages`, `save_all_messages`
- **User Functions**: `init_user_if_not_exists`

## 🔧 Integration Steps

### 1. Initialize User on Login

In your `state.py` `handle_auth_change` method:

```python
@rx.event
async def handle_auth_change(self):
    """Handle authentication state changes (login/logout)."""
    from ark.database.utils import init_user_if_not_exists
    
    clerk_state = await self.get_state(clerk.ClerkState)
    clerk_user_state = await self.get_state(clerk.ClerkUser)
    
    if clerk_state.is_signed_in:
        print(f"User signed in: {clerk_state.user_id}")
        print(f"User Name: {clerk_user_state.first_name}")
        self.logged_user_name = clerk_user_state.first_name
        
        # Initialize user in database
        await init_user_if_not_exists(
            clerk_state.user_id, 
            clerk_user_state.first_name or ""
        )
    else:
        print("User signed out")
```

### 2. Create Chat on New Chat

In your `generate_chat_id_and_redirect` method:

```python
async def generate_chat_id_and_redirect(self):
    from ark.database.utils import create_chat
    
    self.chat_id = str(uuid.uuid4())
    
    # Get user ID from Clerk
    clerk_state = await self.get_state(clerk.ClerkState)
    if clerk_state.is_signed_in:
        # Create chat in database
        await create_chat(
            chat_id=self.chat_id,
            user_id=clerk_state.user_id,
            title="New Chat",  # You'll update this with first message
            initial_provider=self.selected_provider,
            initial_model=self.selected_model
        )
    
    return rx.redirect(f"/chat/{self.chat_id}")
```

### 3. Save Messages After Each Exchange

In your `send_message` method, after the message is processed:

```python
def send_message(self):
    """Send message using the new message handler."""
    from ark.database.utils import save_message_auto_order, update_chat_title
    
    # ... existing code ...
    
    # Add the message to the conversation
    self.messages.append(message_dict)
    
    # Save messages to database if chat_id exists
    if self.chat_id:
        # Save all messages that aren't saved yet
        asyncio.create_task(self._save_current_messages())
    
    # Clear uploaded images after sending
    self.img = []

async def _save_current_messages(self):
    """Save current messages to database"""
    from ark.database.utils import save_message_auto_order, update_chat_title, get_message_count
    
    clerk_state = await self.get_state(clerk.ClerkState)
    if not clerk_state.is_signed_in or not self.chat_id:
        return
    
    # Get current message count in DB to know which messages to save
    db_count = await get_message_count(self.chat_id)
    
    # Save any new messages
    for i in range(db_count, len(self.messages)):
        message = self.messages[i]
        await save_message_auto_order(self.chat_id, message)
    
    # Update chat title with first user message if not set
    if len(self.messages) > 0 and self.messages[0].get('role') == 'user':
        first_message = self.messages[0].get('display_text', 'New Chat')[:100]
        await update_chat_title(self.chat_id, first_message)
```

### 4. Load Chat History on Page Load

Add this method to load existing chats:

```python
@rx.event
async def load_chat_history(self, chat_id: str):
    """Load chat history from database"""
    from ark.database.utils import get_chat_messages, chat_exists
    
    clerk_state = await self.get_state(clerk.ClerkState)
    if not clerk_state.is_signed_in:
        return
    
    # Verify user owns this chat
    if await chat_exists(chat_id, clerk_state.user_id):
        # Load messages
        db_messages = await get_chat_messages(chat_id)
        
        # Convert database messages to your ChatMessage format
        self.messages = []
        for msg in db_messages:
            chat_message = {
                "role": msg["role"],
                "content": msg["content"],
                "display_text": msg["display_text"]
            }
            
            # Add optional fields if they exist
            if msg.get("thinking"):
                chat_message["thinking"] = msg["thinking"]
            if msg.get("citations"):
                chat_message["citations"] = msg["citations"]
            if msg.get("generation_time"):
                chat_message["generation_time"] = msg["generation_time"]
            if msg.get("total_tokens"):
                chat_message["total_tokens"] = msg["total_tokens"]
            if msg.get("tokens_per_second"):
                chat_message["tokens_per_second"] = msg["tokens_per_second"]
            if msg.get("tool_name"):
                chat_message["tool_name"] = msg["tool_name"]
            if msg.get("tool_args"):
                chat_message["tool_args"] = msg["tool_args"]
            if msg.get("weather_data"):
                chat_message["weather_data"] = msg["weather_data"]
            if msg.get("weather_location"):
                chat_message["weather_location"] = msg["weather_location"]
                
            self.messages.append(chat_message)
        
        self.chat_id = chat_id
```

### 5. Save Chat History on "New Chat" Click

In your `reset_chat` method, save the current conversation before clearing:

```python
async def reset_chat(self):
    """Reset chat and save current conversation"""
    from ark.database.utils import save_all_messages
    
    # Save current conversation if it exists and has messages
    if self.chat_id and self.messages:
        clerk_state = await self.get_state(clerk.ClerkState)
        if clerk_state.is_signed_in:
            await save_all_messages(self.chat_id, self.messages)
    
    # Save to log file (existing functionality)
    save_messages_to_log(self.messages)
    
    # Clear state
    self.messages = []
    self.is_gen = False
    self.selected_provider = ModelConfig.DEFAULT_PROVIDER
    self.selected_model = ModelConfig.CHAT_MODEL
    self.selected_action = ""
    self.thinking_expanded = {}
    self.citations_expanded = {}
    self.tool_expanded = {}
    self.weather_data = None
    self.weather_location = ""
    self.chat_id = ""
```

### 6. Get User's Chat List

Add this method to get a user's chat history:

```python
@rx.event
async def get_user_chat_list(self):
    """Get list of user's chats for sidebar/navigation"""
    from ark.database.utils import get_user_chats
    
    clerk_state = await self.get_state(clerk.ClerkState)
    if not clerk_state.is_signed_in:
        return []
    
    chats = await get_user_chats(clerk_state.user_id, limit=50)
    return chats
```

## 🚀 Usage Examples

### Loading a specific chat
```python
# In your page component for /chat/{chat_id}
@rx.page(route="/chat/[chat_id]", on_load=State.load_chat_history)
def chat_page():
    return rx.container(
        # Your chat UI components
    )
```

### Displaying chat history in sidebar
```python
def chat_sidebar():
    return rx.vstack(
        rx.foreach(
            State.get_user_chat_list,
            lambda chat: rx.link(
                chat["title"],
                href=f"/chat/{chat['id']}"
            )
        )
    )
```

## 🎯 Next Steps

1. **Test the integration** - Start with the user initialization
2. **Add error handling** - Wrap database calls in try/catch
3. **Add loading states** - Show spinners while loading chat history
4. **Implement chat deletion** - Add UI to delete old chats
5. **Add search functionality** - Search through chat history

## 📝 Database Schema Summary

```sql
-- Users table (links to Clerk)
users (id, first_name, created_at)

-- Chats table (chat sessions)
chats (id, user_id, title, initial_provider, initial_model, created_at, updated_at)

-- Messages table (individual messages)
messages (id, chat_id, message_order, role, content, display_text, thinking, 
         citations, generation_time, total_tokens, tokens_per_second, 
         tool_name, tool_args, weather_data, weather_location, created_at)
```

All functions are tested and ready to use! 🎉
