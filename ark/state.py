import reflex as rx
from typing import List, Optional
from ark.models import WeatherData, ChatMessage
from ark.handlers.message_handler import message_handler
import reflex_clerk_api as clerk
import base64
import os
import uuid
from ark.db.utils import init_user_if_not_exists


# Model Configuration Constants
class ModelConfig:
    DEFAULT_PROVIDER = "openrouter"
    CHAT_MODEL = "google/gemini-2.5-flash"
    SEARCH_MODEL = "perplexity/sonar-pro"


class State(rx.State):
    prompt: str = ""
    messages: List[ChatMessage] = []
    is_gen: bool = False
    selected_action: str = ""
    is_tool_use: bool = False
    img: list[str] = []
    logged_user_name: str = ""
    chat_id: str = ""
    user_chats: List[dict] = []
    _saving_messages: bool = False

    # Thinking section expansion state
    thinking_expanded: dict[int, bool] = {}
    # Citations section expansion state
    citations_expanded: dict[int, bool] = {}
    # Tool section expansion state
    tool_expanded: dict[int, bool] = {}

    # Provider and model selection
    selected_provider: str = ModelConfig.DEFAULT_PROVIDER
    selected_model: str = ModelConfig.CHAT_MODEL

    # Weather-related state variables
    weather_data: Optional[WeatherData] = None
    weather_location: str = ""

    # Theme state
    is_dark_theme: bool = False

    async def generate_chat_id_and_redirect(self):
        from ark.db.utils import create_chat
        
        self.chat_id = str(uuid.uuid4())
        
        # Get user ID from Clerk
        clerk_state = await self.get_state(clerk.ClerkState)
        if clerk_state.is_signed_in:
            # Create chat in database
            await create_chat(
                chat_id=self.chat_id,
                user_id=clerk_state.user_id,
                title="New Chat",  # Will be updated with first message
                initial_provider=self.selected_provider,
                initial_model=self.selected_model
            )
        
        return rx.redirect(f"/chat/{self.chat_id}")

    @rx.var
    def current_url(self) -> str:
        return self.router.page.path

    def set_prompt(self, value: str):
        self.prompt = value

    def set_provider_and_model(self, provider: str, model: str = ""):
        """Set the selected provider and model from offline models selection"""
        self.selected_provider = provider
        self.selected_model = model
        print(f"Provider set to: {provider}, Model: {model or 'default'}")

    def handle_generation(self):
        self.is_gen = True

        # Create content array starting with text
        content = [{"type": "text", "text": self.prompt}]

        # Add base64 images if any are uploaded
        if self.img:
            base64_images = self.base64_imgs
            for image_data_url in base64_images:
                content.append(
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                )

        # Create user message
        user_message = {"role": "user", "content": content, "display_text": self.prompt}
        self.messages.append(user_message)
        self.prompt = ""

    async def reset_chat(self):
        """Reset chat and save current conversation"""
        from ark.db.utils import save_all_messages
        
        # Save current conversation if it exists and has messages
        if self.chat_id and self.messages:
            clerk_state = await self.get_state(clerk.ClerkState)
            if clerk_state.is_signed_in:
                await save_all_messages(self.chat_id, self.messages)
        
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

    def toggle_thinking(self, message_index: int):
        """Toggle the thinking section for a specific message"""
        if message_index in self.thinking_expanded:
            self.thinking_expanded[message_index] = not self.thinking_expanded[
                message_index
            ]
        else:
            self.thinking_expanded[message_index] = True

    def toggle_citations(self, message_index: int):
        """Toggle the citations section for a specific message"""
        if message_index in self.citations_expanded:
            self.citations_expanded[message_index] = not self.citations_expanded[
                message_index
            ]
        else:
            self.citations_expanded[message_index] = True

    def toggle_tool(self, message_index: int):
        """Toggle the tool section for a specific message"""
        if message_index in self.tool_expanded:
            self.tool_expanded[message_index] = not self.tool_expanded[message_index]
        else:
            self.tool_expanded[message_index] = True

    def send_message(self):
        """Send message using the new message handler."""
        # Determine model based on action and selection
        model = self._get_model_for_action()

        # Process the message
        message_dict, new_weather_data, new_weather_location = (
            message_handler.process_message(
                messages=self.messages,
                provider=self.selected_provider,
                model=model,
                action=self.selected_action,
                weather_data=self.weather_data,
                weather_location=self.weather_location,
            )
        )

        # Update state
        self.is_gen = False
        self.is_tool_use = bool(message_dict.get("tool_name"))

        if new_weather_data:
            self.weather_data = new_weather_data
            self.weather_location = new_weather_location

        # Add the message to the conversation
        self.messages.append(message_dict)

        # Save messages to database if chat_id exists
        if self.chat_id:
            # Save all messages that aren't saved yet
            import asyncio
            asyncio.create_task(self._save_current_messages())

        # Clear uploaded images after sending
        self.img = []

    async def _save_current_messages(self):
        """Save current messages to database"""
        from ark.db.utils import save_message_from_dict, update_chat_title, get_message_count
        
        # Prevent concurrent saves
        if self._saving_messages:
            return
        
        self._saving_messages = True
        
        try:
            clerk_state = await self.get_state(clerk.ClerkState)
            if not clerk_state.is_signed_in or not self.chat_id:
                return
            
            # Get current message count in DB to know which messages to save
            db_count = await get_message_count(self.chat_id)
            
            # Only save messages that aren't already in the database
            if db_count < len(self.messages):
                # Save any new messages with manual order tracking
                for i in range(db_count, len(self.messages)):
                    message = self.messages[i]
                    message_order = i  # Use the index as the order
                    try:
                        await save_message_from_dict(self.chat_id, message_order, message)
                        print(f"Saved message {message_order} successfully")
                    except Exception as e:
                        print(f"Error saving message {message_order}: {e}")
                        # If it's a duplicate key error, skip it
                        if "duplicate key" in str(e):
                            continue
                        else:
                            break
                
                # Update chat title with first user message if not set
                if len(self.messages) > 0 and self.messages[0].get('role') == 'user':
                    first_message = self.messages[0].get('display_text', 'New Chat')[:100]
                    await update_chat_title(self.chat_id, first_message)
        
        finally:
            self._saving_messages = False

    def _get_model_for_action(self) -> str:
        """Get the appropriate model based on the selected action."""
        if self.selected_action == "Search":
            if self.selected_provider == ModelConfig.DEFAULT_PROVIDER:
                return ModelConfig.SEARCH_MODEL
            # For offline providers, use their selected model
            return self.selected_model if self.selected_model else None
        else:
            # Regular chat - use selected model
            return self.selected_model if self.selected_model else None

    def select_action(self, action: str):
        if self.selected_action == action:
            # Deactivating the current action - reset to defaults
            self.selected_action = ""
            self.selected_provider = ModelConfig.DEFAULT_PROVIDER
            self.selected_model = ModelConfig.CHAT_MODEL
        else:
            self.selected_action = action

    def handle_search_click(self):
        """Handle search button click - toggle action and set/reset model accordingly"""
        if self.selected_action == "Search":
            # Deactivating search - reset to defaults
            self.selected_action = ""
            self.selected_provider = ModelConfig.DEFAULT_PROVIDER
            self.selected_model = ModelConfig.CHAT_MODEL
        else:
            # Activating search - set search model
            self.selected_action = "Search"
            self.selected_provider = ModelConfig.DEFAULT_PROVIDER
            self.selected_model = ModelConfig.SEARCH_MODEL

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.is_dark_theme = not self.is_dark_theme

    @rx.var
    def base64_imgs(self) -> list[str]:
        """Return a list of base64 data URLs for all uploaded images."""
        base64_list = []
        upload_dir = rx.get_upload_dir()
        for filename in self.img:
            image_path = upload_dir / filename
            try:
                base64_list.append(self.encode_image_to_base64(str(image_path)))
                os.remove(image_path)
            except Exception:
                # If file not found or error, skip
                continue
        return base64_list

    @staticmethod
    def encode_image_to_base64(image_path: str) -> str:
        """Encode an image file to a base64 data URL.

        Args:
            image_path: The path to the image file.

        Returns:
            The base64 data URL of the image.
        """
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
        # Guess MIME type from extension (simple version)
        if image_path.lower().endswith(".png"):
            mime = "image/png"
        else:
            mime = "image/jpeg"
        return f"data:{mime};base64,{encoded}"

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.name

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.name)

    @rx.event
    def clear_images(self):
        """Clear the uploaded images list."""
        self.img = []

    @rx.event
    async def load_user_chats(self):
        """Load user's chats from database"""
        from ark.db.utils import get_user_chats
        
        clerk_state = await self.get_state(clerk.ClerkState)
        if not clerk_state.is_signed_in:
            self.user_chats = []
            return
        
        chats = await get_user_chats(clerk_state.user_id, limit=50)
        self.user_chats = chats

    @rx.event
    async def load_chat_history(self, chat_id: str):
        """Load chat history from database and set provider/model"""
        from ark.db.utils import get_chat_messages, chat_exists, get_chat
        
        clerk_state = await self.get_state(clerk.ClerkState)
        if not clerk_state.is_signed_in:
            return
        
        # Verify user owns this chat and get chat metadata
        if await chat_exists(chat_id, clerk_state.user_id):
            # Load chat metadata (provider/model)
            chat_data = await get_chat(chat_id)
            if chat_data:
                self.selected_provider = chat_data.get("initial_provider", ModelConfig.DEFAULT_PROVIDER)
                self.selected_model = chat_data.get("initial_model", ModelConfig.CHAT_MODEL)
                print(f"Loaded chat {chat_id} with provider: {self.selected_provider}, model: {self.selected_model}")
            
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
            print(f"Loaded {len(self.messages)} messages for chat {chat_id}")





    @rx.event
    async def handle_auth_change(self):
        """Handle authentication state changes (login/logout)."""
        from ark.db.utils import init_user_if_not_exists
        
        clerk_state = await self.get_state(clerk.ClerkState)
        clerk_user_state = await self.get_state(clerk.ClerkUser)
        
        if clerk_state.is_signed_in:
            print(f"User signed in: {clerk_state.user_id}")
            print(f"User Name: {clerk_user_state.first_name}")
            self.logged_user_name = clerk_user_state.first_name or ""
            
            # Initialize user in database
            await init_user_if_not_exists(
                clerk_state.user_id, 
                clerk_user_state.first_name or ""
            )
        else:
            print("User signed out")
            self.logged_user_name = ""
