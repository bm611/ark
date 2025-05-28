from openai import OpenAI
import os

_DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant."
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)


def ask(messages: list[dict[str, str]], model="google/gemini-2.0-flash-001"):
    """Send messages to OpenRouter API and return the response."""

    # Prepend system message if not already present
    full_messages = messages.copy()
    if not full_messages or full_messages[0]["role"] != "system":
        full_messages.insert(0, {"role": "system", "content": _DEFAULT_SYSTEM_MESSAGE})

    completion = client.chat.completions.create(model=model, messages=full_messages)

    return completion.choices[0].message.content


def get_ollama_models():
    """Get available models from Ollama."""
    try:
        ollama_client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )
        
        models = ollama_client.models.list()
        return [model.id for model in models.data]
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return []


def get_lmstudio_models():
    """Get available models from LM Studio."""
    try:
        lmstudio_client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="lmstudio",
        )
        
        models = lmstudio_client.models.list()
        return [model.id for model in models.data]
    except Exception as e:
        print(f"Error connecting to LM Studio: {e}")
        return []


def list_available_models(api_base, api_key):
    """Generic function to list available models from any OpenAI-compatible API."""
    try:
        client = OpenAI(
            base_url=api_base,
            api_key=api_key,
        )

        models = client.models.list()

        print("Available models:")
        for model in models.data:
            print(f"- {model.id}")
    except Exception as e:
        print(f"Error connecting to {api_base}: {e}")
