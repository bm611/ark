import reflex as rx
from ark.state import State
from ark.components.common.buttons import action_button
from ark.components.modals.offline_models import (
    OfflineModelsState,
    offline_models_overlay,
    offline_models_content,
)
import reflex_clerk_api as clerk


def input_section():
    return (
        rx.box(
            rx.vstack(
                rx.cond(
                    (State.img.length() > 0) | (State.pdf_files.length() > 0),
                    rx.box(
                        rx.hstack(
                            # Image files
                            rx.foreach(
                                State.img,
                                lambda filename: rx.box(
                                    rx.hstack(
                                        rx.icon(
                                            "image",
                                            size=18,
                                            color=rx.cond(
                                                State.is_dark_theme,
                                                "#60a5fa",
                                                "#3b82f6",
                                            ),
                                        ),
                                        rx.text(
                                            filename,
                                            class_name=rx.cond(
                                                State.is_dark_theme,
                                                "text-sm text-neutral-200 font-[dm] font-medium",
                                                "text-sm text-gray-700 font-[dm] font-medium",
                                            ),
                                        ),
                                        rx.button(
                                            rx.icon("x", size=14),
                                            variant="ghost",
                                            class_name=rx.cond(
                                                State.is_dark_theme,
                                                "ml-2 p-1 rounded-full hover:bg-neutral-600/30 text-neutral-400 hover:text-neutral-200 border-0 bg-transparent",
                                                "ml-2 p-1 rounded-full hover:bg-gray-200/50 text-gray-500 hover:text-gray-700 border-0 bg-transparent",
                                            ),
                                            on_click=State.clear_images,
                                        ),
                                        align="center",
                                        spacing="2",
                                    ),
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "bg-neutral-800/90 border border-neutral-600/60 rounded-xl px-4 py-3 backdrop-blur-sm shadow-lg",
                                        "bg-white/90 border border-gray-300/60 rounded-xl px-4 py-3 backdrop-blur-sm shadow-lg",
                                    ),
                                ),
                            ),
                            # PDF files
                            rx.foreach(
                                State.pdf_files,
                                lambda filename: rx.box(
                                    rx.hstack(
                                        rx.icon(
                                            "file-text",
                                            size=18,
                                            color=rx.cond(
                                                State.is_dark_theme,
                                                "#ef4444",
                                                "#dc2626",
                                            ),
                                        ),
                                        rx.text(
                                            filename,
                                            class_name=rx.cond(
                                                State.is_dark_theme,
                                                "text-sm text-neutral-200 font-[dm] font-medium",
                                                "text-sm text-gray-700 font-[dm] font-medium",
                                            ),
                                        ),
                                        rx.button(
                                            rx.icon("x", size=14),
                                            variant="ghost",
                                            class_name=rx.cond(
                                                State.is_dark_theme,
                                                "ml-2 p-1 rounded-full hover:bg-neutral-600/30 text-neutral-400 hover:text-neutral-200 border-0 bg-transparent",
                                                "ml-2 p-1 rounded-full hover:bg-gray-200/50 text-gray-500 hover:text-gray-700 border-0 bg-transparent",
                                            ),
                                            on_click=State.clear_pdfs,
                                        ),
                                        align="center",
                                        spacing="2",
                                    ),
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "bg-neutral-800/90 border border-neutral-600/60 rounded-xl px-4 py-3 backdrop-blur-sm shadow-lg",
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
                rx.box(
                    rx.text_area(
                        value=State.prompt,
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "w-full mx-auto text-white text-base sm:text-lg md:text-2xl rounded-3xl min-h-28 sm:min-h-32 max-h-40 sm:max-h-48 border transition-all duration-200 px-3 sm:px-4 md:px-6 py-3 sm:py-4 pb-12 sm:pb-16 resize-none outline-none focus:outline-none border-[3px] border-transparent bg-[linear-gradient(#0a0a0a,#0a0a0a),linear-gradient(90deg,#f97316,#c026d3)] bg-origin-border bg-clip-padding bg-clip-border shadow-[0_0_30px_rgba(249,115,22,0.7),0_0_60px_rgba(192,38,211,0.4),0_8px_40px_rgba(0,0,0,0.5)]",
                            "w-full mx-auto text-gray-900 text-base sm:text-lg md:text-2xl rounded-3xl min-h-28 sm:min-h-32 max-h-40 sm:max-h-48 border transition-all duration-200 px-3 sm:px-4 md:px-6 py-3 sm:py-4 pb-12 sm:pb-16 resize-none outline-none focus:outline-none border-[3px] border-transparent bg-[linear-gradient(white,white),linear-gradient(90deg,#fb923c,#a21caf)] bg-origin-border bg-clip-padding bg-clip-border shadow-[0_0_40px_rgba(251,146,60,0.7),0_0_80px_rgba(162,28,175,0.4)]",
                        ),
                        placeholder="Ask Anything...",
                        style={
                            "background": rx.cond(
                                State.is_dark_theme, "#0a0a0a", "white"
                            ),
                            "color": rx.cond(State.is_dark_theme, "white", "#111827"),
                            "outline": "none",
                            "& textarea::placeholder": {
                                "color": rx.cond(
                                    State.is_dark_theme, "#a3a3a3", "#6b7280"
                                ),
                            },
                        },
                        on_change=State.set_prompt,
                        size="3",
                    ),
                    rx.box(
                        rx.hstack(
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
                                        style={},
                                        class_name="",
                                        border=None,
                                        padding=None,
                                        accept={
                                            "image/png": [".png"],
                                            "image/jpeg": [".jpg", ".jpeg"],
                                            "application/pdf": [".pdf"],
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
                                    class_name="gap-0 mb-2",
                                ),
                            ),
                            rx.button(
                                rx.hstack(
                                    rx.icon(
                                        "arrow-up",
                                        size=20,
                                        color="white",
                                        class_name="sm:hidden w-5 h-5",
                                    ),
                                    rx.text(
                                        "Send",
                                        class_name="hidden sm:block text-sm font-medium text-white ml-1",
                                    ),
                                    class_name="flex items-center justify-center",
                                ),
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "ml-auto text-white rounded-full h-8 sm:h-10 w-10 sm:w-auto sm:px-4 shadow-[0px_4px_0px_0px_rgba(107,114,128,0.6)] hover:shadow-[0px_4px_0px_0px_rgba(107,114,128,0.7)] active:shadow-[0px_4px_0px_0px_rgba(107,114,128,0.8)] transition-all duration-150 flex items-center justify-center mb-1",
                                    "ml-auto text-white rounded-full h-8 sm:h-10 w-10 sm:w-auto sm:px-4 shadow-[0px_4px_0px_0px_rgba(107,114,128,0.6)] hover:shadow-[0px_4px_0px_0px_rgba(107,114,128,0.7)] active:shadow-[0px_4px_0px_0px_rgba(107,114,128,0.8)] transition-all duration-150 flex items-center justify-center mb-1",
                                ),
                                style={
                                    "background": rx.cond(
                                        State.is_dark_theme,
                                        "linear-gradient(135deg, #6b7280 0%, #4b5563 50%, #374151 100%)",
                                        "linear-gradient(135deg, #9ca3af 0%, #6b7280 50%, #4b5563 100%)",
                                    ),
                                    "border": "2px solid #374151",
                                    "boxShadow": "0px 4px 0px 0px rgba(107,114,128,0.6)",
                                },
                                on_click=[
                                    State.handle_generation,
                                    State.generate_chat_id_and_redirect,
                                ],
                                loading=State.is_gen,
                                disabled=State.is_gen,
                            ),
                            align="center",
                            class_name="w-full",
                        ),
                        class_name="absolute bottom-2 left-2 right-2 px-2",
                    ),
                    class_name="relative w-full max-w-4xl mx-auto",
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
                        clerk.signed_in(
                            rx.heading(
                                rx.cond(
                                    State.logged_user_name == "",
                                    "Welcome back!",
                                    "Welcome back, " + State.logged_user_name + "!",
                                ),
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "text-4xl md:text-7xl font-bold mb-3 md:mb-4 tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-green-400 animate-fade-in-up px-8 md:px-0 leading-tight",
                                    "text-4xl md:text-7xl font-bold mb-3 md:mb-4 tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-green-400 to-purple-500 animate-fade-in-up px-8 md:px-0 leading-tight",
                                ),
                                as_="h1",
                            )
                        ),
                        clerk.signed_out(
                            rx.heading(
                                "Welcome to Ark!",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "text-4xl md:text-7xl font-bold mb-3 md:mb-4 tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-green-400 animate-fade-in-up px-8 md:px-0 leading-tight",
                                    "text-4xl md:text-7xl font-bold mb-3 md:mb-4 tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-green-400 to-purple-500 animate-fade-in-up px-8 md:px-0 leading-tight",
                                ),
                                as_="h1",
                            )
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
                                "hidden sm:block text-base sm:text-lg md:text-2xl mb-6 sm:mb-8 md:mb-12 text-neutral-300 font-medium animate-fade-in-up px-6 md:px-0 leading-relaxed",
                                "hidden sm:block text-base sm:text-lg md:text-2xl mb-6 sm:mb-8 md:mb-12 text-gray-700 font-medium animate-fade-in-up px-6 md:px-0 leading-relaxed",
                            ),
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Try these examples:",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-sm sm:text-base font-semibold text-neutral-300 mb-3 sm:mb-4 px-4 md:px-0 mt-4",
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
                                            "example-prompt-card bg-gradient-to-br from-neutral-800/90 to-neutral-900/70 hover:from-neutral-700/95 hover:to-neutral-800/80 border border-neutral-600/50 hover:border-neutral-500/70 text-neutral-200 hover:text-white transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-lg hover:shadow-xl transform hover:scale-105",
                                            "example-prompt-card bg-gradient-to-br from-white/90 to-gray-50/80 hover:from-white hover:to-blue-50/50 border border-gray-200/60 hover:border-blue-200/80 text-gray-700 hover:text-gray-900 transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-md hover:shadow-xl transform hover:scale-105",
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "Give me some Python programming tips with code examples."
                                            ),
                                            State.handle_generation,
                                            State.generate_chat_id_and_redirect,
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
                                            "example-prompt-card bg-gradient-to-br from-neutral-800/90 to-neutral-900/70 hover:from-neutral-700/95 hover:to-neutral-800/80 border border-neutral-600/50 hover:border-neutral-500/70 text-neutral-200 hover:text-white transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-lg hover:shadow-xl transform hover:scale-105",
                                            "example-prompt-card bg-gradient-to-br from-white/90 to-gray-50/80 hover:from-white hover:to-green-50/50 border border-gray-200/60 hover:border-green-200/80 text-gray-700 hover:text-gray-900 transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-md hover:shadow-xl transform hover:scale-105",
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "What's the latest news in US, World, Technology & Science?"
                                            ),
                                            State.handle_search_click,
                                            State.handle_generation,
                                            State.generate_chat_id_and_redirect,
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
                                            "example-prompt-card bg-gradient-to-br from-neutral-800/90 to-neutral-900/70 hover:from-neutral-700/95 hover:to-neutral-800/80 border border-neutral-600/50 hover:border-neutral-500/70 text-neutral-200 hover:text-white transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-lg hover:shadow-xl transform hover:scale-105",
                                            "example-prompt-card bg-gradient-to-br from-white/90 to-gray-50/80 hover:from-white hover:to-purple-50/50 border border-gray-200/60 hover:border-purple-200/80 text-gray-700 hover:text-gray-900 transition-all duration-300 px-4 sm:px-6 py-3 sm:py-4 rounded-2xl text-xs sm:text-sm shadow-md hover:shadow-xl transform hover:scale-105",
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "Explain quantum computing"
                                            ),
                                            State.handle_generation,
                                            State.generate_chat_id_and_redirect,
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
