# Ark - AI Chat Application

A modern, feature-rich AI chat application built with Python and Reflex that supports multiple AI providers and local models.

## Features

### 🌐 Online Features (Require Internet)
- **OpenRouter Integration**: Access to hundreds of AI models through OpenRouter's unified API
- **OpenAI SDK**: Easily plugin any OpenAI compatible model
- **Turbo Mode**: Ultra-fast responses using Qwen3-32B hosted on Cerebras
- **Perplexity Search**: Integrated search functionality powered by Perplexity AI

### 💻 Offline Features (No Internet Required)
- **Local Models**: Chat with locally hosted models via Ollama and LM Studio
- **Token Usage Tracking**: Performance metrics and statistics

### 💬 General Features
- Real-time conversation interface
- Modern, responsive UI design
- Multiple AI provider support

## Installation

### Quick Setup Options

#### Option 1: Online Only (Fastest Setup)
If you only want to use online AI models (OpenRouter, OpenAI, Perplexity):
1. Follow the basic setup steps below
2. Configure API keys in `.env` file
3. Skip local model setup sections

#### Option 2: Offline Only (No Internet Required)
If you want to use only local models:
1. Follow the basic setup steps below
2. Skip API key configuration
3. Set up either Ollama or LM Studio (see Local Models Setup section)

#### Option 3: Full Setup (Online + Offline)
For complete functionality:
1. Follow all setup steps below
2. Configure API keys for online features
3. Set up local models for offline usage

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

4. **Local LLM Setup**
   - If you want to use local models, follow the local model setup instructions below

5. **Run the application**
   ```bash
   reflex run
   ```

## Local Models Setup

### Ollama Setup

1. **Install Ollama**
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Windows
   # Download from https://ollama.com/download
   ```

2. **Start Ollama service**
   ```bash
   ollama serve
   ```

3. **Download models**
   ```bash
   ollama pull qwen3-0.6b
   ```

4. **Verify installation**
   ```bash
   ollama list
   ```

### LM Studio Setup

1. **Download LM Studio**
   - Visit [https://lmstudio.ai](https://lmstudio.ai)
   - Download for your operating system (Windows, macOS, Linux)

2. **Install and Launch**
   - Install the downloaded application
   - Launch LM Studio

3. **Download Models**
   - Use the built-in model browser
   - Search for models like:
     - `microsoft/Phi-3-mini-4k-instruct-gguf`
     - `meta-llama/Llama-2-7b-chat-gguf`
     - `mistralai/Mistral-7B-Instruct-v0.1-gguf`

4. **Start Local Server**
   - Go to the "Local Server" tab
   - Select a downloaded model
   - Click "Start Server"
   - Default endpoint: `http://localhost:1234/v1`

### Verifying Local Model Setup

Once you have either Ollama or LM Studio running:

1. **Check Ollama** (default: `http://localhost:11434`)
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Check LM Studio** (default: `http://localhost:1234`)
   ```bash
   curl http://localhost:1234/v1/models
   ```

3. **In the Application**
   - Open the model selection drawer
   - Click "Refresh" to fetch available local models
   - Local models will appear in the respective sections

## API Keys Setup

### OpenRouter
1. Visit [https://openrouter.ai](https://openrouter.ai)
2. Sign up for an account
3. Navigate to API Keys section
4. Generate a new API key
5. Add to your `.env` file as `OPENROUTER_API_KEY`

## Usage

### Starting a Chat
1. Launch the application with `reflex run`
2. Select your preferred AI model from the dropdown
   - **Online models**: Requires internet connection
   - **Local models**: No internet connection required
3. Start typing your message in the chat input
4. Press Enter or click Send to get a response

### Using Turbo Mode
- Select "Qwen3-32B (Cerebras)" from the model dropdown for ultra-fast responses
- **Requires internet connection**
- Ideal for quick questions and rapid iterations

### Local Model Chat
- Ensure Ollama or LM Studio is running
- Refresh the model list to see available local models
- Select a local model and start chatting offline
- **No internet connection required**

### Search with Perplexity
- Use the search functionality to get web-based answers
- **Requires internet connection**
- Automatic citation extraction provides source information

## Project Structure

```
ark/
├── ark/                    # Main application code
│   ├── components/         # Reusable UI components
│   ├── pages/             # Application pages
│   ├── services/          # External service integrations
│   └── state.py           # Application state management
├── data/                  # Data files (changelog, etc.)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the documentation above
- Review local model setup instructions
- Ensure all API keys are properly configured
- Verify local model services are running