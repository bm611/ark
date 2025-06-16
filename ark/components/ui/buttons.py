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
    gradient_colors: str = "bg-gray-200",
    active_gradient: str = "linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%)",
    active_border: str = "#166534",
    shadow_color: str = "rgba(34,197,94,0.8)",
    on_click: Any = None,
    **kwargs,
) -> rx.Component:
    """
    Reusable action button component.

    Args:
        label: Button text
        icon: Icon name
        is_active: Whether button is in active state
        gradient_colors: CSS background for inactive state
        active_gradient: CSS gradient for active state
        active_border: Border color for active state
        shadow_color: Shadow color for active state
        on_click: Click handler
    """
    return rx.button(
        rx.hstack(
            rx.icon(
                icon,
                size=16,
                class_name=rx.cond(
                    is_active,
                    "text-white",
                    rx.cond(State.is_dark_theme, "text-slate-300", "text-gray-600"),
                ),
            ),
            rx.cond(
                label != "",
                rx.text(
                    label,
                    class_name=rx.cond(
                        is_active,
                        "font-[dm] text-xs md:text-sm font-semibold text-white",
                        rx.cond(
                            State.is_dark_theme,
                            "font-[dm] text-xs md:text-sm font-semibold text-slate-300",
                            "font-[dm] text-xs md:text-sm font-semibold text-gray-600",
                        ),
                    ),
                ),
                None,
            ),
            class_name=rx.cond(
                label != "",
                "items-center gap-1 md:gap-2",
                "items-center",
            ),
        ),
        on_click=on_click,
        class_name=rx.cond(
            is_active,
            f"text-left px-2 py-1 md:p-4 rounded-2xl shadow-[0px_8px_0px_0px_{shadow_color}] active:shadow-[0px_4px_0px_0px_{shadow_color}] active:translate-y-1 transition-all duration-200 ml-2 hover:md:shadow-[0px_4px_0px_0px_{shadow_color}] hover:md:translate-y-1",
            f"text-left px-2 py-1 md:p-4 rounded-2xl shadow-[0px_4px_0px_0px_rgba(107,114,128,0.4)] active:shadow-[0px_8px_0px_0px_{shadow_color}] active:translate-y-1 transition-all duration-200 ml-2 hover:md:shadow-[0px_8px_0px_0px_{shadow_color}] hover:md:translate-y-1",
        ),
        style=rx.cond(
            is_active,
            {
                "background": active_gradient,
                "border": f"1px solid {active_border}",
            },
            rx.cond(
                State.is_dark_theme,
                {
                    "background": "#334155",
                    "border": "1px solid #475569",
                },
                {
                    "background": "white",
                    "border": "1px solid #d1d5db",
                },
            ),
        ),
        **kwargs,
    )


def expandable_section_button(
    label: str,
    icon: str,
    is_expanded: bool,
    gradient: str = "linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%)",
    border_color: str = "#1e40af",
    shadow_color: str = "rgba(59,130,246,0.8)",
    on_click: Any = None,
) -> rx.Component:
    """
    Reusable expandable section button.

    Args:
        label: Button text
        icon: Icon name
        is_expanded: Whether section is expanded
        gradient: CSS gradient background
        border_color: Border color
        shadow_color: Shadow color
        on_click: Click handler
    """
    return rx.button(
        rx.hstack(
            rx.icon(
                icon,
                size=16,
                class_name="text-white",
            ),
            rx.text(
                label,
                class_name="font-[dm] text-xs md:text-sm font-semibold text-white",
            ),
            rx.cond(
                is_expanded,
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
        on_click=on_click,
        class_name=f"text-left p-2 rounded-xl shadow-[0px_4px_0px_0px_{shadow_color}] hover:shadow-[0px_2px_0px_0px_{shadow_color}] hover:translate-y-1 transition-all duration-200",
        style={
            "background": gradient,
            "border": f"2px solid {border_color}",
        },
    )


def gradient_card(
    title: str,
    description: str,
    image_src: str,
    background_color: str = "bg-gradient-to-br from-purple-500 to-pink-500",
) -> rx.Component:
    """
    Reusable gradient card component.

    Args:
        title: Card title
        description: Card description
        image_src: Image source URL
        background_color: Background gradient class
    """
    return rx.box(
        rx.box(
            rx.box(
                rx.flex(
                    rx.box(
                        rx.box(
                            rx.image(
                                src=image_src,
                                class_name="w-20 md:w-28 h-20 md:h-28 object-contain relative z-10",
                            ),
                            class_name="relative",
                        ),
                        rx.box(
                            class_name="absolute inset-0 bg-gradient-to-r from-cyan-400 to-purple-400 blur-xl opacity-50",
                        ),
                        class_name="flex-shrink-0 mr-3 mt-1 md:mr-0 md:mb-8 relative",
                    ),
                    rx.box(
                        rx.heading(
                            title,
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "text-lg md:text-3xl font-black mt-1 mb-1 md:mb-4 tracking-wide bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent text-left",
                                "text-lg md:text-3xl font-black mt-1 mb-1 md:mb-4 tracking-wide bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent text-left",
                            ),
                            as_="h2",
                        ),
                        rx.text(
                            description,
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "font-[dm] text-sm md:text-lg text-slate-300 font-medium text-left",
                                "font-[dm] text-sm md:text-lg text-gray-700 font-medium text-left",
                            ),
                        ),
                        class_name="flex-1",
                    ),
                    direction="row",
                    class_name="md:flex-col",
                    align="start",
                ),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "bg-slate-800/90 backdrop-blur-md rounded-xl md:rounded-3xl p-2 md:p-8 h-full md:h-80 flex flex-col relative overflow-hidden",
                    "bg-white/90 backdrop-blur-md rounded-xl md:rounded-3xl p-2 md:p-8 h-full md:h-80 flex flex-col relative overflow-hidden",
                ),
            ),
            class_name=f"{background_color} p-[2px] rounded-xl md:rounded-3xl shadow-lg md:shadow-2xl shadow-purple-500/25 hover:shadow-purple-500/40 transition-all duration-300",
        ),
        class_name="transform hover:scale-[1.02] transition-transform duration-300",
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
            class_name="font-[dm] text-xs font-bold text-black",
        ),
        class_name=f"{color_class} rounded-xl p-2 items-center border-2 md:border-3 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] md:shadow-[5px_5px_0px_0px_rgba(0,0,0,1)]",
        **kwargs,
    )
