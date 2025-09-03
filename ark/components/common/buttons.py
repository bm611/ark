"""
Reusable button components.
"""

import reflex as rx
from typing import Any
from ark.state import State


def action_button(
    label: str,
    icon: str,
    is_active: bool = False,
    bg_color: str = "white",
    active_bg_color: str = "#22c55e",
    shadow_color: str = "rgba(0,0,0,1)",
    on_click: Any = None,
    **kwargs,
) -> rx.Component:
    """
    Reusable action button component.

    Args:
        label: Button text
        icon: Icon name
        is_active: Whether button is in active state
        bg_color: Background color for inactive state
        active_bg_color: Background color for active state
        shadow_color: Shadow color for active state
        on_click: Click handler
    """
    return rx.button(
        rx.hstack(
            rx.icon(
                icon,
                size=16,
                color=rx.cond(is_active, "white", "black"),
            ),
            rx.cond(
                label != "",
                rx.text(
                    label,
                    class_name="font-bold text-xs md:text-sm",
                    color=rx.cond(is_active, "white", "black"),
                ),
                None,
            ),
            class_name="items-center gap-1 md:gap-2",
        ),
        on_click=on_click,
        class_name=f"text-left px-2 py-1 md:p-2 border-2 border-black shadow-[4px_4px_0px_0px_{shadow_color}] hover:shadow-[2px_2px_0px_0px_{shadow_color}] hover:translate-x-1 hover:translate-y-1 active:shadow-[0px_0px_0px_0px_{shadow_color}] active:translate-x-2 active:translate-y-2 transition-all duration-100 ml-2",
        style={
            "background": rx.cond(is_active, active_bg_color, bg_color),
        },
        **kwargs,
    )


def expandable_section_button(
    label: str,
    icon: str,
    is_expanded: bool,
    bg_color: str = "#3b82f6",
    shadow_color: str = "rgba(0,0,0,1)",
    on_click: Any = None,
) -> rx.Component:
    """
    Reusable expandable section button.

    Args:
        label: Button text
        icon: Icon name
        is_expanded: Whether section is expanded
        bg_color: Background color
        shadow_color: Shadow color
        on_click: Click handler
    """
    return rx.button(
        rx.hstack(
            rx.icon(
                icon,
                size=16,
                color="white",
            ),
            rx.text(
                label,
                class_name="font-bold text-xs md:text-sm text-white",
            ),
            rx.icon(
                rx.cond(is_expanded, "chevron-down", "chevron-right"),
                size=16,
                color="white",
            ),
            class_name="items-center gap-1",
        ),
        on_click=on_click,
        class_name=f"text-left p-2 border-2 border-black shadow-[4px_4px_0px_0px_{shadow_color}] hover:shadow-[2px_2px_0px_0px_{shadow_color}] hover:translate-x-1 hover:translate-y-1 active:shadow-[0px_0px_0px_0px_{shadow_color}] active:translate-x-2 active:translate-y-2 transition-all duration-100",
        style={
            "background": bg_color,
        },
    )


def gradient_card(
    title: str,
    description: str,
    image_src: str,
    bg_color: str = "#FBBF24",
) -> rx.Component:
    """
    Reusable gradient card component.

    Args:
        title: Card title
        description: Card description
        image_src: Image source URL
        bg_color: Background color
    """
    return rx.box(
        rx.flex(
            rx.image(
                src=image_src,
                class_name="w-20 h-20 object-contain",
            ),
            rx.box(
                rx.heading(
                    title,
                    class_name="text-2xl font-bold text-black",
                    as_="h2",
                ),
                rx.text(
                    description,
                    class_name="text-md text-black",
                ),
            ),
            direction="column",
            align="center",
            justify="center",
            spacing="4",
        ),
        class_name=f"p-6 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]",
        style={
            "background": bg_color,
        },
    )


def performance_metric(
    value: str, label: str, color_class: str = "bg-purple-300", **kwargs
) -> rx.Component:
    """
    Reusable performance metric component.

    Args:
        value: Metric value
        label: Metric label
        color_class: Background color class
    """
    return rx.flex(
        rx.text(
            f"{value} {label}",
            class_name="font-bold text-xs text-black",
        ),
        class_name=f"{color_class} p-2 items-center border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]",
        **kwargs,
    )
