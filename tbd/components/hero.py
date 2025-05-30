import reflex as rx
from tbd.state import State
from typing import List
from tbd.services.openrouter import get_ollama_models, get_lmstudio_models


class OfflineModelsState(rx.State):
    """State management for the offline models bottom drawer"""

    is_open: bool = False
    selected_provider: str = "ollama"  # "ollama" or "lmstudio"
    selected_model: str = ""  # Track selected model

    # Dynamic model lists
    ollama_models: List[str] = []
    lmstudio_models: List[str] = []

    # Connection status
    ollama_connected: bool = False
    lmstudio_connected: bool = False

    def refresh_ollama_models(self):
        """Refresh Ollama models"""
        try:
            models = get_ollama_models()
            self.ollama_models = models
            self.ollama_connected = len(models) > 0
        except Exception as e:
            print(f"Error refreshing Ollama models: {e}")
            self.ollama_models = []
            self.ollama_connected = False

    def refresh_lmstudio_models(self):
        """Refresh LM Studio models"""
        try:
            models = get_lmstudio_models()
            self.lmstudio_models = models
            self.lmstudio_connected = len(models) > 0
        except Exception as e:
            print(f"Error refreshing LM Studio models: {e}")
            self.lmstudio_models = []
            self.lmstudio_connected = False

    def refresh_all_models(self):
        """Refresh models for both providers"""
        self.refresh_ollama_models()
        self.refresh_lmstudio_models()

    def toggle_drawer(self):
        """Toggle the drawer open/closed"""
        self.is_open = not self.is_open
        if self.is_open:
            # Automatically refresh models when opening
            self.refresh_all_models()

    def open_drawer(self):
        """Open the drawer"""
        self.is_open = True
        # Automatically refresh models when opening
        self.refresh_all_models()

    def close_drawer(self):
        """Close the drawer"""
        self.is_open = False

    def select_provider(self, provider: str):
        """Select model provider (ollama or lmstudio)"""
        self.selected_provider = provider

    async def select_model(self, model: str):
        """Select a specific model and close drawer"""
        self.selected_model = model
        print(f"Selected model: {model} from {self.selected_provider}")

        # Update the main State with the selected provider and model
        from tbd.state import State

        state = await self.get_state(State)
        state.set_provider_and_model(self.selected_provider, model)

        self.close_drawer()


def offline_models_overlay() -> rx.Component:
    """Creates the backdrop overlay for the bottom drawer"""
    return rx.box(
        width="100%",
        height="100%",
        position="fixed",
        top="0",
        left="0",
        background_color="rgba(0, 0, 0, 0.5)",
        z_index="999",
        display=rx.cond(OfflineModelsState.is_open, "block", "none"),
        on_click=OfflineModelsState.close_drawer,
        class_name="backdrop-blur-sm",
    )


def model_item(model_name: str, provider: str) -> rx.Component:
    """Individual model item component"""
    return rx.box(
        rx.flex(
            rx.box(
                rx.image(
                    src=f"/{provider}.png",
                    alt=f"{provider} logo",
                    width="20px",
                    height="20px",
                    class_name="object-contain",
                ),
                class_name="flex-shrink-0",
            ),
            rx.box(
                rx.text(model_name, class_name="font-[dm] font-medium text-sm"),
                class_name="flex-1 min-w-0",
            ),
            rx.icon("chevron-right", size=16, color="#9CA3AF"),
            align="center",
            class_name="w-full gap-3",
        ),
        on_click=lambda: OfflineModelsState.select_model(model_name),
        class_name="p-3 hover:bg-gray-50 cursor-pointer transition-colors duration-150 border-b border-gray-100 last:border-b-0",
    )


def provider_tab(provider: str, label: str, image_src: str) -> rx.Component:
    """Provider tab component with connection status indicator"""
    is_active = OfflineModelsState.selected_provider == provider

    # Determine connection status based on provider
    is_connected = rx.cond(
        provider == "ollama",
        OfflineModelsState.ollama_connected,
        OfflineModelsState.lmstudio_connected,
    )

    return rx.button(
        rx.flex(
            rx.image(
                src=image_src,
                alt=f"{provider} logo",
                width="18px",
                height="18px",
                class_name="object-contain",
            ),
            rx.text(label, class_name="font-[dm] font-medium text-sm"),
            # Status indicator
            rx.box(
                class_name=rx.cond(
                    is_connected,
                    "w-2 h-2 bg-green-500 rounded-full",
                    "w-2 h-2 bg-red-500 rounded-full",
                )
            ),
            align="center",
            justify="center",
            class_name="gap-2",
        ),
        on_click=lambda: OfflineModelsState.select_provider(provider),
        class_name=rx.cond(
            is_active,
            "flex-1 py-2 px-4 bg-gray-200 text-gray-900 rounded-lg transition-all duration-200",
            "flex-1 py-2 px-4 bg-gray-50 text-gray-700 hover:bg-gray-100 rounded-lg transition-all duration-200",
        ),
    )


def offline_models_content() -> rx.Component:
    """The actual bottom drawer content"""
    return rx.box(
        # Sheet container
        rx.box(
            # Handle bar
            rx.box(
                width="40px",
                height="4px",
                background_color="#D1D5DB",
                border_radius="2px",
                margin="12px auto 20px auto",
                class_name="cursor-pointer",
            ),
            # Header
            rx.flex(
                rx.heading(
                    "Offline Models",
                    size="5",
                    class_name="font-[dm] font-bold",
                ),
                rx.button(
                    rx.icon("x", size=20),
                    on_click=OfflineModelsState.close_drawer,
                    class_name="p-2 hover:bg-gray-100 rounded-full",
                    variant="surface",
                ),
                justify="between",
                align="center",
                class_name="mb-6",
            ),
            # Provider tabs
            rx.flex(
                provider_tab("ollama", "Ollama", "/ollama.png"),
                provider_tab("lmstudio", "LM Studio", "/lmstudio.png"),
                gap="2",
                class_name="mb-6 p-1 bg-gray-50 rounded-xl",
            ),
            # Models list
            rx.box(
                rx.cond(
                    OfflineModelsState.selected_provider == "ollama",
                    # Ollama models section
                    rx.cond(
                        OfflineModelsState.ollama_connected,
                        # Connected - show models
                        rx.cond(
                            OfflineModelsState.ollama_models.length() > 0,
                            rx.box(
                                rx.foreach(
                                    OfflineModelsState.ollama_models,
                                    lambda model: model_item(model, "ollama"),
                                ),
                                class_name="bg-white rounded-xl border border-gray-200 overflow-hidden",
                            ),
                            # Connected but no models
                            rx.box(
                                rx.flex(
                                    rx.icon("inbox", size=24, color="#9CA3AF"),
                                    rx.text(
                                        "No models found",
                                        class_name="font-[dm] text-sm font-medium text-gray-700",
                                    ),
                                    rx.text(
                                        "Make sure you have models installed in Ollama",
                                        class_name="font-[dm] text-xs text-gray-500",
                                    ),
                                    direction="column",
                                    align="center",
                                    class_name="gap-2",
                                ),
                                class_name="bg-white rounded-xl border border-gray-200 p-6 text-center",
                            ),
                        ),
                        # Not connected
                        rx.box(
                            rx.flex(
                                rx.icon("wifi-off", size=24, color="#EF4444"),
                                rx.text(
                                    "Ollama not available",
                                    class_name="font-[dm] text-sm font-medium text-gray-700",
                                ),
                                rx.text(
                                    "Make sure Ollama is running on localhost:11434",
                                    class_name="font-[dm] text-xs text-gray-500",
                                ),
                                rx.button(
                                    rx.icon("refresh-cw", size=14),
                                    "Retry",
                                    on_click=OfflineModelsState.refresh_ollama_models,
                                    size="1",
                                    variant="outline",
                                    class_name="mt-2 font-[dm] bg-white hover:bg-gray-50 border-gray-300 text-gray-700",
                                ),
                                direction="column",
                                align="center",
                                class_name="gap-2",
                            ),
                            class_name="bg-white rounded-xl border border-gray-200 p-6 text-center",
                        ),
                    ),
                    # LM Studio models section
                    rx.cond(
                        OfflineModelsState.lmstudio_connected,
                        # Connected - show models
                        rx.cond(
                            OfflineModelsState.lmstudio_models.length() > 0,
                            rx.box(
                                rx.foreach(
                                    OfflineModelsState.lmstudio_models,
                                    lambda model: model_item(model, "lmstudio"),
                                ),
                                class_name="bg-white rounded-xl border border-gray-200 overflow-hidden",
                            ),
                            # Connected but no models
                            rx.box(
                                rx.flex(
                                    rx.icon("inbox", size=24, color="#9CA3AF"),
                                    rx.text(
                                        "No models found",
                                        class_name="font-[dm] text-sm font-medium text-gray-700",
                                    ),
                                    rx.text(
                                        "Make sure you have models loaded in LM Studio",
                                        class_name="font-[dm] text-xs text-gray-500",
                                    ),
                                    direction="column",
                                    align="center",
                                    class_name="gap-2",
                                ),
                                class_name="bg-white rounded-xl border border-gray-200 p-6 text-center",
                            ),
                        ),
                        # Not connected
                        rx.box(
                            rx.flex(
                                rx.icon("wifi-off", size=24, color="#EF4444"),
                                rx.text(
                                    "LM Studio not available",
                                    class_name="font-[dm] text-sm font-medium text-gray-700",
                                ),
                                rx.text(
                                    "Make sure LM Studio is running on localhost:1234",
                                    class_name="font-[dm] text-xs text-gray-500",
                                ),
                                rx.button(
                                    rx.icon("refresh-cw", size=14),
                                    "Retry",
                                    on_click=OfflineModelsState.refresh_lmstudio_models,
                                    size="1",
                                    variant="outline",
                                    class_name="mt-2 font-[dm] bg-white hover:bg-gray-50 border-gray-300 text-gray-700",
                                ),
                                direction="column",
                                align="center",
                                class_name="gap-2",
                            ),
                            class_name="bg-white rounded-xl border border-gray-200 p-6 text-center",
                        ),
                    ),
                ),
                class_name="h-80 overflow-y-auto",
            ),
            # Footer info
            rx.box(
                rx.text(
                    "Select a model to start chatting offline",
                    class_name="font-[dm] text-sm text-gray-500 text-center",
                ),
                class_name="mt-6 pt-4 border-t border-gray-100",
            ),
            padding="0 24px 32px 24px",
            background_color="white",
            border_radius="20px 20px 0 0",
            box_shadow="0 -4px 20px rgba(0, 0, 0, 0.1)",
            class_name="max-h-[80vh] w-full max-w-md mx-auto md:max-w-lg",
        ),
        # Sheet positioning and animation
        position="fixed",
        bottom="0",
        left="0",
        right="0",
        z_index="1000",
        transform=rx.cond(
            OfflineModelsState.is_open, "translateY(0)", "translateY(100%)"
        ),
        transition="transform 0.3s cubic-bezier(0.32, 0.72, 0, 1)",
        class_name="flex justify-center",
    )


def input_section():
    return (
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        value=State.prompt,
                        class_name="w-full font-[dm] mt-4 mx-auto text-black text-lg md:text-2xl bg-white rounded-2xl h-16 shadow-lg border-2 border-gray-600",
                        placeholder="Ask Anything...",
                        on_change=State.set_prompt,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("arrow-up", size=28, color="black"),
                            class_name="flex items-center justify-center",
                        ),
                        class_name="mt-4 mx-auto text-black bg-[#d5d5d0] hover:bg-[#b8b8b0] rounded-2xl h-16 px-4 md:px-8",
                        on_click=[
                            rx.redirect("/chat"),
                            State.handle_generation,
                            State.send_message,
                        ],
                        loading=State.is_gen,
                        disabled=State.is_gen,
                    ),
                    class_name="w-full flex gap-1 items-center justify-center max-w-4xl mx-auto",
                ),
                rx.cond(
                    State.current_url == "/",
                    rx.hstack(
                        rx.button(
                            rx.hstack(
                                rx.icon(
                                    "globe",
                                    size=16,
                                    class_name=rx.cond(
                                        State.selected_action == "Search",
                                        "text-white",
                                        "text-gray-600",
                                    ),
                                ),
                                rx.text(
                                    "Search",
                                    class_name=rx.cond(
                                        State.selected_action == "Search",
                                        "font-[dm] text-xs md:text-sm font-semibold text-white",
                                        "font-[dm] text-xs md:text-sm font-semibold text-gray-600",
                                    ),
                                ),
                                class_name="items-center gap-1 md:gap-2",
                            ),
                            on_click=State.handle_search_click,
                            class_name=rx.cond(
                                State.selected_action == "Search",
                                "text-left px-2 py-1 md:p-4 rounded-2xl shadow-[0px_8px_0px_0px_rgba(34,197,94,0.8)] hover:shadow-[0px_4px_0px_0px_rgba(34,197,94,0.8)] hover:translate-y-1 transition-all duration-200 ml-2",
                                "text-left px-2 py-1 md:p-4 rounded-2xl shadow-[0px_4px_0px_0px_rgba(107,114,128,0.4)] hover:shadow-[0px_8px_0px_0px_rgba(34,197,94,0.8)] hover:translate-y-1 transition-all duration-200 ml-2",
                            ),
                            style=rx.cond(
                                State.selected_action == "Search",
                                {
                                    "background": "linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%)",
                                    "border": "1px solid #166534",
                                },
                                {
                                    "background": "white",
                                    "border": "1px solid #d1d5db",
                                },
                            ),
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon(
                                    "cloud-off",
                                    size=16,
                                    class_name=rx.cond(
                                        rx.cond(
                                            State.selected_action == "Offline",
                                            OfflineModelsState.selected_model != "",
                                            False,
                                        ),
                                        "text-white",
                                        "text-gray-600",
                                    ),
                                ),
                                rx.text(
                                    "Offline",
                                    class_name=rx.cond(
                                        rx.cond(
                                            State.selected_action == "Offline",
                                            OfflineModelsState.selected_model != "",
                                            False,
                                        ),
                                        "font-[dm] text-xs md:text-sm font-semibold text-white",
                                        "font-[dm] text-xs md:text-sm font-semibold text-gray-600",
                                    ),
                                ),
                                class_name="items-center gap-1 md:gap-2",
                            ),
                            on_click=[
                                State.select_action("Offline"),
                                OfflineModelsState.open_drawer,
                            ],
                            class_name=rx.cond(
                                rx.cond(
                                    State.selected_action == "Offline",
                                    OfflineModelsState.selected_model != "",
                                    False,
                                ),
                                "text-left px-2 py-1 md:p-4 rounded-2xl shadow-2xl shadow-purple-500/25 hover:shadow-purple-500/40 transition-all duration-200 ml-2",
                                "text-left px-2 py-1 md:p-4 rounded-2xl shadow-[0px_4px_0px_0px_rgba(107,114,128,0.4)] hover:shadow-2xl shadow-purple-500/25 hover:shadow-purple-500/40 transition-all duration-200 ml-2",
                            ),
                            style=rx.cond(
                                rx.cond(
                                    State.selected_action == "Offline",
                                    OfflineModelsState.selected_model != "",
                                    False,
                                ),
                                {
                                    "background": "linear-gradient(135deg, #9333ea 0%, #7c3aed 50%, #6d28d9 100%)",
                                    "border": "1px solid #5b21b6",
                                },
                                {
                                    "background": "white",
                                    "border": "1px solid #d1d5db",
                                },
                            ),
                        ),
                        class_name="gap-0",
                    ),
                ),
                class_name="w-full mx-auto max-w-4xl",
            ),
            class_name="fixed bottom-2 md:bottom-6 left-0 right-0 p-2 md:p-4",
        ),
    )


def card(
    title: str,
    description: str,
    image_src: str,
    background_color: str = "bg-gradient-to-br from-purple-500 to-pink-500",
):
    return rx.box(
        # Gradient border wrapper
        rx.box(
            # Inner card with glassmorphism effect
            rx.box(
                # Mobile: horizontal layout, Desktop: vertical layout
                rx.flex(
                    # Image container with glow effect
                    rx.box(
                        rx.box(
                            rx.image(
                                src=image_src,
                                class_name="w-24 md:w-36 h-24 md:h-36 object-contain relative z-10",
                            ),
                            class_name="relative",
                        ),
                        # Glow effect behind image
                        rx.box(
                            class_name="absolute inset-0 bg-gradient-to-r from-cyan-400 to-purple-400 blur-xl opacity-50",
                        ),
                        class_name="flex-shrink-0 mr-4 mt-3 md:mr-0 md:mb-8 relative",
                    ),
                    # Content container
                    rx.box(
                        # Title with gradient text
                        rx.heading(
                            title,
                            class_name="text-2xl md:text-4xl font-black mb-2 md:mb-4 tracking-wide bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent text-left",
                            as_="h2",
                        ),
                        # Description with modern styling
                        rx.text(
                            description,
                            class_name="font-[dm] text-base md:text-xl text-gray-700 font-medium text-left",
                        ),
                        class_name="flex-1",
                    ),
                    direction="row",
                    class_name="md:flex-col",
                    align="start",
                ),
                class_name="bg-white/90 backdrop-blur-md rounded-2xl md:rounded-3xl p-3 md:p-8 h-full flex flex-col relative overflow-hidden",
            ),
            class_name=f"{background_color} p-[2px] rounded-2xl md:rounded-3xl shadow-2xl shadow-purple-500/25 hover:shadow-purple-500/40 transition-all duration-300",
        ),
        class_name="transform hover:scale-[1.02] transition-transform duration-300",
    )


def hero():
    return (
        rx.box(
            rx.flex(
                rx.box(
                    rx.heading(
                        "Ask Anything!",
                        class_name="text-3xl md:text-6xl font-bold mb-8 md:mb-12 tracking-wide text-black",
                        as_="h1",
                    ),
                    rx.flex(
                        card(
                            title="Chat",
                            description="Engage in intelligent conversations powered by advanced AI technology.",
                            image_src="/go_pop.png",
                            background_color="bg-amber-200",
                        ),
                        card(
                            title="Search",
                            description="Find accurate information quickly with AI-powered search capabilities.",
                            image_src="/g_search.png",
                            background_color="bg-sky-200",
                        ),
                        card(
                            title="Learn",
                            description="Expand your knowledge with personalized learning experiences.",
                            image_src="/g_learn.png",
                            background_color="bg-purple-200",
                        ),
                        class_name="flex flex-col md:grid md:grid-cols-3 gap-3 md:gap-8 max-w-sm md:max-w-6xl mx-auto px-2 md:px-4",
                    ),
                    class_name="text-center",
                ),
                direction="column",
                align="center",
                justify="center",
            ),
            offline_models_overlay(),
            offline_models_content(),
            class_name="flex items-center justify-center min-h-[70vh] pb-4",
        ),
    )
