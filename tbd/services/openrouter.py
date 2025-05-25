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
