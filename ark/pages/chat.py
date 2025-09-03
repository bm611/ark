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
            class_name="font-bold text-3xl tracking-tight text-black",
        ),
        "h2": lambda text: rx.heading(
            text,
            size="3",
            margin_y="1em",
            class_name="font-bold text-2xl tracking-tight text-black",
        ),
        "h3": lambda text: rx.heading(
            text,
            size="1",
            margin_y="1em",
            class_name="font-bold text-xl tracking-tight text-black",
        ),
        "h4": lambda text: rx.heading(
            text,
            size="1",
            margin_y="1em",
            class_name="font-bold text-xl tracking-tight text-black",
        ),
        "p": lambda text: rx.text(text, margin_y="1em", class_name="text-black"),
        "code": lambda text: rx.code(
            text,
            class_name="font-mono text-sm bg-gray-200 text-black px-1.5 py-0.5 border border-black",
        ),
        "codeblock": lambda text, **props: rx.box(
            rx.box(
                rx.text(
                    props.get("language", "text"),
                    class_name="text-gray-500 font-mono text-xs font-semibold",
                ),
                rx.button(
                    rx.icon("copy", size=14),
                    rx.text("Copy", class_name="ml-1 text-xs font-mono"),
                    on_click=[rx.set_clipboard(text), rx.toast("Copied!")],
                    variant="ghost",
                    size="1",
                    class_name="text-gray-500 hover:text-black hover:bg-gray-200 px-2 py-1 rounded-md transition-colors duration-200",
                ),
                class_name="flex justify-between items-center px-4 py-2 bg-gray-100 border-b-2 border-black",
            ),
            rx.code_block(
                text,
                theme=rx.code_block.themes.vsc_dark_plus,
                width="100%",
                overflow_x="auto",
                custom_style={
                    "font-size": "14px",
                    "font_family": "'Fira Code', monospace",
                },
            ),
            margin_y="1.5em",
            class_name="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] overflow-hidden",
        ),
        "a": lambda text, **props: rx.link(
            text, **props, color="blue.500", _hover={"color": "blue.700"}
        ),
        "table": lambda children: rx.box(
            rx.box(children, class_name="p-4"),
            class_name="border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] my-4",
            overflow_x="auto",
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
            rx.box(
                rx.vstack(
                    rx.text(
                        message.get("display_text", message["content"]),
                        class_name="text-2xl md:text-4xl font-bold tracking-tight text-black",
                        style={
                            "display": "-webkit-box",
                            "-webkit-line-clamp": "2",
                            "-webkit-box-orient": "vertical",
                            "overflow": "hidden",
                            "text-overflow": "ellipsis",
                        },
                    ),
                    # File preview section for user messages
                    rx.cond(
                        message.get("files") & (message.get("files", []).length() > 0),
                        rx.box(
                            rx.hstack(
                                rx.foreach(
                                    message.get("files", []),
                                    lambda file_ref: rx.cond(
                                        file_ref["content_type"].startswith("image/"),
                                        # Image display
                                        rx.image(
                                            src=file_ref.get("presigned_url") | file_ref.get("base64_url"),
                                            class_name="rounded-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]",
                                            style={
                                                "max-width": "200px",
                                                "max-height": "200px",
                                                "object-fit": "contain",
                                            },
                                        ),
                                        # File display (PDF, etc.)
                                        rx.box(
                                            rx.hstack(
                                                rx.icon("file-text", size=18, color="#000"),
                                                rx.text(
                                                    file_ref.get("original_filename") | file_ref.get("filename"),
                                                    class_name="text-sm text-black font-bold",
                                                ),
                                                align="center",
                                                spacing="2",
                                            ),
                                            class_name="bg-gray-200 border-2 border-black rounded-lg px-4 py-3 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]",
                                        ),
                                    ),
                                ),
                                wrap="wrap",
                                spacing="3",
                                class_name="mt-4",
                            ),
                        ),
                    ),
                    spacing="2",
                    align_items="start",
                ),
                class_name="p-4 md:p-6 bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]",
            ),
            # Assistant's message
            rx.box(
                rx.vstack(
                    # Buttons section
                    rx.hstack(
                        # Citations section
                        rx.cond(
                            message.get("citations", []),
                            expandable_section_button(
                                label="Sources",
                                icon="list",
                                is_expanded=State.citations_expanded.get(index, False),
                                on_click=State.toggle_citations(index),
                            ),
                        ),
                        # Thinking tokens collapsible section
                        rx.cond(
                            message.get("thinking"),
                            expandable_section_button(
                                label="Thinking",
                                icon="lightbulb",
                                is_expanded=State.thinking_expanded.get(index, False),
                                on_click=State.toggle_thinking(index),
                            ),
                        ),
                        class_name="gap-2 mb-4 flex-wrap",
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
                                        class_name="font-mono text-sm md:text-base text-black underline",
                                    ),
                                    class_name="mb-1",
                                ),
                            ),
                            class_name="p-4 bg-yellow-200 border-2 border-black",
                            width="100%",
                        ),
                    ),
                    rx.cond(
                        State.thinking_expanded.get(index, False),
                        rx.box(
                            rx.markdown(
                                message["thinking"],
                                component_map=markdown_component_map(),
                                class_name="font-mono text-sm md:text-base text-black",
                            ),
                            class_name="p-4 bg-blue-200 border-2 border-black",
                            width="100%",
                        ),
                    ),
                    # Main content
                    rx.cond(
                        message.get("content"),
                        rx.markdown(
                            message["content"],
                            component_map=markdown_component_map(),
                            class_name="font-sans text-base md:text-lg text-black",
                        ),
                    ),
                    # Performance stats
                    rx.cond(
                        message.get("generation_time"),
                        rx.flex(
                            rx.flex(
                                rx.text(
                                    f"{message.get('tokens_per_second', 'N/A'):.2f} TOKENS/SEC",
                                    class_name="font-black text-xs text-black uppercase",
                                ),
                                class_name="bg-purple-300 p-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]",
                            ),
                            rx.flex(
                                rx.text(
                                    f"{message.get('total_tokens', 'N/A')} TOKENS",
                                    class_name="font-black text-xs text-black uppercase",
                                ),
                                class_name="bg-sky-300 p-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]",
                            ),
                            rx.flex(
                                rx.text(
                                    f"{message.get('generation_time', 'N/A'):.2f} SEC",
                                    class_name="font-black text-xs text-black uppercase",
                                ),
                                class_name="bg-amber-300 p-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]",
                            ),
                            class_name="gap-2 md:gap-4 mt-4",
                        ),
                    ),
                    spacing="2",
                    align_items="start",
                ),
                class_name="p-4 md:p-6 bg-gray-100 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mt-4",
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
                    class_name="w-full text-black text-base md:text-lg rounded-none h-12 border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] focus:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] focus:translate-x-1 focus:translate-y-1 transition-all duration-100 pl-4 pr-14 outline-none",
                    style={
                        "background": "#FFFFFF",
                        "color": "#000000",
                        "&::placeholder": {
                            "color": "#374151",
                            "font-weight": "600",
                        },
                    },
                    on_change=State.set_prompt,
                ),
                rx.button(
                    rx.icon("arrow-right", size=24, color="black"),
                    class_name="absolute right-2 top-1/2 transform -translate-y-1/2 bg-yellow-400 border-2 border-black h-8 w-8 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[1px_1px_0px_0px_rgba(0,0,0,1)] hover:translate-x-0.5 hover:translate-y-0.5 active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] active:translate-x-1 active:translate-y-1 transition-all duration-100",
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
        class_name="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-lg border-t-4 border-black",
    )


def chat_messages():
    return rx.box(
        rx.foreach(
            State.messages,
            lambda message, index: response_message(message, index),
        ),
        class_name="flex-1 overflow-y-scroll p-4 md:p-6 space-y-8 max-w-4xl mx-auto w-full pb-32 md:pb-40",
    )
