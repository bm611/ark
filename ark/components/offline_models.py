"""
Offline models component for provider selection.
"""

import reflex as rx
from typing import List
from ark.state import State
from ark.providers.manager import provider_manager
from rxconfig import config


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
            models = provider_manager.get_models_for_provider("ollama")
            self.ollama_models = models
            self.ollama_connected = len(models) > 0
        except Exception as e:
            print(f"Error refreshing Ollama models: {e}")
            self.ollama_models = []
            self.ollama_connected = False

    def refresh_lmstudio_models(self):
        """Refresh LM Studio models"""
        try:
            models = provider_manager.get_models_for_provider("lmstudio")
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
            # Only refresh models when running locally
            if "0.0.0.0" in config.api_url:
                self.refresh_all_models()

    def open_drawer(self):
        """Open the drawer"""
        self.is_open = True
        # Only refresh models when running locally
        if "0.0.0.0" in config.api_url:
            return self.refresh_all_models()
        else:
            # In hosted environment, just show the drawer without refreshing
            print("Skipping model refresh in hosted environment")

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
        background_color=rx.cond(
            State.is_dark_theme, "rgba(0, 0, 0, 0.7)", "rgba(0, 0, 0, 0.5)"
        ),
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
                rx.text(
                    model_name,
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "font-[dm] font-medium text-sm text-white",
                        "font-[dm] font-medium text-sm text-gray-900",
                    ),
                ),
                class_name="flex-1 min-w-0",
            ),
            rx.icon(
                "chevron-right",
                size=16,
                color=rx.cond(State.is_dark_theme, "#9CA3AF", "#6B7280"),
            ),
            align="center",
            class_name="w-full gap-3",
        ),
        on_click=lambda: OfflineModelsState.select_model(model_name),
        class_name=rx.cond(
            State.is_dark_theme,
            "p-3 hover:bg-gray-700 cursor-pointer transition-colors duration-150 border-b border-gray-600 last:border-b-0",
            "p-3 hover:bg-gray-50 cursor-pointer transition-colors duration-150 border-b border-gray-100 last:border-b-0",
        ),
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
            rx.text(
                label,
                class_name=rx.cond(
                    is_active,
                    "font-[dm] font-semibold text-sm text-white",
                    rx.cond(
                        State.is_dark_theme,
                        "font-[dm] font-medium text-sm text-gray-300",
                        "font-[dm] font-medium text-sm text-gray-700",
                    ),
                ),
            ),
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
            "flex-1 py-3 px-4 rounded-xl shadow-[0px_4px_0px_0px_rgba(147,51,234,0.6)] active:shadow-[0px_2px_0px_0px_rgba(147,51,234,0.6)] active:translate-y-1 transition-all duration-200 border-2 border-purple-600 md:hover:shadow-[0px_2px_0px_0px_rgba(147,51,234,0.6)] md:hover:translate-y-1",
            rx.cond(
                State.is_dark_theme,
                "flex-1 py-3 px-4 bg-gray-700 active:bg-gray-600 rounded-xl transition-all duration-200 border-2 border-gray-600 md:hover:bg-gray-600",
                "flex-1 py-3 px-4 bg-gray-50 active:bg-gray-100 rounded-xl transition-all duration-200 border-2 border-gray-200 md:hover:bg-gray-100",
            ),
        ),
        style=rx.cond(
            is_active,
            {
                "background": "linear-gradient(135deg, rgba(168,85,247,0.7) 0%, rgba(147,51,234,0.7) 50%, rgba(124,58,237,0.7) 100%)",
            },
            {},
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
                background_color=rx.cond(State.is_dark_theme, "#6B7280", "#D1D5DB"),
                border_radius="2px",
                margin="12px auto 20px auto",
                class_name="cursor-pointer",
            ),
            # Header
            rx.flex(
                rx.heading(
                    "Offline Models",
                    size="5",
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "font-[dm] font-bold text-white",
                        "font-[dm] font-bold text-gray-900",
                    ),
                ),
                rx.button(
                    rx.icon(
                        "x",
                        size=20,
                        color="black",
                    ),
                    on_click=OfflineModelsState.close_drawer,
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "p-2 active:bg-gray-700 rounded-xl border-2 border-gray-600 shadow-[0px_3px_0px_0px_rgba(75,85,99,0.8)] active:shadow-[0px_1px_0px_0px_rgba(75,85,99,0.8)] active:translate-y-1 transition-all duration-200 md:hover:bg-gray-700 md:hover:shadow-[0px_1px_0px_0px_rgba(75,85,99,0.8)] md:hover:translate-y-1",
                        "p-2 active:bg-gray-100 rounded-xl border-2 border-gray-300 shadow-[0px_3px_0px_0px_rgba(0,0,0,0.2)] active:shadow-[0px_1px_0px_0px_rgba(0,0,0,0.2)] active:translate-y-1 transition-all duration-200 md:hover:bg-gray-100 md:hover:shadow-[0px_1px_0px_0px_rgba(0,0,0,0.2)] md:hover:translate-y-1",
                    ),
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
                gap="3",
                class_name=rx.cond(
                    State.is_dark_theme,
                    "mb-6 p-2 bg-gray-800 rounded-2xl border-2 border-gray-600 shadow-[0px_4px_0px_0px_rgba(75,85,99,0.8)]",
                    "mb-6 p-2 bg-gray-50 rounded-2xl border-2 border-gray-200 shadow-[0px_4px_0px_0px_rgba(0,0,0,0.1)]",
                ),
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
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "bg-gray-800 rounded-2xl border-2 border-gray-600 overflow-hidden shadow-[0px_4px_0px_0px_rgba(75,85,99,0.8)]",
                                    "bg-white rounded-2xl border-2 border-gray-300 overflow-hidden shadow-[0px_4px_0px_0px_rgba(0,0,0,0.1)]",
                                ),
                            ),
                            # Connected but no models
                            rx.box(
                                rx.flex(
                                    rx.icon("inbox", size=24, color="#9CA3AF"),
                                    rx.text(
                                        "No models found",
                                        class_name=rx.cond(
                                            State.is_dark_theme,
                                            "font-[dm] text-sm font-medium text-white",
                                            "font-[dm] text-sm font-medium text-gray-700",
                                        ),
                                    ),
                                    rx.text(
                                        "Make sure you have models installed in Ollama",
                                        class_name=rx.cond(
                                            State.is_dark_theme,
                                            "font-[dm] text-xs text-gray-400",
                                            "font-[dm] text-xs text-gray-500",
                                        ),
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
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "font-[dm] text-sm font-medium text-white",
                                        "font-[dm] text-sm font-medium text-gray-700",
                                    ),
                                ),
                                rx.text(
                                    "Make sure Ollama is running on localhost:11434",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "font-[dm] text-xs text-gray-400",
                                        "font-[dm] text-xs text-gray-500",
                                    ),
                                ),
                                rx.button(
                                    rx.icon("refresh-cw", size=14),
                                    "Retry",
                                    on_click=OfflineModelsState.refresh_ollama_models,
                                    size="1",
                                    variant="outline",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "mt-2 font-[dm] bg-gray-700 active:bg-gray-600 border-gray-500 text-white rounded-xl border-2 shadow-[0px_2px_0px_0px_rgba(75,85,99,0.8)] active:shadow-[0px_1px_0px_0px_rgba(75,85,99,0.8)] active:translate-y-0.5 transition-all duration-200 md:hover:bg-gray-600 md:hover:shadow-[0px_1px_0px_0px_rgba(75,85,99,0.8)] md:hover:translate-y-0.5",
                                        "mt-2 font-[dm] bg-white active:bg-gray-50 border-gray-300 text-gray-700 rounded-xl border-2 shadow-[0px_2px_0px_0px_rgba(0,0,0,0.2)] active:shadow-[0px_1px_0px_0px_rgba(0,0,0,0.2)] active:translate-y-0.5 transition-all duration-200 md:hover:bg-gray-50 md:hover:shadow-[0px_1px_0px_0px_rgba(0,0,0,0.2)] md:hover:translate-y-0.5",
                                    ),
                                ),
                                direction="column",
                                align="center",
                                class_name="gap-2",
                            ),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "bg-gray-800 rounded-2xl border-2 border-gray-600 p-6 text-center shadow-[0px_4px_0px_0px_rgba(75,85,99,0.8)]",
                                "bg-white rounded-2xl border-2 border-gray-300 p-6 text-center shadow-[0px_4px_0px_0px_rgba(0,0,0,0.1)]",
                            ),
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
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "bg-gray-800 rounded-2xl border-2 border-gray-600 overflow-hidden shadow-[0px_4px_0px_0px_rgba(75,85,99,0.8)]",
                                    "bg-white rounded-2xl border-2 border-gray-300 overflow-hidden shadow-[0px_4px_0px_0px_rgba(0,0,0,0.1)]",
                                ),
                            ),
                            # Connected but no models
                            rx.box(
                                rx.flex(
                                    rx.icon("inbox", size=24, color="#9CA3AF"),
                                    rx.text(
                                        "No models found",
                                        class_name=rx.cond(
                                            State.is_dark_theme,
                                            "font-[dm] text-sm font-medium text-white",
                                            "font-[dm] text-sm font-medium text-gray-700",
                                        ),
                                    ),
                                    rx.text(
                                        "Make sure you have models loaded in LM Studio",
                                        class_name=rx.cond(
                                            State.is_dark_theme,
                                            "font-[dm] text-xs text-gray-400",
                                            "font-[dm] text-xs text-gray-500",
                                        ),
                                    ),
                                    direction="column",
                                    align="center",
                                    class_name="gap-2",
                                ),
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "bg-gray-800 rounded-2xl border-2 border-gray-600 p-6 text-center shadow-[0px_4px_0px_0px_rgba(75,85,99,0.8)]",
                                    "bg-white rounded-2xl border-2 border-gray-300 p-6 text-center shadow-[0px_4px_0px_0px_rgba(0,0,0,0.1)]",
                                ),
                            ),
                        ),
                        # Not connected
                        rx.box(
                            rx.flex(
                                rx.icon("wifi-off", size=24, color="#EF4444"),
                                rx.text(
                                    "LM Studio not available",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "font-[dm] text-sm font-medium text-white",
                                        "font-[dm] text-sm font-medium text-gray-700",
                                    ),
                                ),
                                rx.text(
                                    "Make sure LM Studio is running on localhost:1234",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "font-[dm] text-xs text-gray-400",
                                        "font-[dm] text-xs text-gray-500",
                                    ),
                                ),
                                rx.button(
                                    rx.icon("refresh-cw", size=14),
                                    "Retry",
                                    on_click=OfflineModelsState.refresh_lmstudio_models,
                                    size="1",
                                    variant="outline",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "mt-2 font-[dm] bg-gray-700 active:bg-gray-600 border-gray-500 text-white rounded-xl border-2 shadow-[0px_2px_0px_0px_rgba(75,85,99,0.8)] active:shadow-[0px_1px_0px_0px_rgba(75,85,99,0.8)] active:translate-y-0.5 transition-all duration-200 md:hover:bg-gray-600 md:hover:shadow-[0px_1px_0px_0px_rgba(75,85,99,0.8)] md:hover:translate-y-0.5",
                                        "mt-2 font-[dm] bg-white active:bg-gray-50 border-gray-300 text-gray-700 rounded-xl border-2 shadow-[0px_2px_0px_0px_rgba(0,0,0,0.2)] active:shadow-[0px_1px_0px_0px_rgba(0,0,0,0.2)] active:translate-y-0.5 transition-all duration-200 md:hover:bg-gray-50 md:hover:shadow-[0px_1px_0px_0px_rgba(0,0,0,0.2)] md:hover:translate-y-0.5",
                                    ),
                                ),
                                direction="column",
                                align="center",
                                class_name="gap-2",
                            ),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "bg-gray-800 rounded-2xl border-2 border-gray-600 p-6 text-center shadow-[0px_4px_0px_0px_rgba(75,85,99,0.8)]",
                                "bg-white rounded-2xl border-2 border-gray-300 p-6 text-center shadow-[0px_4px_0px_0px_rgba(0,0,0,0.1)]",
                            ),
                        ),
                    ),
                ),
                class_name="h-80 overflow-y-auto",
            ),
            # Footer info
            rx.box(
                rx.text(
                    "Select a model to start chatting offline",
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "font-[dm] text-sm text-gray-400 text-center",
                        "font-[dm] text-sm text-gray-500 text-center",
                    ),
                ),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "mt-6 pt-4 border-t border-gray-600",
                    "mt-6 pt-4 border-t border-gray-100",
                ),
            ),
            padding="0 24px 32px 24px",
            background_color=rx.cond(State.is_dark_theme, "#1f2937", "white"),
            border_radius="20px 20px 0 0",
            box_shadow=rx.cond(
                State.is_dark_theme,
                "0 -4px 20px rgba(0, 0, 0, 0.3)",
                "0 -4px 20px rgba(0, 0, 0, 0.1)",
            ),
            border=rx.cond(
                State.is_dark_theme, "3px solid #374151", "3px solid #e5e7eb"
            ),
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
