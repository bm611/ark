import reflex as rx
from typing import Dict, Any
from ark.state import State
from ark.components.common.buttons import expandable_section_button
from ark.components.common.layout import navigation_header


def markdown_component_map() -> Dict[str, Any]:
    """Create a component map for markdown to properly handle tables and other elements.

    Returns:
        A dictionary mapping markdown elements to their Reflex components
    """
    return {
        "h1": lambda text: rx.heading(
            text,
            size="5",
            margin_y="1em",
            class_name="font-[dm] text-3xl font-bold leading-tight my-4",
        ),
        "h2": lambda text: rx.heading(
            text,
            size="3",
            margin_y="1em",
            class_name="font-[dm] text-2xl font-bold leading-tight my-4",
        ),
        "h3": lambda text: rx.heading(
            text,
            size="1",
            margin_y="1em",
            class_name="font-[dm] text-xl font-bold leading-tight my-4",
        ),
        "h4": lambda text: rx.heading(
            text,
            size="1",
            margin_y="1em",
            class_name="font-[dm] text-xl font-bold leading-tight my-4",
        ),
        "p": lambda text: rx.text(text, margin_y="1em", class_name="font-[dm]"),
        "code": lambda text: rx.code(
            text,
            class_name=rx.cond(
                State.is_dark_theme,
                "font-mono text-sm bg-slate-700 text-slate-300 px-1.5 py-0.5 rounded-md border border-slate-600",
                "font-mono text-sm bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded-md border border-gray-200",
            ),
            style={
                "font-family": "ui-monospace, SFMono-Regular, 'SF Mono', Monaco, Inconsolata, 'Roboto Mono', monospace",
                "font-size": "0.875rem",
                "line-height": "1.25rem",
                "word-break": "break-all",
                "white-space": "pre-wrap",
            },
        ),
        "codeblock": lambda text, **props: rx.box(
            # Header section with language and copy button
            rx.box(
                rx.text(
                    props.get("language", "text"),
                    size="1",
                    class_name="text-gray-300 font-mono text-xs font-semibold",
                ),
                rx.button(
                    rx.icon("copy", size=14),
                    rx.text("Copy", class_name="ml-1 text-xs font-mono"),
                    on_click=[rx.set_clipboard(text), rx.toast("Copied!")],
                    variant="ghost",
                    size="1",
                    class_name="text-gray-300 hover:text-white hover:bg-gray-600 px-2 py-1 rounded transition-colors duration-200",
                ),
                class_name="flex justify-between items-center px-4 py-3 bg-slate-700 rounded-t-lg border-b border-slate-600",
            ),
            # Code block section
            rx.code_block(
                text,
                theme=rx.code_block.themes.vsc_dark_plus,
                width="100%",
                max_width="100%",
                overflow_x="auto",
                custom_style={
                    "font-size": "12px",
                    "font_family": "Inter",
                    "white-space": "pre",
                    "word-wrap": "break-word",
                    "overflow-wrap": "break-word",
                    "border-radius": "0",
                    "margin": "0",
                },
                css={
                    "@media (max-width: 768px)": {
                        "font-size": "10px",
                        "padding": "12px",
                    },
                },
            ),
            margin_y="1em",
            class_name="bg-slate-800 rounded-lg shadow-lg border border-slate-600 overflow-hidden",
        ),
        "a": lambda text, **props: rx.link(
            text, **props, color="orange", _hover={"color": "red"}
        ),
        "table": lambda children: rx.box(
            children,
            overflow_x="auto",
            margin_y="1em",
            width="100%",
            max_width="100vw",
            scrollbar_width="thin",
            css={
                "WebkitOverflowScrolling": "touch",
                "@media (max-width: 768px)": {
                    "display": "block",
                    "overflow-x": "scroll",
                },
            },
            style={
                "table": {
                    "width": "100%",
                    "border-collapse": "collapse",
                    "min-width": "400px",
                },
                "th": {
                    "border": "1px solid #e2e8f0",
                    "padding": "8px",
                    "background-color": "#f8fafc",
                    "text-align": "left",
                    "white-space": "nowrap",
                },
                "td": {"border": "1px solid #e2e8f0", "padding": "8px"},
            },
        ),
    }


def chat_nav():
    return navigation_header(
        provider_name=State.selected_provider,
        model_name=State.selected_model,
        new_chat_handler=[
            rx.redirect("/"),
            State.reset_chat,
        ],
    )


def response_message(message: dict, index: int) -> rx.Component:
    return rx.box(
        rx.cond(
            message["role"] == "user",
            rx.vstack(
                rx.text(
                    message.get("display_text", message["content"]),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "ml-2 text-xl md:text-4xl font-bold tracking-wide text-slate-50",
                        "ml-2 text-xl md:text-4xl font-bold tracking-wide text-gray-900",
                    ),
                    style={
                        "display": "-webkit-box",
                        "-webkit-line-clamp": "2",
                        "-webkit-box-orient": "vertical",
                        "overflow": "hidden",
                        "text-overflow": "ellipsis",
                    },
                ),
                # Image preview section for user messages
                rx.cond(
                    State.current_message_image & (index == 0),
                    rx.box(
                        rx.image(
                            src=State.current_message_image,
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "rounded-xl border-2 border-slate-600 shadow-[8px_8px_0px_0px_rgba(51,65,85,0.8)] mb-2",
                                "rounded-xl border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-2",
                            ),
                            style={
                                "max-width": "300px",
                                "max-height": "300px",
                                "object-fit": "contain",
                            },
                        ),
                        class_name="ml-2 mt-4",
                    ),
                ),
                # Generating response indicator for user messages
                rx.cond(
                    State.is_streaming,
                    rx.box(
                        rx.text(
                            "Generating Response...",
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "text-lg font-semibold text-slate-300 bg-gradient-to-r from-slate-300 via-slate-50 to-slate-300 bg-clip-text text-transparent animate-pulse bg-[length:200%_100%] animate-[shimmer_2s_infinite]",
                                "text-lg font-semibold text-gray-600 bg-gradient-to-r from-gray-600 via-gray-800 to-gray-600 bg-clip-text text-transparent animate-pulse bg-[length:200%_100%] animate-[shimmer_2s_infinite]",
                            ),
                        ),
                        class_name="w-full justify-left px-4 py-4",
                    ),
                ),
                spacing="0",
                align_items="start",
            ),
            rx.vstack(
                # Buttons section in horizontal stack
                rx.hstack(
                    # Citations section
                    rx.cond(
                        message.get("citations", []),
                        rx.box(
                            expandable_section_button(
                                label="Sources",
                                icon="list",
                                is_expanded=State.citations_expanded.get(index, False),
                                gradient="linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%)",
                                border_color="#1e40af",
                                shadow_color="rgba(59,130,246,0.8)",
                                on_click=State.toggle_citations(index),
                            ),
                        ),
                    ),
                    # Thinking tokens collapsible section
                    rx.cond(
                        message.get("thinking"),
                        rx.box(
                            rx.button(
                                rx.hstack(
                                    rx.icon(
                                        "lightbulb",
                                        size=16,
                                        class_name="text-white",
                                    ),
                                    rx.text(
                                        "Thinking",
                                        class_name="font-[dm] text-xs md:text-sm font-semibold text-white",
                                    ),
                                    rx.cond(
                                        State.thinking_expanded.get(index, False),
                                        rx.icon(
                                            "chevron-down",
                                            size=16,
                                            class_name="text-white",
                                        ),
                                        rx.icon(
                                            "chevron-right",
                                            size=16,
                                            class_name="text-white",
                                        ),
                                    ),
                                    class_name="items-center gap-1",
                                ),
                                on_click=State.toggle_thinking(index),
                                class_name="text-left p-2 rounded-xl shadow-[0px_4px_0px_0px_rgba(147,51,234,0.8)] hover:shadow-[0px_2px_0px_0px_rgba(147,51,234,0.8)] hover:translate-y-1 transition-all duration-200",
                                style={
                                    "background": "linear-gradient(135deg, #a855f7 0%, #8b5cf6 50%, #7c3aed 100%)",
                                    "border": "2px solid #6d28d9",
                                },
                            ),
                        ),
                    ),
                    class_name="gap-2 mb-4 flex-wrap ml-2",
                ),
                # Expanded content sections
                rx.cond(
                    State.citations_expanded.get(index, False),
                    rx.box(
                        rx.foreach(
                            message.get("citations", []),
                            lambda citation, citation_index: rx.box(
                                rx.link(
                                    f"[{citation_index + 1}] {citation}",
                                    href=citation,
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "font-[dm] text-sm md:text-lg text-slate-50 mb-1",
                                        "font-[dm] text-sm md:text-lg text-black mb-1",
                                    ),
                                ),
                                class_name="mb-1",
                            ),
                        ),
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "bg-slate-800 border-2 border-slate-600 rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(51,65,85,0.8)] mb-4",
                            "bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4",
                        ),
                        width="100%",
                        max_width="100%",
                        overflow_x="auto",
                        style={
                            "word-wrap": "break-word",
                            "overflow-wrap": "break-word",
                        },
                    ),
                ),
                rx.cond(
                    State.thinking_expanded.get(index, False),
                    rx.box(
                        rx.markdown(
                            message["thinking"],
                            component_map=markdown_component_map(),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "font-[dm] text-sm md:text-lg text-slate-50",
                                "font-[dm] text-sm md:text-lg text-black",
                            ),
                        ),
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "bg-slate-800 border-2 border-slate-600 rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(51,65,85,0.8)] mb-4",
                            "bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4",
                        ),
                        width="100%",
                        max_width="100%",
                        overflow_x="auto",
                        style={
                            "word-wrap": "break-word",
                            "overflow-wrap": "break-word",
                        },
                    ),
                ),
                rx.cond(
                    message.get("content"),
                    rx.box(
                        # Assistant message content
                        rx.markdown(
                            message["content"],
                            component_map=markdown_component_map(),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "font-[dm] text-sm md:text-lg text-slate-50",
                                "font-[dm] text-sm md:text-lg text-gray-900",
                            ),
                        ),
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "bg-slate-800 border-2 border-slate-600 rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(51,65,85,0.8)] mb-4",
                            "bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4",
                        ),
                        width="100%",
                        max_width="100%",
                        overflow_x="auto",
                        style={
                            "word-wrap": "break-word",
                            "overflow-wrap": "break-word",
                        },
                    ),
                ),
                # Performance stats with hero component design style
                rx.cond(
                    message.get("generation_time"),
                    rx.flex(
                        rx.flex(
                            rx.text(
                                f"{message.get('tokens_per_second', 'N/A'):.2f} TOKENS/SEC",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "font-[dm] text-xs font-bold text-slate-50",
                                    "font-[dm] text-xs font-bold text-black",
                                ),
                            ),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "bg-purple-600 rounded-xl p-2 items-center border-2 md:border-3 border-slate-600 shadow-[3px_3px_0px_0px_rgba(51,65,85,0.8)] md:shadow-[5px_5px_0px_0px_rgba(51,65,85,0.8)]",
                                "bg-purple-300 rounded-xl p-2 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]",
                            ),
                        ),
                        rx.flex(
                            rx.text(
                                f"{message.get('total_tokens', 'N/A'):.2f} TOKENS",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "font-[dm] text-xs font-bold text-slate-50",
                                    "font-[dm] text-xs font-bold text-black",
                                ),
                            ),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "bg-sky-600 rounded-xl p-2 items-center border-2 md:border-3 border-slate-600 shadow-[3px_3px_0px_0px_rgba(51,65,85,0.8)] md:shadow-[5px_5px_0px_0px_rgba(51,65,85,0.8)]",
                                "bg-sky-300 rounded-xl p-2 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]",
                            ),
                        ),
                        rx.flex(
                            rx.text(
                                f"{message.get('generation_time', 'N/A'):.2f} SEC",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "font-[dm] text-xs font-bold text-slate-50",
                                    "font-[dm] text-xs font-bold text-black",
                                ),
                            ),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "bg-amber-600 rounded-xl p-2 items-center border-2 md:border-3 border-slate-600 shadow-[3px_3px_0px_0px_rgba(51,65,85,0.8)] md:shadow-[5px_5px_0px_0px_rgba(51,65,85,0.8)]",
                                "bg-amber-300 rounded-xl p-2 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]",
                            ),
                        ),
                        class_name="gap-2 md:gap-4 mb-20 ml-2",
                    ),
                ),
                spacing="0",
            ),
        ),
    )


def chat_input():
    return rx.box(
        rx.box(
            rx.box(
                rx.input(
                    value=State.prompt,
                    placeholder="Ask Follow Up...",
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "w-full text-white text-base md:text-lg rounded-xl h-12 shadow-[0px_2px_0px_0px_rgba(0,0,0,0.1)] hover:shadow-[0px_3px_0px_0px_rgba(0,0,0,0.15)] focus:shadow-[0px_3px_0px_0px_rgba(0,0,0,0.2)] border border-gray-600 hover:border-gray-500 focus:border-gray-400 transition-all duration-200 pl-3 md:pl-4 pr-12 md:pr-14 outline-none focus:outline-none",
                        "w-full text-gray-900 text-base md:text-lg rounded-xl h-12 shadow-[0px_2px_0px_0px_rgba(0,0,0,0.1)] hover:shadow-[0px_3px_0px_0px_rgba(0,0,0,0.15)] focus:shadow-[0px_3px_0px_0px_rgba(0,0,0,0.2)] border border-gray-300 hover:border-gray-400 focus:border-gray-600 transition-all duration-200 pl-3 md:pl-4 pr-12 md:pr-14 outline-none focus:outline-none",
                    ),
                    style={
                        "background": rx.cond(State.is_dark_theme, "#1f2937", "white"),
                        "color": rx.cond(State.is_dark_theme, "white", "#111827"),
                        "outline": "none",
                        "& input::placeholder": {
                            "color": rx.cond(State.is_dark_theme, "#a3a3a3", "#6b7280"),
                        },
                    },
                    on_change=State.set_prompt,
                ),
                rx.button(
                    rx.icon(
                        "arrow-right",
                        size=24,
                        color=rx.cond(State.is_dark_theme, "white", "gray"),
                    ),
                    class_name="absolute right-1.5 top-1/2 transform -translate-y-1/2 bg-transparent rounded-none h-8 w-8 p-0 m-0 flex items-center justify-center",
                    style={"boxShadow": "none", "background": "none"},
                    on_click=[
                        State.handle_generation,
                        State.send_message_stream,
                    ],
                    loading=State.is_streaming,
                    disabled=State.is_streaming,
                ),
                class_name="relative w-full max-w-2xl mx-auto",
            ),
            class_name="p-4",
        ),
        class_name=rx.cond(
            State.is_dark_theme,
            "fixed bottom-0 left-0 right-0 backdrop-blur-lg",
            "fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-lg",
        ),
    )


def chat_messages():
    return rx.box(
        rx.foreach(
            State.messages,
            lambda message, index: response_message(message, index),
        ),
        class_name="flex-1 overflow-y-scroll p-4 md:p-6 space-y-4 max-w-4xl mx-auto w-full pb-24 md:pb-32 hide-scrollbar",
    )
