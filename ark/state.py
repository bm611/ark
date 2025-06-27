import reflex as rx
from typing import List
from ark.models.chat import ChatMessage, FileReference
from ark.handlers.message_handler import message_handler
import reflex_clerk_api as clerk
import base64
import os
import uuid
import asyncpg


# Model Configuration Constants
class ModelConfig:
    DEFAULT_PROVIDER = "openrouter"
    CHAT_MODEL = "google/gemini-2.5-flash"
    SEARCH_MODEL = "perplexity/sonar-pro"


class State(rx.State):
    prompt: str = ""
    messages: List[ChatMessage] = []
    is_gen: bool = False
    is_streaming: bool = False
    selected_action: str = ""
    img: list[str] = []
    pdf_files: list[str] = []
    uploaded_files: List[FileReference] = []  # R2 uploaded files
    logged_user_name: str = ""
    chat_id: str = ""
    user_chats: List[dict] = []
    _saving_messages: bool = False

    # Thinking section expansion state
    thinking_expanded: dict[int, bool] = {}
    # Citations section expansion state
    citations_expanded: dict[int, bool] = {}

    # Provider and model selection
    selected_provider: str = ModelConfig.DEFAULT_PROVIDER
    selected_model: str = ModelConfig.CHAT_MODEL

    # Theme state
    is_dark_theme: bool = False

    # Mobile menu state
    is_mobile_menu_open: bool = False

    # Current message image
    current_message_image: str = ""

    async def generate_chat_id_and_redirect(self):
        from ark.database.utils import create_chat

        self.chat_id = str(uuid.uuid4())
        self.is_mobile_menu_open = False

        # Get user ID from Clerk
        clerk_state = await self.get_state(clerk.ClerkState)
        if clerk_state.is_signed_in:
            # Create chat in database
            await create_chat(
                chat_id=self.chat_id,
                user_id=clerk_state.user_id,
                title="New Chat",  # Will be updated with first message
                initial_provider=self.selected_provider,
                initial_model=self.selected_model,
            )

        return rx.redirect(f"/chat/{self.chat_id}")

    async def handle_chat_page_load(self):
        """Handle loading a chat page - either load existing chat or process new message."""
        # Get the conversation ID from the URL
        conversation_id = self.router.page.params.get("conversation", "")

        if conversation_id and conversation_id != self.chat_id:
            # This is an existing chat, load its history
            await self.load_chat_history(conversation_id)
        elif (
            self.messages
            and self.messages[-1].get("role") == "user"
            and not self.is_streaming
        ):
            # This is a new chat with a user message waiting to be processed
            async for _ in self.send_message_stream():
                yield

    @rx.var
    def current_url(self) -> str:
        return self.router.page.path
    

    def set_prompt(self, value: str):
        self.prompt = value

    def set_provider_and_model(self, provider: str, model: str = ""):
        """Set the selected provider and model"""
        self.selected_provider = provider
        self.selected_model = model
        print(f"Provider set to: {provider}, Model: {model or 'default'}")

    def handle_generation(self):
        self.is_gen = True

        # Create content array starting with text
        content = [{"type": "text", "text": self.prompt}]

        # Process R2 uploaded files first (preferred method)
        for file_ref in self.uploaded_files:
            if file_ref.get("type") == "image" and file_ref.get("presigned_url"):
                # Use presigned URL for images (OpenRouter can fetch external images)
                self.current_message_image = file_ref["presigned_url"]
                content.append(
                    {"type": "image_url", "image_url": {"url": file_ref["presigned_url"]}}
                )
            elif file_ref.get("type") == "pdf" and file_ref.get("file_key"):
                # Download and encode PDFs for AI processing
                try:
                    from ark.services.r2_storage import download_and_encode_pdf, generate_presigned_url
                    # Generate fresh presigned URL for PDF download
                    presigned_url = generate_presigned_url(file_ref["file_key"])
                    if presigned_url:
                        pdf_base64 = download_and_encode_pdf(presigned_url, file_ref.get("original_filename", "document.pdf"))
                        if pdf_base64:
                            content.append(
                                {
                                    "type": "file",
                                    "file": {
                                        "filename": file_ref.get("original_filename", "document.pdf"),
                                        "file_data": pdf_base64,
                                    },
                                }
                            )
                except Exception as e:
                    print(f"Error processing R2 PDF {file_ref.get('original_filename')}: {e}")

        # Fallback to legacy base64 processing (for offline users or R2 failures)
        if self.img:
            base64_images = self.base64_imgs
            if base64_images:
                if not self.current_message_image:  # Only if no R2 image was set
                    self.current_message_image = base64_images[0]
                content.append(
                    {"type": "image_url", "image_url": {"url": base64_images[0]}}
                )

        if self.pdf_files:
            base64_pdfs = self.base64_pdfs
            for pdf_data in base64_pdfs:
                content.append(
                    {
                        "type": "file",
                        "file": {
                            "filename": pdf_data["filename"],
                            "file_data": pdf_data["data"],
                        },
                    }
                )

        # Create user message with file references
        files_metadata = []
        
        # Add R2 uploaded files to metadata (preferred)
        files_metadata.extend(self.uploaded_files)
        
        # Add legacy base64 files metadata (fallback)
        base64_images = self.base64_imgs
        for i, filename in enumerate(self.img):
            base64_url = base64_images[i] if i < len(base64_images) else None
            if base64_url:  # Only add if we have valid base64 data
                files_metadata.append({
                    "filename": filename,
                    "content_type": f"image/{filename.split('.')[-1].lower()}",
                    "type": "image",
                    "base64_url": base64_url  # Add base64 data for display
                })
            
        # Add PDF files metadata with base64 data
        base64_pdfs = self.base64_pdfs
        for pdf_data in base64_pdfs:
            if pdf_data.get("data"):  # Only add if we have valid base64 data
                files_metadata.append({
                    "filename": pdf_data["filename"],
                    "content_type": "application/pdf", 
                    "type": "pdf",
                    "base64_url": pdf_data["data"]  # Add base64 data for display
                })
            
        user_message = {
            "role": "user", 
            "content": content, 
            "display_text": self.prompt,
            "files": files_metadata
        }
        self.messages.append(user_message)
        self.prompt = ""

    async def reset_chat(self):
        """Reset chat and save current conversation"""
        from ark.database.utils import save_all_messages

        # Save current conversation if it exists and has messages
        if self.chat_id and self.messages:
            clerk_state = await self.get_state(clerk.ClerkState)
            if clerk_state.is_signed_in:
                await save_all_messages(self.chat_id, self.messages)

        # Clear state
        self.img = []
        self.pdf_files = []
        self.uploaded_files = []
        self.messages = []
        self.is_gen = False
        self.selected_provider = ModelConfig.DEFAULT_PROVIDER
        self.selected_model = ModelConfig.CHAT_MODEL
        self.selected_action = ""
        self.thinking_expanded = {}
        self.citations_expanded = {}
        self.chat_id = ""
        self.current_message_image = ""
        self.is_mobile_menu_open = False

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

    async def send_message_stream(self):
        """Send message with streaming response."""
        if self.messages and self.messages[-1].get("role") == "assistant":
            # If last message is assistant, don't allow sending another message
            return

        # Set streaming state
        self.is_streaming = True
        yield

        # Determine model based on action and selection
        model = self._get_model_for_action()

        # Add empty assistant message that will be filled during streaming
        assistant_message = {
            "role": "assistant",
            "content": "",
            "display_text": "",
        }
        self.messages.append(assistant_message)
        yield

        try:
            # Process the message with streaming
            async for (
                partial_message,
                is_complete,
            ) in message_handler.process_message_stream(
                messages=self.messages[
                    :-1
                ],  # Exclude the empty assistant message we just added
                provider=self.selected_provider,
                model=model,
                action=self.selected_action,
            ):
                # Update the last message (assistant message) with streaming content
                self.messages[-1] = partial_message
                # Force Reflex to detect the state change
                self.messages = self.messages

                # Yield to update UI
                yield

                # If this is the final complete message, break
                if is_complete:
                    break

        except Exception as e:
            # Handle errors by updating the last message with error info
            self.messages[-1] = {
                "role": "assistant",
                "content": f"Error: {str(e)}",
                "display_text": f"Error: {str(e)}",
            }
            yield

        finally:
            # Reset streaming state
            self.is_streaming = False
            self.is_gen = False
            yield

            # Save messages to database if chat_id exists
            if self.chat_id:
                # Save all messages that aren't saved yet
                import asyncio

                asyncio.create_task(self._save_current_messages())

    async def _save_current_messages(self):
        """Save current messages to database"""
        from ark.database.utils import (
            save_message_from_dict,
            update_chat_title,
            get_message_count,
        )

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
                    message = self.messages[i].copy()  # Make a copy to avoid modifying original
                    # Add user_id for R2 upload if this is a user message with files
                    if message.get("role") == "user" and message.get("files"):
                        message["user_id"] = clerk_state.user_id
                    message_order = i  # Use the index as the order
                    try:
                        await save_message_from_dict(
                            self.chat_id, message_order, message
                        )
                        print(f"Saved message {message_order} successfully")
                    except Exception as e:
                        print(f"Error saving message {message_order}: {e}")
                        # If it's a duplicate key error, skip it
                        if "duplicate key" in str(e):
                            continue
                        else:
                            break

                # Update chat title with first user message if not set
                if len(self.messages) > 0 and self.messages[0].get("role") == "user":
                    first_message = self.messages[0].get("display_text", "New Chat")[
                        :100
                    ]
                    await update_chat_title(self.chat_id, first_message)

        finally:
            self._saving_messages = False

    def _get_model_for_action(self) -> str:
        """Get the appropriate model based on the selected action."""
        if self.selected_action == "Search":
            if self.selected_provider == ModelConfig.DEFAULT_PROVIDER:
                return ModelConfig.SEARCH_MODEL
            # Use selected model for other providers
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

    def toggle_mobile_menu(self):
        """Toggle mobile menu open/close state"""
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    def close_mobile_menu(self):
        """Close mobile menu"""
        self.is_mobile_menu_open = False

    def toggle_theme_and_close_menu(self):
        """Toggle theme and close mobile menu"""
        self.toggle_theme()
        self.close_mobile_menu()

    def handle_auth_action(self):
        """Handle auth actions and close mobile menu"""
        self.close_mobile_menu()

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

    @staticmethod
    def encode_pdf_to_base64(pdf_path: str) -> str:
        """Encode a PDF file to a base64 data URL.

        Args:
            pdf_path: The path to the PDF file.

        Returns:
            The base64 data URL of the PDF.
        """
        with open(pdf_path, "rb") as pdf_file:
            encoded = base64.b64encode(pdf_file.read()).decode("utf-8")
        return f"data:application/pdf;base64,{encoded}"

    @rx.var
    def base64_pdfs(self) -> list[dict]:
        """Return a list of base64 data URLs for all uploaded PDFs with filenames."""
        pdf_list = []
        upload_dir = rx.get_upload_dir()
        for filename in self.pdf_files:
            pdf_path = upload_dir / filename
            try:
                base64_data = self.encode_pdf_to_base64(str(pdf_path))
                pdf_list.append({"filename": filename, "data": base64_data})
                os.remove(pdf_path)
            except Exception:
                # If file not found or error, skip
                continue
        return pdf_list

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle file upload - prioritize R2 upload, fallback to base64 for universal processing.

        Args:
            files: The uploaded files.
        """
        from ark.services.r2_storage import upload_file, generate_presigned_url
        
        clerk_state = await self.get_state(clerk.ClerkState)
        
        for file in files:
            try:
                upload_data = await file.read()
                
                # Save to local storage (needed for fallback and R2 upload)
                outfile = rx.get_upload_dir() / file.name
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)
                
                # Try R2 upload if user is signed in
                r2_success = False
                if clerk_state.is_signed_in:
                    try:
                        r2_metadata = upload_file(
                            file_path=file.name,
                            file_content=upload_data,
                            content_type=file.content_type or "application/octet-stream",
                            user_id=clerk_state.user_id
                        )
                        
                        if r2_metadata:
                            # Generate presigned URL
                            presigned_url = generate_presigned_url(r2_metadata['file_key'])
                            
                            # Create FileReference for R2 file
                            file_ref: FileReference = {
                                'file_key': r2_metadata['file_key'],
                                'original_filename': file.name,
                                'content_type': file.content_type or "application/octet-stream",
                                'file_size': len(upload_data),
                                'type': "pdf" if file.name.lower().endswith(".pdf") else "image",
                                'presigned_url': presigned_url
                            }
                            self.uploaded_files.append(file_ref)
                            r2_success = True
                            print(f"Successfully uploaded {file.name} to R2")
                            
                            # Clean up local file after successful R2 upload
                            try:
                                os.remove(outfile)
                                print(f"Cleaned up local file: {file.name}")
                            except Exception as cleanup_e:
                                print(f"Could not remove local file {file.name}: {cleanup_e}")
                            
                    except Exception as e:
                        print(f"R2 upload failed for {file.name}: {e}")
                
                # Fallback to legacy base64 system if R2 failed or user not signed in
                if not r2_success:
                    if file.name.lower().endswith(".pdf"):
                        self.pdf_files.append(file.name)
                    else:
                        self.img.append(file.name)
                        
            except Exception as e:
                print(f"Error processing file {file.name}: {e}")

    @rx.event
    def clear_images(self):
        """Clear the uploaded images list."""
        self.img = []
        # Also clear image files from uploaded_files
        self.uploaded_files = [f for f in self.uploaded_files if f.get("type") != "image"]

    @rx.event
    def clear_pdfs(self):
        """Clear the uploaded PDFs list."""
        self.pdf_files = []
        # Also clear PDF files from uploaded_files
        self.uploaded_files = [f for f in self.uploaded_files if f.get("type") != "pdf"]

    @rx.event
    def clear_all_files(self):
        """Clear all uploaded files."""
        self.img = []
        self.pdf_files = []
        self.uploaded_files = []

    @rx.event
    async def load_user_chats(self):
        """Load user's chats from database"""
        from ark.database.utils import get_user_chats

        clerk_state = await self.get_state(clerk.ClerkState)
        if not clerk_state.is_signed_in:
            self.user_chats = []
            return

        chats = await get_user_chats(clerk_state.user_id, limit=50)
        self.user_chats = chats

    @rx.event
    async def load_chat_history(self, chat_id: str):
        """Load chat history from database and set provider/model"""
        from ark.database.utils import get_chat_messages, chat_exists, get_chat, get_connection
        from ark.database.file_utils import get_chat_files
        from ark.services.r2_storage import generate_presigned_url

        clerk_state = await self.get_state(clerk.ClerkState)
        if not clerk_state.is_signed_in:
            return

        # Verify user owns this chat and get chat metadata
        if await chat_exists(chat_id, clerk_state.user_id):
            # Load chat metadata (provider/model)
            chat_data = await get_chat(chat_id)
            if chat_data:
                self.selected_provider = chat_data.get(
                    "initial_provider", ModelConfig.DEFAULT_PROVIDER
                )
                self.selected_model = chat_data.get(
                    "initial_model", ModelConfig.CHAT_MODEL
                )
                print(
                    f"Loaded chat {chat_id} with provider: {self.selected_provider}, model: {self.selected_model}"
                )

            # Load chat files from R2
            file_references = []
            conn = await get_connection()
            try:
                chat_files = await get_chat_files(conn, chat_id)
                print(f"Found {len(chat_files)} files in database for chat {chat_id}")
                
                # Convert to FileReference and generate presigned URLs
                for file_data in chat_files:
                    try:
                        presigned_url = generate_presigned_url(file_data['file_key'])
                        if presigned_url:  # Only add files with valid presigned URLs
                            # Determine file type from content_type
                            file_type = "pdf" if file_data['content_type'] == "application/pdf" else "image"
                            
                            file_ref: FileReference = {
                                'file_id': str(file_data['id']),
                                'file_key': file_data['file_key'],
                                'original_filename': file_data['original_filename'],
                                'content_type': file_data['content_type'],
                                'file_size': file_data['file_size'],
                                'type': file_type,
                                'presigned_url': presigned_url
                            }
                            file_references.append(file_ref)
                            print(f"✓ Loaded file: {file_data['original_filename']} ({file_type}) with URL: {presigned_url[:50]}...")
                        else:
                            print(f"✗ Failed to generate presigned URL for file: {file_data['original_filename']}")
                    except Exception as e:
                        print(f"✗ Error processing file {file_data.get('original_filename', 'unknown')}: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error loading chat files: {e}")
            finally:
                await conn.close()
                
            print(f"Successfully loaded {len(file_references)} files with valid URLs")

            # Load messages
            db_messages = await get_chat_messages(chat_id)

            # Convert database messages to your ChatMessage format
            self.messages = []
            
            # Find which message should get the files (look for multimodal content)
            message_with_files_index = None
            for i, msg in enumerate(db_messages):
                if (msg["role"] == "user" and 
                    isinstance(msg["content"], list) and 
                    any(item.get("type") in ["image_url", "file"] for item in msg["content"] if isinstance(item, dict))):
                    message_with_files_index = i
                    break
            
            # If no multimodal content found, use first user message
            if message_with_files_index is None:
                for i, msg in enumerate(db_messages):
                    if msg["role"] == "user":
                        message_with_files_index = i
                        break
            
            for i, msg in enumerate(db_messages):
                # Handle content based on role and structure
                if isinstance(msg["content"], list):
                    if msg["role"] == "assistant":
                        # For assistant messages, extract text from content list for UI compatibility
                        content_text = ""
                        for item in msg["content"]:
                            if isinstance(item, dict) and item.get("type") == "text":
                                content_text = item.get("text", "")
                                break
                        content = content_text
                    else:
                        # For user messages, update image/file URLs with fresh presigned URLs
                        content = msg["content"]
                        
                        # Create a mapping of files by type for better matching
                        image_files = [f for f in file_references if f.get('type') == 'image']
                        pdf_files = [f for f in file_references if f.get('type') == 'pdf']
                        
                        for item in msg["content"]:
                            if isinstance(item, dict):
                                if item.get("type") == "image_url" and image_files:
                                    # Use the first available image file
                                    item["image_url"]["url"] = image_files[0]['presigned_url']
                                    print(f"Updated image URL with fresh presigned URL: {image_files[0]['presigned_url'][:50]}...")
                                elif item.get("type") == "file" and pdf_files:
                                    # Update PDF file data if needed (though it's usually base64)
                                    print(f"Found PDF file reference: {pdf_files[0]['original_filename']}")
                else:
                    content = msg["content"]

                chat_message = {
                    "role": msg["role"],
                    "content": content,
                    "display_text": msg["display_text"],
                }

                # Add file references to the appropriate message
                if msg["role"] == "user" and file_references and i == message_with_files_index:
                    chat_message["files"] = file_references
                    print(f"Added {len(file_references)} files to user message {i}")
                    for file_ref in file_references:
                        print(f"  - {file_ref.get('original_filename')}: {file_ref.get('presigned_url')[:50]}..." if file_ref.get('presigned_url') else f"  - {file_ref.get('original_filename')}: NO URL")

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
                    chat_message["tokens_per_second"] = round(msg["tokens_per_second"])

                self.messages.append(chat_message)

            self.chat_id = chat_id
            self.is_mobile_menu_open = False
            print(f"Loaded {len(self.messages)} messages for chat {chat_id}")

    @rx.event
    async def delete_chat(self, chat_id: str):
        """Delete a chat and all its messages and files"""
        from ark.database.utils import delete_chat, get_connection
        from ark.services.r2_storage import delete_chat_files

        clerk_state = await self.get_state(clerk.ClerkState)
        if not clerk_state.is_signed_in:
            return

        try:
            # Get file keys for cleanup before deleting chat
            conn = await get_connection()
            try:
                from ark.database.file_utils import get_chat_file_keys
                file_keys = await get_chat_file_keys(conn, chat_id)
            finally:
                await conn.close()

            # Delete files from R2 storage
            if file_keys:
                delete_chat_files(file_keys)

            # Delete the chat (this will also delete messages and file metadata due to foreign key cascade)
            success = await delete_chat(chat_id, clerk_state.user_id)

            if success:
                # Refresh the chat list from database to ensure UI is updated
                await self.load_user_chats()

                # If the deleted chat is the current chat, reset the current chat
                if self.chat_id == chat_id:
                    self.chat_id = ""
                    self.messages = []
            
                # Show success toast
                return rx.toast.success("Chat deleted successfully")
            else:
                # Show error toast
                return rx.toast.error("Failed to delete chat")
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return rx.toast.error("Failed to delete chat")

    @rx.event
    async def handle_auth_change(self):
        """Handle authentication state changes (login/logout)."""
        from ark.database.utils import init_user_if_not_exists

        clerk_state = await self.get_state(clerk.ClerkState)
        clerk_user_state = await self.get_state(clerk.ClerkUser)

        if clerk_state.is_signed_in:
            print(f"User signed in: {clerk_state.user_id}")
            print(f"User Name: {clerk_user_state.first_name}")
            self.logged_user_name = clerk_user_state.first_name or ""

            # Initialize user in database
            await init_user_if_not_exists(
                clerk_state.user_id, clerk_user_state.first_name or ""
            )
        else:
            print("User signed out")
            self.logged_user_name = ""
