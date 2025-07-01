import reflex as rx
from ark.state import State
from ark.components.navigation.nav import navbar


def feature_card(
    icon: str, title: str, description: str, color_scheme: str
) -> rx.Component:
    """Interactive feature card component"""
    return rx.box(
        rx.flex(
            rx.icon(
                icon,
                size=24,
                class_name=f"text-{color_scheme}-500 mb-2 md:mb-4 w-6 h-6 md:w-8 md:h-8",
            ),
            rx.heading(
                title,
                size=rx.breakpoints(initial="4", md="6"),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-white font-bold mb-2 md:mb-3",
                    "text-gray-900 font-bold mb-2 md:mb-3",
                ),
            ),
            rx.text(
                description,
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-gray-300 leading-snug md:leading-relaxed text-sm md:text-base",
                    "text-gray-600 leading-snug md:leading-relaxed text-sm md:text-base",
                ),
            ),
            direction="column",
            align="start",
        ),
        class_name=rx.cond(
            State.is_dark_theme,
            f"p-3 md:p-6 rounded-lg md:rounded-xl bg-gray-800/50 border border-gray-700/50 hover:bg-gray-800/70 hover:border-{color_scheme}-500/30 transition-all duration-300 cursor-pointer transform hover:scale-105",
            f"p-3 md:p-6 rounded-lg md:rounded-xl bg-white border border-gray-200 hover:bg-gray-50 hover:border-{color_scheme}-500/30 transition-all duration-300 cursor-pointer transform hover:scale-105 shadow-sm hover:shadow-md",
        ),
    )


def tech_stack_item(name: str, description: str, icon: str, color: str) -> rx.Component:
    """Interactive technology stack item"""
    return rx.box(
        rx.flex(
            rx.box(
                rx.icon(
                    icon,
                    size=20,
                    class_name=f"text-{color}-500 w-5 h-5 md:w-6 md:h-6",
                ),
                class_name=f"p-2 md:p-3 rounded-md md:rounded-lg bg-{color}-100/80 dark:bg-{color}-900/30",
            ),
            rx.flex(
                rx.text(
                    name,
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "font-semibold text-white text-base md:text-lg",
                        "font-semibold text-gray-900 text-base md:text-lg",
                    ),
                ),
                rx.text(
                    description,
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "text-gray-400 text-xs md:text-sm",
                        "text-gray-700 text-xs md:text-sm",
                    ),
                ),
                direction="column",
                align="start",
                class_name="ml-3 md:ml-4",
            ),
            align="center",
            class_name="w-full",
        ),
        class_name=rx.cond(
            State.is_dark_theme,
            "p-3 md:p-4 rounded-md md:rounded-lg border border-gray-700/50 hover:border-gray-600/50 transition-all duration-200 hover:bg-gray-800/30",
            "p-3 md:p-4 rounded-md md:rounded-lg border border-gray-200 hover:border-gray-300 transition-all duration-200 hover:bg-gray-50",
        ),
    )


def architecture_diagram() -> rx.Component:
    """Interactive architecture flow diagram"""
    return rx.box(
        rx.heading(
            "System Architecture Flow",
            size=rx.breakpoints(initial="5", md="7"),
            class_name=rx.cond(
                State.is_dark_theme,
                "text-white font-bold mb-4 md:mb-8 text-center",
                "text-gray-900 font-bold mb-4 md:mb-8 text-center",
            ),
        ),
        rx.flex(
            # User Input Layer
            rx.box(
                rx.flex(
                    rx.icon(
                        "user",
                        size=24,
                        class_name="text-blue-500 mb-2 w-6 h-6 md:w-8 md:h-8",
                    ),
                    rx.text("User Input", class_name="font-bold text-base md:text-lg"),
                    rx.text(
                        "Text, Images, PDFs", class_name="text-xs md:text-sm opacity-75"
                    ),
                    direction="column",
                    align="center",
                ),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "p-4 md:p-6 rounded-lg md:rounded-xl bg-blue-900/20 border border-blue-500/30 hover:bg-blue-900/30 transition-all duration-300",
                    "p-4 md:p-6 rounded-lg md:rounded-xl bg-blue-50 border border-blue-200 hover:bg-blue-100 transition-all duration-300",
                ),
            ),
            # Arrow
            rx.icon(
                "arrow-down",
                size=20,
                class_name="text-gray-500 my-2 md:my-4 w-5 h-5 md:w-6 md:h-6",
            ),
            # State Management
            rx.box(
                rx.flex(
                    rx.icon("cpu", size=32, class_name="text-purple-500 mb-2"),
                    rx.text("State Management", class_name="font-bold text-lg"),
                    rx.text("Reflex State Handler", class_name="text-sm opacity-75"),
                    direction="column",
                    align="center",
                ),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "p-6 rounded-xl bg-purple-900/20 border border-purple-500/30 hover:bg-purple-900/30 transition-all duration-300",
                    "p-6 rounded-xl bg-purple-50 border border-purple-200 hover:bg-purple-100 transition-all duration-300",
                ),
            ),
            # Arrow
            rx.icon(
                "arrow-down",
                size=20,
                class_name="text-gray-500 my-2 md:my-4 w-5 h-5 md:w-6 md:h-6",
            ),
            # Processing Layer
            rx.flex(
                rx.box(
                    rx.flex(
                        rx.icon(
                            "cloud",
                            size=20,
                            class_name="text-green-500 mb-1 md:mb-2 w-5 h-5 md:w-7 md:h-7",
                        ),
                        rx.text(
                            "File Storage", class_name="font-bold text-sm md:text-base"
                        ),
                        rx.text("Cloudflare R2", class_name="text-xs opacity-75"),
                        direction="column",
                        align="center",
                    ),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "p-3 md:p-4 rounded-md md:rounded-lg bg-green-900/20 border border-green-500/30 hover:bg-green-900/30 transition-all duration-300 flex-1",
                        "p-3 md:p-4 rounded-md md:rounded-lg bg-green-50 border border-green-200 hover:bg-green-100 transition-all duration-300 flex-1",
                    ),
                ),
                rx.box(
                    rx.flex(
                        rx.icon(
                            "brain",
                            size=20,
                            class_name="text-orange-500 mb-1 md:mb-2 w-5 h-5 md:w-7 md:h-7",
                        ),
                        rx.text("LLM", class_name="font-bold text-sm md:text-base"),
                        rx.text("OpenRouter", class_name="text-xs opacity-75"),
                        direction="column",
                        align="center",
                    ),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "p-3 md:p-4 rounded-md md:rounded-lg bg-orange-900/20 border border-orange-500/30 hover:bg-orange-900/30 transition-all duration-300 flex-1",
                        "p-3 md:p-4 rounded-md md:rounded-lg bg-orange-50 border border-orange-200 hover:bg-orange-100 transition-all duration-300 flex-1",
                    ),
                ),
                rx.box(
                    rx.flex(
                        rx.icon(
                            "database",
                            size=20,
                            class_name="text-red-500 mb-1 md:mb-2 w-5 h-5 md:w-7 md:h-7",
                        ),
                        rx.text(
                            "Database", class_name="font-bold text-sm md:text-base"
                        ),
                        rx.text("PostgreSQL", class_name="text-xs opacity-75"),
                        direction="column",
                        align="center",
                    ),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "p-3 md:p-4 rounded-md md:rounded-lg bg-red-900/20 border border-red-500/30 hover:bg-red-900/30 transition-all duration-300 flex-1",
                        "p-3 md:p-4 rounded-md md:rounded-lg bg-red-50 border border-red-200 hover:bg-red-100 transition-all duration-300 flex-1",
                    ),
                ),
                class_name="gap-4 w-full",
                direction="row",
            ),
            # Arrow
            rx.icon(
                "arrow-down",
                size=20,
                class_name="text-gray-500 my-2 md:my-4 w-5 h-5 md:w-6 md:h-6",
            ),
            # Output Layer
            rx.box(
                rx.flex(
                    rx.icon(
                        "message_circle",
                        size=24,
                        class_name="text-cyan-500 mb-2 w-6 h-6 md:w-8 md:h-8",
                    ),
                    rx.text("Streaming Response", class_name="font-bold text-lg"),
                    rx.text("Real-time AI Chat", class_name="text-sm opacity-75"),
                    direction="column",
                    align="center",
                ),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "p-6 rounded-xl bg-cyan-900/20 border border-cyan-500/30 hover:bg-cyan-900/30 transition-all duration-300",
                    "p-6 rounded-xl bg-cyan-50 border border-cyan-200 hover:bg-cyan-100 transition-all duration-300",
                ),
            ),
            direction="column",
            align="center",
            class_name="max-w-md mx-auto",
        ),
        class_name="mb-16",
    )


def interactive_demo_section() -> rx.Component:
    """Interactive demo section"""
    return rx.box(
        rx.heading(
            "Try It Yourself",
            size=rx.breakpoints(initial="6", md="8"),
            class_name=rx.cond(
                State.is_dark_theme,
                "text-white font-bold mb-4 md:mb-6 text-center",
                "text-gray-900 font-bold mb-4 md:mb-6 text-center",
            ),
        ),
        rx.text(
            "Ready to experience Ark's capabilities? Click below to start chatting with AI!",
            class_name=rx.cond(
                State.is_dark_theme,
                "text-gray-300 text-center mb-6 md:mb-8 text-base md:text-lg",
                "text-gray-600 text-center mb-6 md:mb-8 text-base md:text-lg",
            ),
        ),
        rx.flex(
            rx.button(
                rx.flex(
                    rx.icon(
                        "message_circle",
                        size=24,
                        class_name="text-white mr-3 md:mr-4",
                    ),
                    rx.text(
                        "Start Chatting",
                        class_name="text-white font-bold text-xl md:text-2xl",
                    ),
                    align="center",
                ),
                class_name=(
                    "px-8 md:px-12 py-6 md:py-8 rounded-2xl md:rounded-3xl text-white transition-all duration-300 font-bold "
                    "shadow-[0px_8px_0px_0px_rgb(59,130,246,0.8)] md:shadow-[0px_12px_0px_0px_rgb(59,130,246,0.8)] "
                    "hover:shadow-[0px_12px_0px_0px_rgb(59,130,246,1.0)] md:hover:shadow-[0px_16px_0px_0px_rgb(59,130,246,1.0)] "
                    "hover:brightness-110 active:shadow-[0px_4px_0px_0px_rgb(59,130,246,0.8)] md:active:shadow-[0px_8px_0px_0px_rgb(59,130,246,0.8)] active:translate-y-2 "
                    "transform hover:scale-105 hover:-translate-y-1"
                ),
                style={
                    "background": "linear-gradient(135deg, #3b82f6 0%, #60a5fa 30%, #93c5fd 70%, #dbeafe 100%)",
                    "border": "3px solid rgba(59,130,246,0.9)",
                    "boxShadow": "inset 0 2px 4px rgba(255,255,255,0.3)",
                },
                on_click=rx.redirect("/"),
            ),
            class_name="justify-center",
        ),
        class_name="text-center p-6 md:p-10 rounded-2xl md:rounded-3xl border-2 border-dashed border-blue-300 dark:border-blue-600 bg-gradient-to-br from-blue-50/40 to-indigo-50/40 dark:from-blue-900/20 dark:to-indigo-900/20",
    )


def how_it_works_page() -> rx.Component:
    """Main how it works page component"""
    return rx.box(
        navbar(),
        rx.box(
            # Hero section
            rx.box(
                rx.heading(
                    "How Ark Works",
                    size=rx.breakpoints(initial="7", md="9"),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "text-white font-bold mb-4 md:mb-6 text-center",
                        "text-gray-900 font-bold mb-4 md:mb-6 text-center",
                    ),
                ),
                rx.text(
                    "Discover the technology and architecture behind Ark's powerful AI chat platform. From multi-modal conversations to real-time streaming responses, learn how everything works together seamlessly.",
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "text-gray-300 text-center text-base md:text-xl leading-relaxed mb-8 md:mb-12 max-w-4xl mx-auto px-4",
                        "text-gray-600 text-center text-base md:text-xl leading-relaxed mb-8 md:mb-12 max-w-4xl mx-auto px-4",
                    ),
                ),
                class_name="pt-8 md:pt-16 pb-4 md:pb-8",
            ),
            # Key Features Grid
            rx.box(
                rx.heading(
                    "Key Features",
                    size=rx.breakpoints(initial="6", md="8"),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "text-white font-bold mb-4 md:mb-8 text-center",
                        "text-gray-900 font-bold mb-4 md:mb-8 text-center",
                    ),
                ),
                rx.grid(
                    feature_card(
                        "zap",
                        "Real-time Streaming",
                        "Experience lightning-fast AI responses with token-by-token streaming. Watch as thoughts form in real-time, making conversations feel natural and immediate.",
                        "yellow",
                    ),
                    feature_card(
                        "upload",
                        "Multi-modal Chat",
                        "Upload images and PDFs directly into conversations. Ark intelligently processes visual content and documents, enabling rich, context-aware discussions.",
                        "blue",
                    ),
                    feature_card(
                        "database",
                        "Persistent History",
                        "Never lose a conversation. All chats are automatically saved to PostgreSQL with full search capabilities and organized history management.",
                        "green",
                    ),
                    feature_card(
                        "search",
                        "Web Search Integration",
                        "Get up-to-date information with Perplexity-powered web search. Responses include citations and sources for fact-checking and further reading.",
                        "purple",
                    ),
                    feature_card(
                        "cloud",
                        "Cloud File Storage",
                        "Files are securely stored in Cloudflare R2 with automatic presigned URL generation. Efficient, scalable, and reliable file management.",
                        "cyan",
                    ),
                    feature_card(
                        "shield",
                        "Secure Authentication",
                        "Powered by Clerk authentication with automatic user state management. Your data is protected with enterprise-grade security.",
                        "red",
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    spacing=rx.breakpoints(initial="3", md="6"),
                    class_name="mb-8 md:mb-16",
                ),
            ),
            # Architecture Diagram
            architecture_diagram(),
            # Technology Stack
            rx.box(
                rx.heading(
                    "Technology Stack",
                    size=rx.breakpoints(initial="6", md="8"),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "text-white font-bold mb-4 md:mb-8 text-center",
                        "text-gray-900 font-bold mb-4 md:mb-8 text-center",
                    ),
                ),
                rx.grid(
                    tech_stack_item(
                        "Reflex Framework",
                        "Python-based reactive web framework for building modern UIs",
                        "code",
                        "blue",
                    ),
                    tech_stack_item(
                        "OpenRouter",
                        "Access to multiple AI models including Gemini 2.5 Flash and Perplexity",
                        "brain",
                        "purple",
                    ),
                    tech_stack_item(
                        "PostgreSQL (Neon)",
                        "Scalable database for chat persistence and user management",
                        "database",
                        "green",
                    ),
                    tech_stack_item(
                        "Cloudflare R2",
                        "Object storage for images and PDFs with CDN performance",
                        "cloud",
                        "orange",
                    ),
                    tech_stack_item(
                        "Clerk Auth",
                        "Modern authentication with user management and security",
                        "shield",
                        "red",
                    ),
                    tech_stack_item(
                        "Real-time Streaming",
                        "Async generators for live AI response streaming",
                        "zap",
                        "yellow",
                    ),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing=rx.breakpoints(initial="2", md="4"),
                    class_name="mb-8 md:mb-16",
                ),
            ),
            # How It Works Steps
            rx.box(
                rx.heading(
                    "How It All Works Together",
                    size=rx.breakpoints(initial="6", md="8"),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "text-white font-bold mb-4 md:mb-8 text-center",
                        "text-gray-900 font-bold mb-4 md:mb-8 text-center",
                    ),
                ),
                rx.flex(
                    rx.box(
                        rx.flex(
                            rx.box(
                                rx.text(
                                    "1", class_name="text-2xl font-bold text-white"
                                ),
                                class_name="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center mb-4",
                            ),
                            rx.heading(
                                "User Input",
                                size=rx.breakpoints(initial="4", md="6"),
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "mb-2 md:mb-3 font-bold text-white",
                                    "mb-2 md:mb-3 font-bold text-gray-900",
                                ),
                            ),
                            rx.text(
                                "Users interact through the clean, responsive interface built with Reflex. The interface supports multiple input methods:",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "text-gray-300 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                    "text-gray-700 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                ),
                            ),
                            rx.box(
                                rx.text(
                                    "• Text messages and questions",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Image uploads (PNG, JPEG) with drag & drop support",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• PDF document uploads for analysis",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Progressive Web App (PWA) capabilities",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                class_name="ml-3 space-y-1",
                            ),
                            direction="column",
                            align="start",
                        ),
                        class_name="flex-1",
                    ),
                    rx.box(
                        rx.flex(
                            rx.box(
                                rx.text(
                                    "2", class_name="text-2xl font-bold text-white"
                                ),
                                class_name="w-12 h-12 rounded-full bg-purple-500 flex items-center justify-center mb-4",
                            ),
                            rx.heading(
                                "State Management",
                                size=rx.breakpoints(initial="4", md="6"),
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "mb-2 md:mb-3 font-bold text-white",
                                    "mb-2 md:mb-3 font-bold text-gray-900",
                                ),
                            ),
                            rx.text(
                                "The centralized State class orchestrates all application operations using Reflex's reactive state system:",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "text-gray-300 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                    "text-gray-700 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                ),
                            ),
                            rx.box(
                                rx.text(
                                    "• File upload processing with Cloudflare R2 integration",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• User authentication and session management via Clerk",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Chat persistence and message history tracking",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Provider and model selection management",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Real-time UI state updates and streaming control",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                class_name="ml-3 space-y-1",
                            ),
                            direction="column",
                            align="start",
                        ),
                        class_name="flex-1",
                    ),
                    rx.box(
                        rx.flex(
                            rx.box(
                                rx.text(
                                    "3", class_name="text-2xl font-bold text-white"
                                ),
                                class_name="w-12 h-12 rounded-full bg-green-500 flex items-center justify-center mb-4",
                            ),
                            rx.heading(
                                "AI Processing",
                                size=rx.breakpoints(initial="4", md="6"),
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "mb-2 md:mb-3 font-bold text-white",
                                    "mb-2 md:mb-3 font-bold text-gray-900",
                                ),
                            ),
                            rx.text(
                                "Advanced AI processing through OpenRouter's unified API gateway with intelligent model routing:",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "text-gray-300 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                    "text-gray-700 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                ),
                            ),
                            rx.box(
                                rx.text(
                                    "• Google Gemini 2.5 Flash for general chat conversations",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Perplexity Sonar Pro for web search with citations",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Multi-modal processing for images and PDFs",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Smart file encoding (presigned URLs for images, base64 for PDFs)",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                class_name="ml-3 space-y-1",
                            ),
                            direction="column",
                            align="start",
                        ),
                        class_name="flex-1",
                    ),
                    rx.box(
                        rx.flex(
                            rx.box(
                                rx.text(
                                    "4", class_name="text-2xl font-bold text-white"
                                ),
                                class_name="w-12 h-12 rounded-full bg-orange-500 flex items-center justify-center mb-4",
                            ),
                            rx.heading(
                                "Real-time Response",
                                size=rx.breakpoints(initial="4", md="6"),
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "mb-2 md:mb-3 font-bold text-white",
                                    "mb-2 md:mb-3 font-bold text-gray-900",
                                ),
                            ),
                            rx.text(
                                "Advanced real-time streaming architecture provides immediate, natural conversation experiences:",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "text-gray-300 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                    "text-gray-700 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                ),
                            ),
                            rx.box(
                                rx.text(
                                    "• Token-by-token streaming using async generators",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Live UI updates with responsive state management",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Automatic citation extraction from search responses",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Content accumulation with reasoning and tool calls",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Smart loading indicators and streaming states",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                class_name="ml-3 space-y-1",
                            ),
                            direction="column",
                            align="start",
                        ),
                        class_name="flex-1",
                    ),
                    rx.box(
                        rx.flex(
                            rx.box(
                                rx.text(
                                    "5", class_name="text-2xl font-bold text-white"
                                ),
                                class_name="w-12 h-12 rounded-full bg-red-500 flex items-center justify-center mb-4",
                            ),
                            rx.heading(
                                "Persistence",
                                size=rx.breakpoints(initial="4", md="6"),
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "mb-2 md:mb-3 font-bold text-white",
                                    "mb-2 md:mb-3 font-bold text-gray-900",
                                ),
                            ),
                            rx.text(
                                "Comprehensive data persistence system ensures no conversation or file is ever lost:",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "text-gray-300 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                    "text-gray-700 leading-snug md:leading-relaxed text-sm md:text-base mb-2",
                                ),
                            ),
                            rx.box(
                                rx.text(
                                    "• PostgreSQL database with users, chats, messages, and files tables",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Automatic chat history with searchable message content",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• File metadata tracking with user and chat associations",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• R2 cloud file lifecycle management and cleanup",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                rx.text(
                                    "• Performance stats and citation data preservation",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-gray-400 text-xs md:text-sm",
                                        "text-gray-600 text-xs md:text-sm",
                                    ),
                                ),
                                class_name="ml-3 space-y-1",
                            ),
                            direction="column",
                            align="start",
                        ),
                        class_name="flex-1",
                    ),
                    direction="column",
                    spacing=rx.breakpoints(initial="4", md="8"),
                    class_name="mb-8 md:mb-16",
                ),
            ),
            # Interactive Demo Section
            interactive_demo_section(),
            class_name="max-w-7xl mx-auto px-2 md:px-4 pb-8 md:pb-16",
        ),
        class_name=rx.cond(
            State.is_dark_theme,
            "min-h-screen bg-gray-950 text-gray-50 transition-colors duration-300",
            "min-h-screen bg-white text-gray-900 transition-colors duration-300",
        ),
    )
