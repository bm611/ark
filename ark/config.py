"""
Configuration constants and settings for the Ark application.
"""
import os
from typing import List, Dict, Any


# Environment Variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
NEON_DB_URL = os.getenv("NEON_DB_URL")
UMAMI_WEBSITE_ID = os.getenv("UMAMI_WEBSITE_ID", "")
CLERK_PUBLISHABLE_KEY = os.environ.get("CLERK_PUBLISHABLE_KEY")
CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY")
RAILWAY_PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")


# Model Configuration
class ModelConfig:
    DEFAULT_PROVIDER = "openrouter"
    CHAT_MODEL = "google/gemini-2.5-flash"
    SEARCH_MODEL = "perplexity/sonar-pro"


# Provider Configurations
class ProviderConfig:
    OPENROUTER = {
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "google/gemini-2.0-flash-001",
        "available_models": [
            "google/gemini-2.0-flash-001",
            "perplexity/sonar",
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4",
        ]
    }
    
    OLLAMA = {
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
        "default_model": None,
    }
    
    LMSTUDIO = {
        "base_url": "http://localhost:1234/v1", 
        "api_key": "lmstudio",
        "default_model": None,
    }


# Database Configuration
class DatabaseConfig:
    DEFAULT_CHAT_LIMIT = 50
    DEFAULT_CHAT_OFFSET = 0
    DEFAULT_INITIAL_PROVIDER = "openrouter"
    DEFAULT_INITIAL_MODEL = "google/gemini-2.5-flash"


# Application Configuration  
class AppConfig:
    FRONTEND_PORT = 3000
    BACKEND_PORT = 8000
    TELEMETRY_ENABLED = False
    SHOW_BUILT_WITH_REFLEX = False


# System Prompt Configuration
SYSTEM_MESSAGE_PROMPT = """
You are Ark, a minimalist AI assistant focused on providing concise, accurate, and helpful responses.

Core Principles:
- Provide clear, direct answers without unnecessary elaboration
- Be concise but comprehensive
- Prioritize accuracy and helpfulness
- When uncertain, acknowledge limitations rather than guessing
- Maintain a friendly but professional tone

Response Guidelines:
- Keep responses focused and to the point
- Use simple, accessible language
- Structure information clearly when needed
- Provide examples when they enhance understanding
- Avoid repetition and filler content

For coding questions:
- Provide working, tested code when possible
- Include brief explanations for complex logic
- Follow best practices and current standards
- Mention important caveats or considerations

For general questions:
- Give direct answers supported by relevant context
- Break down complex topics into digestible parts
- Suggest next steps or related resources when appropriate

Remember: Your goal is to be maximally helpful while respecting the user's time and attention.
"""