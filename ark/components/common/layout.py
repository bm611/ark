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
        class_name=f"bg-white border-2 border-{border_color} p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-4",
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
            class_name="font-bold text-xs md:text-sm text-black",
        ),
        class_name=f"hidden md:flex {color_class} p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]",
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
            class_name="font-bold text-xs md:text-sm text-black",
        ),
        class_name=f"{color_class} p-2 md:p-3 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]",
    )


def loading_skeleton() -> rx.Component:
    """Reusable loading skeleton component."""
    return rx.vstack(
        rx.hstack(
            rx.text(
                "Generating Response...",
                class_name="text-lg font-semibold text-gray-600 bg-gradient-to-r from-gray-600 via-gray-800 to-gray-600 bg-clip-text text-transparent animate-pulse bg-[length:200%_100%] animate-[shimmer_2s_infinite]",
            ),
            class_name="w-full justify-left px-4 py-4",
        ),
        rx.hstack(
            rx.skeleton(
                class_name="h-4 w-32 rounded-full bg-gray-200",
                loading=True,
            ),
            class_name="w-full items-start gap-3 px-4 py-2",
        ),
        rx.hstack(
            rx.skeleton(
                class_name="h-4 w-full rounded-lg bg-gray-200",
                loading=True,
            ),
            class_name="w-full px-4 py-2",
        ),
        rx.hstack(
            rx.skeleton(
                class_name="h-4 w-3/4 rounded-lg bg-gray-200",
                loading=True,
            ),
            class_name="w-full px-4 py-1",
        ),
        rx.hstack(
            rx.skeleton(
                class_name="h-4 w-1/2 rounded-lg bg-gray-200",
                loading=True,
            ),
            class_name="w-full px-4 py-1 pb-4",
        ),
        class_name="w-full space-y-1 py-2 animate-pulse",
        style={
            "@keyframes shimmer": {
                "0%": {"background-position": "-200% 0"},
                "100%": {"background-position": "200% 0"},
            }
        },
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
                        color="black",
                        class_name="md:hidden",
                    ),
                    rx.text(
                        "New Chat",
                        class_name="hidden md:block font-bold text-black tracking-wide text-lg",
                    ),
                    align="center",
                    justify="center",
                    class_name="flex items-center",
                ),
                class_name="text-left p-4 md:p-6 bg-gray-200 border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:translate-x-1 hover:translate-y-1 transition-all duration-200 mb-2",
                on_click=new_chat_handler,
            ),
            class_name="flex-1 flex justify-end",
        ),
        class_name="p-4 items-center",
    )
