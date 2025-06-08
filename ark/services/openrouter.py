"""
Legacy OpenRouter service - maintained for backward compatibility.
This module is deprecated. Use ark.providers.manager for new code.
"""
from ark.providers.manager import provider_manager


def ask(messages: list[dict[str, str]], model=None, provider="openrouter"):
    """
    Send messages to the specified AI provider and return the response.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        model: Model name to use (if None, uses provider's default)
        provider: Provider to use ('openrouter', 'ollama', 'lmstudio')
    """
    return provider_manager.chat_completion(
        messages=messages,
        provider_name=provider,
        model=model,
        tools=provider_manager.tool_manager.get_tool_schemas()
    )


def get_ollama_models():
    """Get available models from Ollama."""
    return provider_manager.get_models_for_provider("ollama")


def get_lmstudio_models():
    """Get available models from LM Studio."""
    return provider_manager.get_models_for_provider("lmstudio")
