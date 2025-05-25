from openai import OpenAI
import os

_DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant."


class ChatSession:
    def __init__(self):
        self.messages = [{"role": "system", "content": _DEFAULT_SYSTEM_MESSAGE}]
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )

    def ask(self, user_message, model="google/gemini-2.0-flash-001"):
        # Add user message to history
        self.messages.append({"role": "user", "content": user_message})

        # Get response from API
        completion = self.client.chat.completions.create(
            model=model, messages=self.messages
        )

        # Extract assistant response
        assistant_response = completion.choices[0].message.content

        # Add assistant response to history
        self.messages.append({"role": "assistant", "content": assistant_response})

        return assistant_response
