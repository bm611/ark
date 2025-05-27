import reflex as rx
from tbd.services import openrouter


class State(rx.State):
    prompt: str = ""
    messages: list[dict[str, str]] = []
    is_gen: bool = False
    selected_action: str = ""

    @rx.var
    def current_url(self) -> str:
        return self.router.page.path

    def set_prompt(self, value: str):
        self.prompt = value

    def handle_generation(self):
        self.is_gen = True
        self.messages.append({"role": "user", "content": self.prompt})

        self.prompt = ""

    def reset_chat(self):
        self.messages = []
        self.is_gen = False

    def send_message(self):
        # Get AI response using all conversation history
        if self.selected_action == "Search":
            response = openrouter.ask(self.messages, "perplexity/sonar")
        else:
            response = openrouter.ask(self.messages)
        self.is_gen = False
        # Add assistant response
        self.messages.append({"role": "assistant", "content": response})

    def select_action(self, action: str):
        if self.selected_action == action:
            self.selected_action = ""
        else:
            self.selected_action = action
