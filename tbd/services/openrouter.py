from openai import OpenAI
import os

_DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant."

# Provider configurations
PROVIDER_CONFIGS = {
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": os.environ.get("OPENROUTER_API_KEY", ""),
        "default_model": "google/gemini-2.0-flash-001"
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
        "default_model": None  # No default - user must select a model
    },
    "lmstudio": {
        "base_url": "http://localhost:1234/v1",
        "api_key": "lmstudio",
        "default_model": None  # No default - user must select a model
    }
}

# Default OpenRouter client for backward compatibility
client = OpenAI(
    base_url=PROVIDER_CONFIGS["openrouter"]["base_url"],
    api_key=PROVIDER_CONFIGS["openrouter"]["api_key"],
)


def create_client(provider="openrouter"):
    """Create an OpenAI client for the specified provider."""
    config = PROVIDER_CONFIGS.get(provider, PROVIDER_CONFIGS["openrouter"])
    return OpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"],
    )


def ask(messages: list[dict[str, str]], model=None, provider="openrouter"):
    """Send messages to the specified AI provider and return the response.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        model: Model name to use (if None, uses provider's default)
        provider: Provider to use ('openrouter', 'ollama', 'lmstudio')
    """
    # Get provider configuration
    config = PROVIDER_CONFIGS.get(provider, PROVIDER_CONFIGS["openrouter"])
    
    # Use provided model or fall back to provider's default
    if model is None:
        model = config["default_model"]
        
    # For offline providers, model selection is required
    if model is None and provider in ["ollama", "lmstudio"]:
        raise ValueError(f"Model selection is required for {provider}. Please select a model from the available options.")
    
    # Create client for the specified provider
    provider_client = create_client(provider)
    
    # Prepend system message if not already present
    full_messages = messages.copy()
    if not full_messages or full_messages[0]["role"] != "system":
        full_messages.insert(0, {"role": "system", "content": _DEFAULT_SYSTEM_MESSAGE})

    completion = provider_client.chat.completions.create(model=model, messages=full_messages)

    return completion.choices[0].message.content


def get_ollama_models():
    """Get available models from Ollama."""
    try:
        ollama_client = create_client("ollama")
        models = ollama_client.models.list()
        return [model.id for model in models.data]
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return []


def get_lmstudio_models():
    """Get available models from LM Studio."""
    try:
        lmstudio_client = create_client("lmstudio")
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


def get_provider_config(provider):
    """Get configuration for a specific provider."""
    return PROVIDER_CONFIGS.get(provider, PROVIDER_CONFIGS["openrouter"])


def get_available_providers():
    """Get list of available providers."""
    return list(PROVIDER_CONFIGS.keys())
