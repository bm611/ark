import reflex as rx
from typing import Dict, Any
from tbd.state import State


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
        "p": lambda text: rx.text(text, margin_y="1em", class_name="font-[dm]"),
        "code": lambda text: rx.code(text),
        "codeblock": lambda text, **props: rx.code_block(
            text,
            **props,
            theme=rx.code_block.themes.vsc_dark_plus,
            margin_y="1em",
            border_radius="16px",
            width="100%",
            max_width="100%",
            overflow_x="auto",
            custom_style={
                "font-size": "12px",
                "font_family": "Inter",
                "white-space": "pre",
                "word-wrap": "break-word",
                "overflow-wrap": "break-word",
            },
            css={
                "@media (max-width: 768px)": {
                    "font-size": "8px",
                    "padding": "8px",
                },
            },
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
    return rx.hstack(
        # Left side - empty with flex-1 to take equal space
        rx.box(class_name="flex-1"),
        # Middle - Model provider section
        rx.flex(
            rx.flex(
                rx.text(
                    State.selected_provider.upper(),
                    class_name="font-[dm] text-xs md:text-sm font-bold text-black",
                ),
                class_name="hidden md:flex bg-green-300 rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]",
            ),
            rx.flex(
                rx.text(
                    State.selected_model.upper(),
                    class_name="font-[dm] text-xs md:text-sm font-bold text-black",
                ),
                class_name="bg-pink-300 rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]",
            ),
            class_name="gap-2 md:gap-4",
        ),
        # Right side - New Chat button with flex-1 and flex-end to align right
        rx.box(
            rx.button(
                rx.flex(
                    rx.icon(
                        "plus", size=24, color="rgb(75, 85, 99)", class_name="md:hidden"
                    ),
                    rx.text(
                        "New Chat",
                        class_name="hidden md:block font-[dm] text-black tracking-wide text-lg font-bold",
                    ),
                    align="center",
                    justify="center",
                    class_name="flex items-center",
                ),
                class_name="text-left p-4 md:p-6 rounded-2xl shadow-[0px_8px_0px_0px_rgba(75,85,99,0.8)] hover:shadow-[0px_4px_0px_0px_rgba(75,85,99,0.8)] hover:translate-y-1 transition-all duration-200 mb-2",
                style={
                    "background": "linear-gradient(135deg, #e2e8f0 0%, #d1d5db 50%, #bcc3ce 100%)",
                    "border": "2px solid #4a5568",
                },
                on_click=[
                    rx.redirect("/"),
                    State.reset_chat,
                ],
            ),
            class_name="flex-1 flex justify-end",
        ),
        class_name="p-4 items-center",
    )


def response_message(message: dict, index: int) -> rx.Component:
    return rx.box(
        rx.cond(
            message["role"] == "user",
            rx.text(
                message["content"],
                class_name="ml-2 text-xl md:text-4xl tracking-wide",
                style={
                    "display": "-webkit-box",
                    "-webkit-line-clamp": "2",
                    "-webkit-box-orient": "vertical",
                    "overflow": "hidden",
                    "text-overflow": "ellipsis",
                },
            ),
            rx.vstack(
                # Citations section
                rx.cond(
                    message.get("citations", []),
                    rx.box(
                        rx.button(
                            rx.hstack(
                                rx.text(
                                    "Sources",
                                    class_name="font-[dm] text-sm md:text-lg font-semibold text-white",
                                ),
                                rx.cond(
                                    State.citations_expanded.get(index, False),
                                    rx.icon(
                                        "chevron-down",
                                        size=24,
                                        class_name="text-white",
                                    ),
                                    rx.icon(
                                        "chevron-right",
                                        size=24,
                                        class_name="text-white",
                                    ),
                                ),
                                class_name="items-center gap-2",
                            ),
                            on_click=State.toggle_citations(index),
                            class_name="w-full text-left p-4 rounded-2xl shadow-[0px_8px_0px_0px_rgba(59,130,246,0.8)] hover:shadow-[0px_4px_0px_0px_rgba(59,130,246,0.8)] hover:translate-y-1 transition-all duration-200 mb-2",
                            style={
                                "background": "linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%)",
                                "border": "2px solid #1e40af",
                            },
                        ),
                        rx.cond(
                            State.citations_expanded.get(index, False),
                            rx.box(
                                rx.foreach(
                                    message.get("citations", []),
                                    lambda citation, citation_index: rx.box(
                                        rx.text(
                                            f"[{citation_index + 1}] {citation}",
                                            class_name="font-[dm] text-sm md:text-lg text-black mb-1",
                                        ),
                                        class_name="mb-1",
                                    ),
                                ),
                                class_name="bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4",
                                width="100%",
                                max_width="100%",
                                overflow_x="auto",
                                style={
                                    "word-wrap": "break-word",
                                    "overflow-wrap": "break-word",
                                },
                            ),
                        ),
                        class_name="mb-4",
                    ),
                ),
                # Thinking tokens collapsible section
                rx.cond(
                    message.get("thinking"),
                    rx.box(
                        rx.button(
                            rx.hstack(
                                rx.text(
                                    "Thinking",
                                    class_name="font-[dm] text-sm md:text-lg font-semibold text-white",
                                ),
                                rx.cond(
                                    State.thinking_expanded.get(index, False),
                                    rx.icon(
                                        "chevron-down",
                                        size=24,
                                        class_name="text-white",
                                    ),
                                    rx.icon(
                                        "chevron-right",
                                        size=24,
                                        class_name="text-white",
                                    ),
                                ),
                                class_name="items-center gap-2",
                            ),
                            on_click=State.toggle_thinking(index),
                            class_name="w-full text-left p-4 rounded-2xl shadow-[0px_8px_0px_0px_rgba(147,51,234,0.8)] hover:shadow-[0px_4px_0px_0px_rgba(147,51,234,0.8)] hover:translate-y-1 transition-all duration-200 mb-2",
                            style={
                                "background": "linear-gradient(135deg, #a855f7 0%, #8b5cf6 50%, #7c3aed 100%)",
                                "border": "2px solid #6d28d9",
                            },
                        ),
                        rx.cond(
                            State.thinking_expanded.get(index, False),
                            rx.box(
                                rx.markdown(
                                    message["thinking"],
                                    component_map=markdown_component_map(),
                                    class_name="font-[dm] text-sm md:text-lg text-black",
                                ),
                                class_name="bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4",
                                width="100%",
                                max_width="100%",
                                overflow_x="auto",
                                style={
                                    "word-wrap": "break-word",
                                    "overflow-wrap": "break-word",
                                },
                            ),
                        ),
                        class_name="mb-4",
                    ),
                ),
                rx.box(
                    # Assistant message content
                    rx.markdown(
                        message["content"],
                        component_map=markdown_component_map(),
                        class_name="font-[dm] text-sm md:text-lg",
                    ),
                    class_name="bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4",
                    width="100%",
                    max_width="100%",
                    overflow_x="auto",
                    style={
                        "word-wrap": "break-word",
                        "overflow-wrap": "break-word",
                    },
                ),
                # Performance stats with hero component design style
                rx.cond(
                    message.get("generation_time"),
                    rx.flex(
                        rx.flex(
                            rx.text(
                                f"{message.get('tokens_per_second', 'N/A'):.2f} TOKENS/SEC",
                                class_name="font-[dm] text-xs md:text-sm font-bold text-black",
                            ),
                            class_name="bg-purple-300 rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]",
                        ),
                        rx.flex(
                            rx.text(
                                f"{message.get('total_tokens', 'N/A'):.2f} TOKENS",
                                class_name="font-[dm] text-xs md:text-sm font-bold text-black",
                            ),
                            class_name="bg-sky-300 rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]",
                        ),
                        rx.flex(
                            rx.text(
                                f"{message.get('generation_time', 'N/A'):.2f} SEC",
                                class_name="font-[dm] text-xs md:text-sm font-bold text-black",
                            ),
                            class_name="bg-amber-300 rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]",
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
            rx.vstack(
                rx.hstack(
                    rx.skeleton(
                        class_name="h-4 w-32 rounded-full bg-gray-200 dark:bg-gray-700",
                        loading=State.is_gen,
                    ),
                    class_name="w-full items-start gap-3 px-4 py-2",
                ),
                rx.hstack(
                    rx.skeleton(
                        class_name="h-4 w-full rounded-lg bg-gray-200 dark:bg-gray-700",
                        loading=State.is_gen,
                    ),
                    class_name="w-full px-4 py-2",
                ),
                rx.hstack(
                    rx.skeleton(
                        class_name="h-4 w-3/4 rounded-lg bg-gray-200 dark:bg-gray-700",
                        loading=State.is_gen,
                    ),
                    class_name="w-full px-4 py-1",
                ),
                rx.hstack(
                    rx.skeleton(
                        class_name="h-4 w-1/2 rounded-lg bg-gray-200 dark:bg-gray-700",
                        loading=State.is_gen,
                    ),
                    class_name="w-full px-4 py-1 pb-4",
                ),
                class_name="w-full space-y-1 py-2 animate-pulse",
            ),
        ),
        class_name="flex-1 overflow-y-scroll p-4 md:p-6 space-y-4 max-w-4xl mx-auto w-full pb-24 md:pb-32 hide-scrollbar",
    )
