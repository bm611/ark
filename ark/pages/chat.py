import reflex as rx
from typing import Dict, Any
from ark.state import State
from ark.components.custom.weather import weather_card
from ark.components.ui.buttons import expandable_section_button
from ark.components.ui.layout import navigation_header, loading_skeleton


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
                "font-mono text-sm bg-gray-700 text-gray-200 px-1.5 py-0.5 rounded-md border border-gray-600",
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
                class_name="flex justify-between items-center px-4 py-3 bg-gray-700 rounded-t-lg border-b border-gray-600",
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
            class_name="bg-gray-800 rounded-lg shadow-lg border border-gray-600 overflow-hidden",
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
            rx.text(
                message.get("display_text", message["content"]),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "ml-2 text-xl md:text-4xl font-bold tracking-wide text-white",
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
                    # Tool use section
                    rx.cond(
                        message.get("tool_name"),
                        rx.box(
                            rx.button(
                                rx.hstack(
                                    rx.icon(
                                        "wrench",
                                        size=16,
                                        class_name="text-white",
                                    ),
                                    rx.text(
                                        "Tools",
                                        class_name="font-[dm] text-xs md:text-sm font-semibold text-white",
                                    ),
                                    rx.cond(
                                        State.tool_expanded.get(index, False),
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
                                on_click=State.toggle_tool(index),
                                class_name="text-left p-2 rounded-xl shadow-[0px_4px_0px_0px_rgba(34,197,94,0.8)] hover:shadow-[0px_2px_0px_0px_rgba(34,197,94,0.8)] hover:translate-y-1 transition-all duration-200",
                                style={
                                    "background": "linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%)",
                                    "border": "2px solid #166534",
                                },
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
                                        "font-[dm] text-sm md:text-lg text-white mb-1",
                                        "font-[dm] text-sm md:text-lg text-black mb-1",
                                    ),
                                ),
                                class_name="mb-1",
                            ),
                        ),
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "bg-gray-800 border-2 border-gray-600 rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(75,85,99,0.8)] mb-4",
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
                    State.tool_expanded.get(index, False),
                    rx.box(
                        rx.text(
                            f"Tool Name: {message.get('tool_name', '')}",
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "font-[dm] text-sm md:text-lg font-semibold text-white",
                                "font-[dm] text-sm md:text-lg font-semibold text-black",
                            ),
                        ),
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "bg-gray-800 border-2 border-gray-600 rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(75,85,99,0.8)] mb-4",
                            "bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4",
                        ),
                        # width="100%",
                        # max_width="100%",
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
                                "font-[dm] text-sm md:text-lg text-white",
                                "font-[dm] text-sm md:text-lg text-black",
                            ),
                        ),
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "bg-gray-800 border-2 border-gray-600 rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(75,85,99,0.8)] mb-4",
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
                                "font-[dm] text-sm md:text-lg text-white",
                                "font-[dm] text-sm md:text-lg text-gray-900",
                            ),
                        ),
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "bg-gray-800 border-2 border-gray-600 rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(75,85,99,0.8)] mb-4",
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
                # Weather component - display when weather data is available
                rx.cond(
                    message.get("weather_data"),
                    rx.box(
                        weather_card(),
                        class_name="mb-4 w-full md:max-w-xl",
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
                                    "font-[dm] text-xs font-bold text-white",
                                    "font-[dm] text-xs font-bold text-black",
                                ),
                            ),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "bg-purple-600 rounded-xl p-2 items-center border-2 md:border-3 border-gray-600 shadow-[3px_3px_0px_0px_rgba(75,85,99,0.8)] md:shadow-[5px_5px_0px_0px_rgba(75,85,99,0.8)]",
                                "bg-purple-300 rounded-xl p-2 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]",
                            ),
                        ),
                        rx.flex(
                            rx.text(
                                f"{message.get('total_tokens', 'N/A'):.2f} TOKENS",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "font-[dm] text-xs font-bold text-white",
                                    "font-[dm] text-xs font-bold text-black",
                                ),
                            ),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "bg-sky-600 rounded-xl p-2 items-center border-2 md:border-3 border-gray-600 shadow-[3px_3px_0px_0px_rgba(75,85,99,0.8)] md:shadow-[5px_5px_0px_0px_rgba(75,85,99,0.8)]",
                                "bg-sky-300 rounded-xl p-2 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]",
                            ),
                        ),
                        rx.flex(
                            rx.text(
                                f"{message.get('generation_time', 'N/A'):.2f} SEC",
                                class_name=rx.cond(
                                    State.is_dark_theme,
                                    "font-[dm] text-xs font-bold text-white",
                                    "font-[dm] text-xs font-bold text-black",
                                ),
                            ),
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "bg-amber-600 rounded-xl p-2 items-center border-2 md:border-3 border-gray-600 shadow-[3px_3px_0px_0px_rgba(75,85,99,0.8)] md:shadow-[5px_5px_0px_0px_rgba(75,85,99,0.8)]",
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


def chat_messages():
    return rx.box(
        rx.foreach(
            State.messages,
            lambda message, index: response_message(message, index),
        ),
        rx.cond(
            State.is_gen,
            loading_skeleton(),
        ),
        class_name="flex-1 overflow-y-scroll p-4 md:p-6 space-y-4 max-w-4xl mx-auto w-full pb-24 md:pb-32 hide-scrollbar",
    )
