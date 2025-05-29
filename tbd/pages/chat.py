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
            theme=rx.code_block.themes.material_oceanic,
            margin_y="1em",
            border_radius="16px",
            custom_style={
                "font-size": "12px",
                "font_family": "Inter",
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
    return rx.box(
        rx.button(
            rx.flex(
                rx.icon(
                    "plus", size=24, color="rgb(75, 85, 99)", class_name="md:hidden"
                ),
                rx.text(
                    "New Chat",
                    class_name="hidden md:block tracking-wide text-lg font-bold",
                ),
                align="center",
                justify="center",
                class_name="flex items-center",
            ),
            class_name="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 transition-all duration-200 text-gray-600 font-[dm] font-semibold shadow-sm hover:shadow-md "
            "w-12 h-12 md:w-auto md:h-auto md:px-6 md:py-3 rounded-xl "
            "flex items-center justify-center ml-auto",
            on_click=[
                rx.redirect("/"),
                State.reset_chat,
            ],
        ),
        class_name="p-4",
    )


def response_message(message: dict) -> rx.Component:
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
                rx.cond(
                    message.get("citations", []),
                    rx.box(
                        rx.text(
                            "Sources:",
                            class_name="text-lg mb-2 tracking-wide",
                        ),
                        rx.foreach(
                            message.get("citations", []),
                            lambda citation, index: rx.box(
                                rx.text(
                                    f"[{index + 1}] {citation}",
                                    class_name="font-[dm] text-sm text-gray-600 mb-1",
                                ),
                                class_name="mb-1",
                            ),
                        ),
                        class_name="mb-4 p-3 bg-gray-50 border border-gray-200 rounded-lg",
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
                        class_name="gap-2 md:gap-4 mb-20",
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
            response_message,
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


def model_provider():
    return rx.center(
        rx.flex(
            rx.flex(
                rx.text(
                    State.selected_provider.upper(),
                    class_name="font-[dm] text-xs md:text-sm font-bold text-black",
                ),
                class_name="bg-green-300 rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]",
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
        # class_name="py-2",
    )
