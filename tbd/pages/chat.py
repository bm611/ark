import reflex as rx
from typing import Dict, Any
from tbd.state import State


def markdown_component_map() -> Dict[str, Any]:
    """Create a component map for markdown to properly handle tables and other elements.

    Returns:
        A dictionary mapping markdown elements to their Reflex components
    """
    return {
        "h1": lambda text: rx.heading(text, size="5", margin_y="1em"),
        "h2": lambda text: rx.heading(text, size="3", margin_y="1em"),
        "h3": lambda text: rx.heading(text, size="1", margin_y="1em"),
        "p": lambda text: rx.text(text, margin_y="1em"),
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
        rx.hstack(
            rx.hstack(
                rx.icon("zap", size=34),
                rx.text("Ark", class_name="text-4xl"),
                class_name="flex justify-center items-center gap-1 cursor-pointer",
                on_click=[
                    rx.redirect("/"),
                    State.reset_chat,
                ],
            ),
            rx.button(
                rx.text("New Chat"),
                class_name="bg-blue-300 hover:bg-blue-500 px-4 md:px-6 py-6 md:py-8 rounded-3xl text-black text-lg md:text-xl transition-colors font-[dm] font-bold flex items-center justify-center",
                on_click=[
                    rx.redirect("/"),
                    State.reset_chat,
                ],
            ),
            class_name="flex justify-between items-center",
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
            rx.box(
                rx.markdown(
                    message["content"],
                    component_map=markdown_component_map(),
                    class_name="font-[dm] text-sm md:text-lg",
                ),
                class_name="bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-20",
            ),
        ),
        class_name="",
    )


def chat_messages():
    return rx.box(
        rx.foreach(
            State.messages,
            response_message,
        ),
        class_name="flex-1 overflow-y-scroll p-4 md:p-6 space-y-4 max-w-4xl mx-auto w-full pb-24 md:pb-32 hide-scrollbar",
    )
