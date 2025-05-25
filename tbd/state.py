import reflex as rx
from tbd.services import openrouter


class State(rx.State):
    prompt: str = ""
    messages: list[dict[str, str]] = []

    def set_prompt(self, value: str):
        self.prompt = value

    def send_message(self):
        if self.prompt:
            # Add user message
            self.messages.append({"role": "user", "content": self.prompt})

            # Get AI response using all conversation history
            response = openrouter.ask(self.messages)

            # Add assistant response
            self.messages.append({"role": "assistant", "content": response})

            # Clear prompt
            self.prompt = ""
