import reflex as rx
from tbd.services import openrouter


class State(rx.State):
    prompt: str = ""
    messages: list[dict[str, str]] = []
    is_gen: bool = False
    selected_action: str = ""
    
    # Provider and model selection
    selected_provider: str = "openrouter"  # Default to openrouter
    selected_model: str = ""  # Empty means use provider's default model

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
        self.messages.append({"role": "user", "content": self.prompt})
        self.prompt = ""

    def reset_chat(self):
        self.messages = []
        self.is_gen = False

    def send_message(self):
        # Determine which model to use based on action and selection
        if self.selected_action == "Search":
            # For search, use Perplexity if on OpenRouter, otherwise use selected provider
            if self.selected_provider == "openrouter":
                response = openrouter.ask(self.messages, model="perplexity/sonar", provider="openrouter")
            else:
                # Use the selected offline provider for search
                model = self.selected_model if self.selected_model else None
                response = openrouter.ask(self.messages, model=model, provider=self.selected_provider)
        else:
            # For regular chat, use the selected provider and model
            model = self.selected_model if self.selected_model else None
            response = openrouter.ask(self.messages, model=model, provider=self.selected_provider)
        
        self.is_gen = False
        # Add assistant response
        self.messages.append({"role": "assistant", "content": response})

    def select_action(self, action: str):
        if self.selected_action == action:
            self.selected_action = ""
        else:
            self.selected_action = action
