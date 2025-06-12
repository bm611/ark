import reflex as rx
from ark.state import State
from ark.components.ui.buttons import action_button, gradient_card
from ark.components.offline_models import (
    OfflineModelsState,
    offline_models_overlay,
    offline_models_content,
)


def input_section():
    return (
        rx.box(
            rx.vstack(
                rx.cond(
                    State.img,
                    rx.box(
                        rx.hstack(
                            rx.foreach(
                                State.img,
                                lambda filename: rx.box(
                                    rx.hstack(
                                        rx.icon(
                                            "file",
                                            size=18,
                                            color=rx.cond(
                                                State.is_dark_theme,
                                                "#a3a3a3",
                                                "#525252",
                                            ),
                                        ),
                                        rx.text(
                                            filename,
                                            class_name=rx.cond(
                                                State.is_dark_theme,
                                                "text-sm text-gray-200 font-[dm] font-medium",
                                                "text-sm text-gray-700 font-[dm] font-medium",
                                            ),
                                        ),
                                        rx.button(
                                            rx.icon("x", size=14),
                                            variant="ghost",
                                            class_name=rx.cond(
                                                State.is_dark_theme,
                                                "ml-2 p-1 rounded-full hover:bg-gray-600/30 text-gray-400 hover:text-gray-200 border-0 bg-transparent",
                                                "ml-2 p-1 rounded-full hover:bg-gray-200/50 text-gray-500 hover:text-gray-700 border-0 bg-transparent",
                                            ),
                                            on_click=State.clear_images,
                                        ),
                                        align="center",
                                        spacing="2",
                                    ),
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "bg-gray-800/80 border border-gray-600/50 rounded-xl px-4 py-3 backdrop-blur-sm shadow-lg",
                                        "bg-white/90 border border-gray-300/60 rounded-xl px-4 py-3 backdrop-blur-sm shadow-lg",
                                    ),
                                ),
                            ),
                            wrap="wrap",
                            spacing="3",
                        ),
                        class_name="mb-1 w-full max-w-4xl mx-auto",
                    ),
                ),
                rx.hstack(
                    rx.input(
                        value=State.prompt,
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "w-full mx-auto text-white text-lg md:text-2xl rounded-2xl h-16 shadow-[0px_4px_0px_0px_rgba(0,0,0,0.1)] hover:shadow-[0px_6px_0px_0px_rgba(0,0,0,0.15)] focus:shadow-[0px_6px_0px_0px_rgba(0,0,0,0.2)] border-2 border-gray-600 hover:border-gray-500 focus:border-gray-400 transition-all duration-200 px-4 md:px-6",
                            "w-full mx-auto text-gray-900 text-lg md:text-2xl rounded-2xl h-16 shadow-[0px_4px_0px_0px_rgba(0,0,0,0.1)] hover:shadow-[0px_6px_0px_0px_rgba(0,0,0,0.15)] focus:shadow-[0px_6px_0px_0px_rgba(0,0,0,0.2)] border-2 border-gray-300 hover:border-gray-400 focus:border-gray-600 transition-all duration-200 px-4 md:px-6",
                        ),
                        placeholder="Ask Anything...",
                        style={
                            "background": rx.cond(
                                State.is_dark_theme, "#1f2937", "white"
                            ),
                            "color": rx.cond(State.is_dark_theme, "white", "#111827"),
                            "& input::placeholder": {
                                "color": rx.cond(
                                    State.is_dark_theme, "#9ca3af", "#6b7280"
                                ),
                            },
                        },
                        on_change=State.set_prompt,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("arrow-up", size=28, color="white"),
                            class_name="flex items-center justify-center",
                        ),
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "mx-auto text-white rounded-2xl h-16 px-4 md:px-8 shadow-[0px_4px_0px_0px_rgba(0,0,0,0.3)] active:shadow-[0px_2px_0px_0px_rgba(0,0,0,0.3)] active:translate-y-1 transition-all duration-200 md:hover:shadow-[0px_6px_0px_0px_rgba(0,0,0,0.4)] md:hover:brightness-110",
                            "mx-auto text-white rounded-2xl h-16 px-4 md:px-8 shadow-[0px_4px_0px_0px_rgba(0,0,0,0.3)] active:shadow-[0px_2px_0px_0px_rgba(0,0,0,0.3)] active:translate-y-1 transition-all duration-200 md:hover:shadow-[0px_6px_0px_0px_rgba(0,0,0,0.4)] md:hover:brightness-110",
                        ),
                        style=rx.cond(
                            State.is_dark_theme,
                            {
                                "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #1e40af 100%)",
                                "border": "1px solid #1e40af",
                            },
                            {
                                "background": "linear-gradient(to right, #374151, #111827)",
                                "border": "1px solid #4b5563",
                            },
                        ),
                        on_click=[
                            rx.redirect("/chat"),
                            State.handle_generation,
                            State.send_message,
                        ],
                        loading=State.is_gen,
                        disabled=State.is_gen,
                    ),
                    class_name="w-full flex gap-2 items-center justify-center max-w-4xl mx-auto",
                ),
                rx.cond(
                    State.current_url == "/",
                    rx.hstack(
                        rx.upload(
                            action_button(
                                label="",
                                icon="paperclip",
                                active_gradient="linear-gradient(135deg, #60a5fa 0%, #2563eb 50%, #1e40af 100%)",
                                active_border="#1e40af",
                                shadow_color="rgba(59,130,246,0.8)",
                            ),
                            # Remove default styling by setting style and class_name to empty
                            style={},
                            class_name="",
                            border=None,
                            padding=None,
                            accept={
                                "image/png": [".png"],
                                "image/jpeg": [".jpg", ".jpeg"],
                            },
                            on_drop=State.handle_upload(
                                rx.upload_files(upload_id="upload")
                            ),
                            id="upload",
                        ),
                        action_button(
                            label="Search",
                            icon="globe",
                            is_active=State.selected_action == "Search",
                            active_gradient="linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%)",
                            active_border="#166534",
                            shadow_color="rgba(34,197,94,0.8)",
                            on_click=State.handle_search_click,
                        ),
                        action_button(
                            label="Offline",
                            icon="cloud-off",
                            is_active=rx.cond(
                                State.selected_action == "Offline",
                                OfflineModelsState.selected_model != "",
                                False,
                            ),
                            active_gradient="linear-gradient(135deg, #9333ea 0%, #7c3aed 50%, #6d28d9 100%)",
                            active_border="#5b21b6",
                            shadow_color="rgba(147,51,234,0.8)",
                            on_click=[
                                State.select_action("Offline"),
                                OfflineModelsState.open_drawer,
                            ],
                        ),
                        class_name="gap-0",
                    ),
                ),
                class_name="w-full mx-auto max-w-4xl",
            ),
            class_name="fixed bottom-2 md:bottom-6 left-0 right-0 p-4",
        ),
    )


def hero():
    return (
        rx.box(
            rx.flex(
                rx.box(
                    rx.box(
                        rx.heading(
                            "Welcome to Ark!",
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "text-4xl md:text-7xl font-bold mb-3 md:mb-4 tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 animate-fade-in-up px-8 md:px-0 leading-tight",
                                "text-4xl md:text-7xl font-bold mb-3 md:mb-4 tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-green-400 to-purple-500 animate-fade-in-up px-8 md:px-0 leading-tight",
                            ),
                            as_="h1",
                        ),
                        rx.heading(
                            "Your AI Chat Companion",
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "text-xl md:text-3xl font-bold mb-3 md:mb-4 tracking-wide text-white animate-fade-in-up px-8 md:px-0 leading-tight",
                                "text-xl md:text-3xl font-bold mb-3 md:mb-4 tracking-wide text-gray-900 animate-fade-in-up px-8 md:px-0 leading-tight",
                            ),
                            as_="h1",
                        ),
                        rx.text(
                            "Chat, search, and learn—smarter, faster, anywhere.",
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "hidden sm:block text-base sm:text-lg md:text-2xl mb-6 sm:mb-8 md:mb-12 text-gray-300 font-medium animate-fade-in-up px-6 md:px-0 leading-relaxed",
                                "hidden sm:block text-base sm:text-lg md:text-2xl mb-6 sm:mb-8 md:mb-12 text-gray-700 font-medium animate-fade-in-up px-6 md:px-0 leading-relaxed",
                            ),
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Try these examples:",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-sm sm:text-base font-semibold text-gray-300 mb-3 sm:mb-4 px-4 md:px-0 mt-4",
                                        "text-sm sm:text-base font-semibold text-gray-600 mb-3 sm:mb-4 px-4 md:px-0 mt-4",
                                    ),
                                ),
                                rx.flex(
                                    rx.button(
                                        rx.vstack(
                                            rx.box(
                                                rx.icon(
                                                    "message-circle",
                                                    size=20,
                                                    color=rx.cond(
                                                        State.is_dark_theme,
                                                        "#60a5fa",
                                                        "#3b82f6",
                                                    ),
                                                ),
                                                class_name="mb-2",
                                            ),
                                            rx.text(
                                                "Python programming tips",
                                                class_name="font-medium text-center leading-tight",
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        class_name=rx.cond(
                                            State.is_dark_theme,
                                            "example-prompt-card bg-gradient-to-br from-gray-800/80 to-gray-900/60 hover:from-gray-700/90 hover:to-gray-800/70 border border-gray-600/40 hover:border-gray-500/60 text-gray-200 hover:text-white transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-lg hover:shadow-xl transform hover:scale-105",
                                            "example-prompt-card bg-gradient-to-br from-white/90 to-gray-50/80 hover:from-white hover:to-blue-50/50 border border-gray-200/60 hover:border-blue-200/80 text-gray-700 hover:text-gray-900 transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-md hover:shadow-xl transform hover:scale-105",
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "Give me some Python programming tips with code examples."
                                            ),
                                            rx.redirect("/chat"),
                                            State.handle_generation,
                                            State.send_message,
                                        ],
                                    ),
                                    rx.button(
                                        rx.vstack(
                                            rx.box(
                                                rx.icon(
                                                    "globe",
                                                    size=20,
                                                    color=rx.cond(
                                                        State.is_dark_theme,
                                                        "#22c55e",
                                                        "#16a34a",
                                                    ),
                                                ),
                                                class_name="mb-2",
                                            ),
                                            rx.text(
                                                "What's the latest news?",
                                                class_name="font-medium text-center leading-tight",
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        class_name=rx.cond(
                                            State.is_dark_theme,
                                            "example-prompt-card bg-gradient-to-br from-gray-800/80 to-gray-900/60 hover:from-gray-700/90 hover:to-gray-800/70 border border-gray-600/40 hover:border-gray-500/60 text-gray-200 hover:text-white transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-lg hover:shadow-xl transform hover:scale-105",
                                            "example-prompt-card bg-gradient-to-br from-white/90 to-gray-50/80 hover:from-white hover:to-green-50/50 border border-gray-200/60 hover:border-green-200/80 text-gray-700 hover:text-gray-900 transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-md hover:shadow-xl transform hover:scale-105",
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "What's the latest news in US, World, Technology & Science?"
                                            ),
                                            State.handle_search_click,
                                            rx.redirect("/chat"),
                                            State.handle_generation,
                                            State.send_message,
                                        ],
                                    ),
                                    rx.button(
                                        rx.vstack(
                                            rx.box(
                                                rx.icon(
                                                    "book-open",
                                                    size=20,
                                                    color=rx.cond(
                                                        State.is_dark_theme,
                                                        "#a855f7",
                                                        "#9333ea",
                                                    ),
                                                ),
                                                class_name="mb-2",
                                            ),
                                            rx.text(
                                                "Explain quantum computing",
                                                class_name="font-medium text-center leading-tight",
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        class_name=rx.cond(
                                            State.is_dark_theme,
                                            "example-prompt-card bg-gradient-to-br from-gray-800/80 to-gray-900/60 hover:from-gray-700/90 hover:to-gray-800/70 border border-gray-600/40 hover:border-gray-500/60 text-gray-200 hover:text-white transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-lg hover:shadow-xl transform hover:scale-105",
                                            "example-prompt-card bg-gradient-to-br from-white/90 to-gray-50/80 hover:from-white hover:to-purple-50/50 border border-gray-200/60 hover:border-purple-200/80 text-gray-700 hover:text-gray-900 transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-md hover:shadow-xl transform hover:scale-105",
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "Explain quantum computing"
                                            ),
                                            rx.redirect("/chat"),
                                            State.handle_generation,
                                            State.send_message,
                                        ],
                                    ),
                                    wrap="wrap",
                                    spacing="3",
                                    justify="center",
                                    class_name="gap-3 sm:gap-4 max-w-3xl mx-auto px-3 sm:px-4",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            class_name="mb-6 sm:mb-8",
                        ),
                        class_name="text-center relative",
                    ),
                ),
                direction="column",
                align="center",
                justify="center",
            ),
            offline_models_overlay(),
            offline_models_content(),
            rx.html(
                """
                <style>
                .example-prompt-card {
                    min-height: 120px;
                    min-width: 180px;
                    max-width: 200px;
                    flex: 1;
                    backdrop-filter: blur(10px);
                }

                @media (max-width: 640px) {
                    .example-prompt-card {
                        min-width: 140px;
                        max-width: 150px;
                        min-height: 85px;
                        font-size: 0.75rem;
                    }
                }

                @media (min-width: 641px) and (max-width: 768px) {
                    .example-prompt-card {
                        min-width: 160px;
                        max-width: 170px;
                        min-height: 95px;
                    }
                }

                .example-prompt-card:active {
                    transform: scale(0.98);
                }
                </style>
                """
            ),
            class_name="flex items-center justify-center min-h-[70vh] pb-4 pt-8 md:pt-0 relative overflow-hidden",
        ),
    )
