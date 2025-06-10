import reflex as rx
import base64


class Upload_State(rx.State):
    """The app state."""

    # The images to show.
    img: list[str]
    llm_response: str = ""

    def send_image_to_openrouter(self, image_path: str, api_key: str) -> dict:
        """Send a base64-encoded image to OpenRouter LLM and get the response.

        Args:
            image_path: The path to the image file.
            api_key: The OpenRouter API key.

        Returns:
            The JSON response from OpenRouter.
        """
        import requests
        import base64

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Encode image to base64 and create data URL
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        if image_path.lower().endswith(".png"):
            mime = "image/png"
        else:
            mime = "image/jpeg"
        data_url = f"data:{mime};base64,{base64_image}"

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_url
                        }
                    }
                ]
            }
        ]

        payload = {
            "model": "google/gemini-2.0-flash-001",
            "messages": messages
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    @rx.event
    async def trigger_llm(self):
        """Trigger LLM response for the first uploaded image."""
        import os

        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if not self.img or not api_key:
            self.llm_response = "No image uploaded or API key missing."
            return

        upload_dir = rx.get_upload_dir()
        image_path = str(upload_dir / self.img[0])
        try:
            result = self.send_image_to_openrouter(image_path, api_key)
            # Clean up: delete the file after converting to base64 and sending to LLM
            import os
            try:
                os.remove(image_path)
            except Exception:
                pass
            # Try to extract the main response text
            content = ""
            if "choices" in result and result["choices"]:
                message = result["choices"][0].get("message", {})
                if isinstance(message, dict):
                    content = message.get("content", "")
                else:
                    content = str(message)
            else:
                content = str(result)
            self.llm_response = content
        except Exception as e:
            self.llm_response = f"Error: {e}"

    @rx.var
    def base64_imgs(self) -> list[str]:
        """Return a list of base64 data URLs for all uploaded images."""
        base64_list = []
        upload_dir = rx.get_upload_dir()
        for filename in self.img:
            image_path = upload_dir / filename
            try:
                base64_list.append(self.encode_image_to_base64(str(image_path)))
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


color = "rgb(107,99,246)"


def upload_component():
    """The main view."""
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text("Drag and drop files here or click to select files"),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            padding="5em",
            accept={
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
            },
        ),
        rx.hstack(rx.foreach(rx.selected_files("upload1"), rx.text)),
        rx.button(
            "Upload",
            on_click=Upload_State.handle_upload(rx.upload_files(upload_id="upload1")),
        ),
        rx.button(
            "Clear",
            on_click=[
                rx.clear_selected_files("upload1"),
                Upload_State.clear_images(),
            ],
        ),
        rx.foreach(
            Upload_State.base64_imgs,
            lambda img: rx.image(src=img),
        ),
        rx.button(
            "Ask LLM about first image",
            on_click=Upload_State.trigger_llm,
            style={"marginTop": "2em"}
        ),
        rx.text(Upload_State.llm_response, style={"marginTop": "1em", "whiteSpace": "pre-wrap"}),
        padding="5em",
    )
