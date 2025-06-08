"""
Reusable layout components.
"""

import reflex as rx
from typing import Any
from ark.state import State


def expandable_content_box(
    content: Any, border_color: str = "black", **kwargs
) -> rx.Component:
    """
    Reusable expandable content box.

    Args:
        content: Content to display
        border_color: Border color
    """
    return rx.box(
        content,
        class_name=rx.cond(
            State.is_dark_theme,
            f"bg-gray-800 border-2 border-gray-600 rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(75,85,99,0.8)] mb-4",
            f"bg-white border-2 border-{border_color} rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4"
        ),
        width="100%",
        max_width="100%",
        overflow_x="auto",
        style={
            "word-wrap": "break-word",
            "overflow-wrap": "break-word",
        },
        **kwargs,
    )


def provider_badge(
    provider_name: str, color_class: str = "bg-green-300"
) -> rx.Component:
    """
    Reusable provider badge component.

    Args:
        provider_name: Name of the provider
        color_class: Background color class
    """
    return rx.flex(
        rx.text(
            provider_name.upper(),
            class_name=rx.cond(
                State.is_dark_theme,
                "font-[dm] text-xs md:text-sm font-bold text-white",
                "font-[dm] text-xs md:text-sm font-bold text-black"
            ),
        ),
        class_name=rx.cond(
            State.is_dark_theme,
            f"hidden md:flex bg-gray-700 rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-gray-600 shadow-[3px_3px_0px_0px_rgba(75,85,99,0.8)] md:shadow-[8px_8px_0px_0px_rgba(75,85,99,0.8)]",
            f"hidden md:flex {color_class} rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
        ),
    )


def model_badge(model_name: str, color_class: str = "bg-pink-300") -> rx.Component:
    """
    Reusable model badge component.

    Args:
        model_name: Name of the model
        color_class: Background color class
    """
    return rx.flex(
        rx.text(
            model_name.upper(),
            class_name=rx.cond(
                State.is_dark_theme,
                "font-[dm] text-xs md:text-sm font-bold text-white",
                "font-[dm] text-xs md:text-sm font-bold text-black"
            ),
        ),
        class_name=rx.cond(
            State.is_dark_theme,
            f"bg-gray-700 rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-gray-600 shadow-[3px_3px_0px_0px_rgba(75,85,99,0.8)] md:shadow-[8px_8px_0px_0px_rgba(75,85,99,0.8)]",
            f"{color_class} rounded-xl p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
        ),
    )


def loading_skeleton() -> rx.Component:
    """Reusable loading skeleton component."""
    return rx.vstack(
        rx.hstack(
            rx.skeleton(
                class_name=rx.cond(
                    State.is_dark_theme,
                    "h-4 w-32 rounded-full bg-gray-700",
                    "h-4 w-32 rounded-full bg-gray-200"
                ),
                loading=True,
            ),
            class_name="w-full items-start gap-3 px-4 py-2",
        ),
        rx.hstack(
            rx.skeleton(
                class_name=rx.cond(
                    State.is_dark_theme,
                    "h-4 w-full rounded-lg bg-gray-700",
                    "h-4 w-full rounded-lg bg-gray-200"
                ),
                loading=True,
            ),
            class_name="w-full px-4 py-2",
        ),
        rx.hstack(
            rx.skeleton(
                class_name=rx.cond(
                    State.is_dark_theme,
                    "h-4 w-3/4 rounded-lg bg-gray-700",
                    "h-4 w-3/4 rounded-lg bg-gray-200"
                ),
                loading=True,
            ),
            class_name="w-full px-4 py-1",
        ),
        rx.hstack(
            rx.skeleton(
                class_name=rx.cond(
                    State.is_dark_theme,
                    "h-4 w-1/2 rounded-lg bg-gray-700",
                    "h-4 w-1/2 rounded-lg bg-gray-200"
                ),
                loading=True,
            ),
            class_name="w-full px-4 py-1 pb-4",
        ),
        class_name="w-full space-y-1 py-2 animate-pulse",
    )


def navigation_header(
    provider_name: str, model_name: str, new_chat_handler: Any = None
) -> rx.Component:
    """
    Reusable navigation header component.

    Args:
        provider_name: Current provider name
        model_name: Current model name
        new_chat_handler: Handler for new chat button
    """
    return rx.hstack(
        # Left side - empty with flex-1 to take equal space
        rx.box(class_name="flex-1"),
        # Middle - Model provider section
        rx.flex(
            provider_badge(provider_name),
            model_badge(model_name),
            class_name="gap-2 md:gap-4",
        ),
        # Right side - New Chat button with flex-1 and flex-end to align right
        rx.box(
            rx.button(
                rx.flex(
                    rx.icon(
                        "plus", 
                        size=24, 
                        color=rx.cond(State.is_dark_theme, "white", "rgb(75, 85, 99)"), 
                        class_name="md:hidden"
                    ),
                    rx.text(
                        "New Chat",
                        class_name=rx.cond(
                            State.is_dark_theme,
                            "hidden md:block font-[dm] text-white tracking-wide text-lg font-bold",
                            "hidden md:block font-[dm] text-black tracking-wide text-lg font-bold"
                        ),
                    ),
                    align="center",
                    justify="center",
                    class_name="flex items-center",
                ),
                class_name="text-left p-4 md:p-6 rounded-2xl shadow-[0px_8px_0px_0px_rgba(75,85,99,0.8)] hover:shadow-[0px_4px_0px_0px_rgba(75,85,99,0.8)] hover:translate-y-1 transition-all duration-200 mb-2",
                style=rx.cond(
                    State.is_dark_theme,
                    {
                        "background": "linear-gradient(135deg, #4b5563 0%, #374151 50%, #1f2937 100%)",
                        "border": "2px solid #6b7280",
                    },
                    {
                        "background": "linear-gradient(135deg, #e2e8f0 0%, #d1d5db 50%, #bcc3ce 100%)",
                        "border": "2px solid #4a5568",
                    }
                ),
                on_click=new_chat_handler,
            ),
            class_name="flex-1 flex justify-end",
        ),
        class_name="p-4 items-center",
    )
