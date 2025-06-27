# Ark - AI Chat Application

A modern, feature-rich AI chat application built with Python and Reflex that provides seamless access to cutting-edge AI models through OpenRouter.

## Features

### 🤖 AI Capabilities

- **OpenRouter Integration**: Access to hundreds of premium AI models through a unified API
- **Multi-modal Support**: Chat with text, images (PNG, JPEG), and PDF documents
- **Real-time Streaming**: Token-by-token response streaming for immediate feedback
- **Smart Search**: Integrated web search with automatic citation extraction using Perplexity models
- **File Upload**: Drag & drop interface with cloud storage (Cloudflare R2)

### 💬 Chat Experience

- **Persistent Conversations**: Full chat history with PostgreSQL storage
- **Theme Support**: Light and dark mode interface
- **Responsive Design**: Optimized for desktop and mobile devices
- **User Authentication**: Secure login with Clerk integration

### ⚡ Performance

- **Cloud File Storage**: Efficient file handling with Cloudflare R2 integration
- **Streaming Responses**: Real-time AI responses with live UI updates
- **Citation Support**: Automatic source extraction from search-enabled models

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database (Neon recommended)
- Cloudflare R2 account (for file uploads)

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd ark
   ```

2. **Create and activate virtual environment**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file with the following variables:

   ```env
   # Required API Keys
   OPENROUTER_API_KEY=your_openrouter_api_key
   CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
   CLERK_SECRET_KEY=your_clerk_secret_key

   # Database
   NEON_DB_URL=your_postgresql_connection_string

   # File Storage (Cloudflare R2)
   R2_ACCESS_KEY_ID=your_r2_access_key
   R2_SECRET_ACCESS_KEY=your_r2_secret_key
   R2_BUCKET_NAME=your_r2_bucket_name
   R2_ENDPOINT_URL=https://your_account_id.r2.cloudflarestorage.com

   # Optional
   UMAMI_WEBSITE_ID=your_analytics_id
   ```

5. **Database Setup**

   ```bash
   python ark/database/schema.py
   ```

6. **Run the application**
   ```bash
   reflex run
   ```

## API Keys Setup

### OpenRouter

1. Visit [https://openrouter.ai](https://openrouter.ai)
2. Sign up for an account
3. Navigate to API Keys section
4. Generate a new API key
5. Add to your `.env` file as `OPENROUTER_API_KEY`

### Clerk Authentication

1. Visit [https://clerk.com](https://clerk.com)
2. Create a new application
3. Copy the publishable and secret keys
4. Add to your `.env` file

### Cloudflare R2

1. Sign up for Cloudflare account
2. Create an R2 bucket
3. Generate API tokens with R2 permissions
4. Add credentials to your `.env` file

## Usage

### Starting a Chat

1. Launch the application with `reflex run`
2. Sign in or create an account through Clerk
3. Start typing your message in the chat input
4. Upload images or PDFs using the paperclip icon
5. Press Enter or click Send to get a response

### Available Models

- **Chat Models**: Defaults to Gemini 2.5 Flash
- **Search Models**: Perplexity Sonar Pro for web search with citations
- All models accessible through OpenRouter's unified API

### File Upload Features

- **Images**: Visual analysis and description (PNG, JPEG)
- **PDFs**: Document processing and content analysis
- **Cloud Storage**: Files stored securely in Cloudflare R2
- **Smart Processing**: Optimized handling for different AI providers

### Search Functionality

- Click the "Search" button to enable web search mode
- Automatic citation extraction from search results
- Sources displayed as expandable sections
- Powered by Perplexity's search models

## Architecture

### Core Components

- **Frontend**: Reflex-based reactive UI with real-time updates
- **Backend**: Python with async message processing
- **Database**: PostgreSQL with Neon hosting for chat persistence
- **Storage**: Cloudflare R2 for scalable file storage
- **Authentication**: Clerk for secure user management

### Provider System

- **Unified Interface**: Single provider (OpenRouter) for all AI models
- **Streaming Support**: Real-time token-by-token responses
- **Model Flexibility**: Easy switching between different AI models
- **Citation Handling**: Automatic source extraction for search models

## Project Structure

```
ark/
├── ark/                    # Main application code
│   ├── components/         # Reusable UI components
│   │   ├── chat/          # Chat-specific components
│   │   └── common/        # Shared UI elements
│   ├── pages/             # Application pages
│   ├── providers/         # AI provider integrations
│   ├── services/          # External service integrations
│   ├── database/          # Database schema and utilities
│   ├── handlers/          # Message processing logic
│   └── state.py           # Application state management
├── assets/                # Static assets
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md             # Documentation
```

## Development

### Database Schema

- **users**: User account information
- **chats**: Chat session metadata
- **messages**: Individual chat messages
- **files**: File metadata and references

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:

- Check the documentation above
- Ensure all API keys are properly configured
- Verify database connection
- Check Cloudflare R2 configuration for file upload issues
