import reflex as rx
from ark.state import State
import reflex_clerk_api as clerk


def mobile_menu_item(icon: str, text: str, on_click_action) -> rx.Component:
    """Individual mobile menu item component"""
    return rx.box(
        rx.flex(
            rx.icon(
                icon,
                size=36,
                class_name=rx.cond(State.is_dark_theme, "text-white", "text-gray-900"),
            ),
            rx.text(
                text,
                class_name=rx.cond(
                    State.is_dark_theme,
                    "font-bold text-white text-4xl",
                    "font-bold text-gray-900 text-4xl",
                ),
            ),
            class_name="w-full gap-6 justify-start items-center",
        ),
        on_click=on_click_action,
        class_name=rx.cond(
            State.is_dark_theme,
            "py-3 hover:bg-gray-700/30 cursor-pointer transition-colors duration-200",
            "py-3 hover:bg-gray-100/50 cursor-pointer transition-colors duration-200",
        ),
    )


def mobile_menu_dropdown() -> rx.Component:
    """Fullscreen mobile menu overlay"""
    return rx.cond(
        State.is_mobile_menu_open,
        rx.box(
            # Fullscreen overlay content
            rx.flex(
                mobile_menu_item(
                    "history",
                    "History",
                    [State.close_mobile_menu, rx.redirect("/history")],
                ),
                mobile_menu_item(
                    "scroll-text",
                    "Changelog",
                    [State.close_mobile_menu, rx.redirect("/changelog")],
                ),
                mobile_menu_item(
                    "circle-help",
                    "How it Works",
                    [State.close_mobile_menu, rx.redirect("/how-it-works")],
                ),
                mobile_menu_item(
                    "github",
                    "Github",
                    [
                        State.close_mobile_menu,
                        rx.redirect("https://github.com/bm611/ark", is_external=True),
                    ],
                ),
                rx.box(
                    rx.flex(
                        rx.cond(
                            State.is_dark_theme,
                            rx.icon("sun", size=36, class_name="text-white"),
                            rx.icon("moon", size=36, class_name="text-gray-900"),
                        ),
                        rx.text(
                            "Theme",
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "font-bold text-white text-4xl",
                                "font-bold text-gray-900 text-4xl",
                            ),
                        ),
                        class_name="w-full gap-6 justify-start items-center",
                    ),
                    on_click=State.toggle_theme_and_close_menu,
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "py-3 hover:bg-gray-700/30 cursor-pointer transition-colors duration-200",
                        "py-3 hover:bg-gray-100/50 cursor-pointer transition-colors duration-200",
                    ),
                ),
                clerk.signed_out(
                    rx.hstack(
                        clerk.sign_in_button(
                            rx.button(
                                rx.text(
                                    "Sign In", class_name="text-white font-semibold"
                                ),
                                class_name=(
                                    "mt-10 px-6 py-8 rounded-3xl text-white text-3xl transition-all font-[dm] font-semibold flex items-center justify-center "
                                    "shadow-[0px_4px_0px_0px_rgb(34,197,94,0.6)] "
                                    "hover:shadow-[0px_6px_0px_0px_rgb(34,197,94,0.8)] "
                                    "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgb(34,197,94,0.6)] active:translate-y-1 "
                                ),
                                style={
                                    "background": "linear-gradient(135deg, rgba(34,197,94,0.7) 0%, rgba(22,163,74,0.7) 50%, rgba(21,128,61,0.7) 100%)",
                                    "border": "1px solid rgba(21,128,61,0.7)",
                                },
                            )
                        ),
                        class_name="flex gap-1 md:gap-1 lg:gap-2 xl:gap-3",
                        on_click=State.close_mobile_menu,
                    )
                ),
                clerk.signed_in(
                    rx.hstack(
                        clerk.sign_out_button(
                            rx.button(
                                rx.text(
                                    "Sign Out", class_name="text-white font-semibold"
                                ),
                                class_name=(
                                    "mt-10 px-6 py-8 rounded-3xl text-white text-3xl transition-all duration-200 font-[dm] font-semibold flex items-center justify-center "
                                    "shadow-[0px_4px_0px_0px_rgb(239,68,68,0.6)] "
                                    "hover:shadow-[0px_6px_0px_0px_rgb(239,68,68,0.8)] "
                                    "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgb(239,68,68,0.6)] active:translate-y-1 "
                                ),
                                style={
                                    "background": "linear-gradient(135deg, rgba(239,68,68,0.7) 0%, rgba(220,38,38,0.7) 50%, rgba(185,28,28,0.7) 100%)",
                                    "border": "1px solid rgba(185,28,28,0.7)",
                                },
                            )
                        ),
                        class_name="",
                        on_click=State.close_mobile_menu,
                    )
                ),
                direction="column",
                align="start",
                justify="start",
                class_name="h-full w-full pt-8 px-8",
            ),
            position="fixed",
            top="90px",
            left="0",
            width="100vw",
            height="calc(100vh - 90px)",
            z_index="998",
            class_name=rx.cond(
                State.is_dark_theme,
                "md:hidden backdrop-blur-sm bg-gray-950/95",
                "md:hidden backdrop-blur-sm bg-white/95",
            ),
        ),
    )


def navbar() -> rx.Component:
    return rx.box(
        # Mobile dropdown menu
        mobile_menu_dropdown(),
        rx.hstack(
            # Left section - Logo
            rx.hstack(
                rx.button(
                    rx.icon("ship"),
                    rx.text(
                        "Ark",
                        class_name="text-xl md:text-2xl lg:text-xl xl:text-3xl font-bold mt-1 text-neutral-50",
                    ),
                    class_name=(
                        "px-4 py-4 rounded-xl transition-all duration-200 "
                        "shadow-[0px_4px_0px_0px_rgba(30,41,59,0.6)] "
                        "hover:shadow-[0px_6px_0px_0px_rgba(30,41,59,0.8)] "
                        "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgba(30,41,59,0.6)] active:translate-y-1 "
                        "md:px-3 md:py-4 md:rounded-xl md:text-lg "
                        "lg:px-2 lg:py-3 lg:rounded-lg lg:text-base "
                        "xl:px-6 xl:py-8 xl:rounded-3xl xl:text-3xl"
                    ),
                    style=rx.cond(
                        State.is_dark_theme,
                        {
                            "background": "linear-gradient(135deg, #3b82f6 0%, #60a5fa 50%, #93c5fd 100%)",
                            "border": "2px solid rgba(59,130,246,0.8)",
                            "backdropFilter": "blur(12px) saturate(180%)",
                            "WebkitBackdropFilter": "blur(12px) saturate(180%)",
                            "backgroundColor": "rgba(15,23,42,0.80)",
                        },
                        {
                            "background": "linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #3b82f6 100%)",
                            "border": "2px solid rgba(30,64,175,0.8)",
                            "backdropFilter": "blur(12px) saturate(180%)",
                            "WebkitBackdropFilter": "blur(12px) saturate(180%)",
                            "backgroundColor": "rgba(255,255,255,0.10)",
                        },
                    ),
                    on_click=rx.redirect("/"),
                ),
                class_name="flex justify-start items-center cursor-pointer",
            ),
            rx.hstack(
                # Hamburger menu
                rx.box(
                    rx.button(
                        rx.cond(
                            State.is_mobile_menu_open,
                            rx.box(
                                rx.box(
                                    class_name="w-6 h-0.5 bg-white transform rotate-45 translate-y-1.5 transition-all duration-300"
                                ),
                                rx.box(
                                    class_name="w-6 h-0.5 bg-white opacity-0 transition-all duration-300"
                                ),
                                rx.box(
                                    class_name="w-6 h-0.5 bg-white transform -rotate-45 -translate-y-1.5 transition-all duration-300"
                                ),
                                class_name="flex flex-col justify-center items-center space-y-1",
                            ),
                            rx.box(
                                rx.box(
                                    class_name="w-6 h-0.5 bg-white transition-all duration-300"
                                ),
                                rx.box(
                                    class_name="w-6 h-0.5 bg-white transition-all duration-300"
                                ),
                                rx.box(
                                    class_name="w-6 h-0.5 bg-white transition-all duration-300"
                                ),
                                class_name="flex flex-col justify-center items-center space-y-1",
                            ),
                        ),
                        class_name=(
                            "md:hidden p-3 rounded-xl transition-all duration-200 "
                            "shadow-[0px_4px_0px_0px_rgba(75,85,99,0.6)] "
                            "hover:shadow-[0px_6px_0px_0px_rgba(75,85,99,0.8)] "
                            "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgba(75,85,99,0.6)] active:translate-y-1"
                        ),
                        style=rx.cond(
                            State.is_dark_theme,
                            {
                                "background": "linear-gradient(135deg, rgba(51,65,85,0.8) 0%, rgba(30,41,59,0.8) 50%, rgba(15,23,42,0.8) 100%)",
                                "border": "1px solid rgba(71,85,105,0.7)",
                            },
                            {
                                "background": "linear-gradient(135deg, rgba(107,114,128,0.7) 0%, rgba(75,85,99,0.7) 50%, rgba(55,65,81,0.7) 100%)",
                                "border": "1px solid rgba(55,65,81,0.7)",
                            },
                        ),
                        on_click=State.toggle_mobile_menu,
                    ),
                ),
                class_name="flex gap-2 md:hidden ml-auto",
            ),
            # Desktop navigation (hidden on mobile) - Three section layout
            rx.hstack(
                # Center navigation with modern tab-style design
                rx.box(
                    rx.hstack(
                        # History Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "history",
                                    size=14,
                                    class_name=rx.cond(
                                        State.is_dark_theme, 
                                        "text-amber-400/80", 
                                        "text-amber-600/80"
                                    ) + " md:size-4 lg:size-4 xl:size-5",
                                ),
                                rx.text(
                                    "History",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-white/90 font-medium text-xs md:text-xs lg:text-sm xl:text-base",
                                        "text-gray-800/90 font-medium text-xs md:text-xs lg:text-sm xl:text-base",
                                    ),
                                ),
                                align="center",
                                justify="center",
                                gap="1",
                                class_name="md:gap-1 lg:gap-2 xl:gap-2",
                            ),
                            class_name=(
                                "group relative px-3 py-2 md:px-2 md:py-1 lg:px-3 lg:py-1 xl:px-5 xl:py-3 "
                                "cursor-pointer transition-all duration-300 ease-in-out "
                                "hover:bg-amber-500/20 hover:scale-105 active:scale-95 "
                                "rounded-xl border-2 border-transparent hover:border-amber-400/50 "
                                "backdrop-blur-sm"
                            ),
                            on_click=rx.redirect("/history"),
                        ),
                        # Vertical Separator
                        rx.box(
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "w-px h-4 md:h-3 lg:h-4 xl:h-6 bg-white/20",
                                "w-px h-4 md:h-3 lg:h-4 xl:h-6 bg-gray-300/50"
                            )
                        ),
                        # Changelog Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "scroll-text",
                                    size=14,
                                    class_name=rx.cond(
                                        State.is_dark_theme, 
                                        "text-purple-400/80", 
                                        "text-purple-600/80"
                                    ) + " md:size-4 lg:size-4 xl:size-5",
                                ),
                                rx.text(
                                    "Changelog",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-white/90 font-medium text-xs md:text-xs lg:text-sm xl:text-base",
                                        "text-gray-800/90 font-medium text-xs md:text-xs lg:text-sm xl:text-base",
                                    ),
                                ),
                                align="center",
                                justify="center",
                                gap="1",
                                class_name="md:gap-1 lg:gap-2 xl:gap-2",
                            ),
                            class_name=(
                                "group relative px-3 py-2 md:px-2 md:py-1 lg:px-3 lg:py-1 xl:px-5 xl:py-3 "
                                "cursor-pointer transition-all duration-300 ease-in-out "
                                "hover:bg-purple-500/20 hover:scale-105 active:scale-95 "
                                "rounded-xl border-2 border-transparent hover:border-purple-400/50 "
                                "backdrop-blur-sm"
                            ),
                            on_click=rx.redirect("/changelog"),
                        ),
                        # Vertical Separator
                        rx.box(
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "w-px h-4 md:h-3 lg:h-4 xl:h-6 bg-white/20",
                                "w-px h-4 md:h-3 lg:h-4 xl:h-6 bg-gray-300/50"
                            )
                        ),
                        # How it Works Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "circle-help",
                                    size=14,
                                    class_name=rx.cond(
                                        State.is_dark_theme, 
                                        "text-green-400/80", 
                                        "text-green-600/80"
                                    ) + " md:size-4 lg:size-4 xl:size-5",
                                ),
                                rx.text(
                                    "How it Works",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-white/90 font-medium text-xs md:text-[10px] lg:text-xs xl:text-base whitespace-nowrap",
                                        "text-gray-800/90 font-medium text-xs md:text-[10px] lg:text-xs xl:text-base whitespace-nowrap",
                                    ),
                                ),
                                align="center",
                                justify="center",
                                gap="1",
                                class_name="md:gap-1 lg:gap-2 xl:gap-2",
                            ),
                            class_name=(
                                "group relative px-3 py-2 md:px-2 md:py-1 lg:px-3 lg:py-1 xl:px-5 xl:py-3 "
                                "cursor-pointer transition-all duration-300 ease-in-out "
                                "hover:bg-green-500/20 hover:scale-105 active:scale-95 "
                                "rounded-xl border-2 border-transparent hover:border-green-400/50 "
                                "backdrop-blur-sm"
                            ),
                            on_click=rx.redirect("/how-it-works"),
                        ),
                        # Vertical Separator
                        rx.box(
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "w-px h-4 md:h-3 lg:h-4 xl:h-6 bg-white/20",
                                "w-px h-4 md:h-3 lg:h-4 xl:h-6 bg-gray-300/50"
                            )
                        ),
                        # Github Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "github",
                                    size=14,
                                    class_name=rx.cond(
                                        State.is_dark_theme, 
                                        "text-blue-400/80", 
                                        "text-blue-600/80"
                                    ) + " md:size-4 lg:size-4 xl:size-5",
                                ),
                                rx.text(
                                    "Github",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-white/90 font-medium text-xs md:text-xs lg:text-sm xl:text-base",
                                        "text-gray-800/90 font-medium text-xs md:text-xs lg:text-sm xl:text-base",
                                    ),
                                ),
                                align="center",
                                justify="center",
                                gap="1",
                                class_name="md:gap-1 lg:gap-2 xl:gap-2",
                            ),
                            class_name=(
                                "group relative px-3 py-2 md:px-2 md:py-1 lg:px-3 lg:py-1 xl:px-5 xl:py-3 "
                                "cursor-pointer transition-all duration-300 ease-in-out "
                                "hover:bg-blue-500/20 hover:scale-105 active:scale-95 "
                                "rounded-xl border-2 border-transparent hover:border-blue-400/50 "
                                "backdrop-blur-sm"
                            ),
                            on_click=rx.redirect("https://github.com/bm611/ark", is_external=True),
                        ),
                        # Vertical Separator
                        rx.box(
                            class_name=rx.cond(
                                State.is_dark_theme,
                                "w-px h-4 md:h-3 lg:h-4 xl:h-6 bg-white/20",
                                "w-px h-4 md:h-3 lg:h-4 xl:h-6 bg-gray-300/50"
                            )
                        ),
                        # Theme Toggle Tab
                        rx.box(
                            rx.flex(
                                rx.cond(
                                    State.is_dark_theme,
                                    rx.icon(
                                        "sun",
                                        size=14,
                                        class_name="text-yellow-400/80 md:size-4 lg:size-4 xl:size-5",
                                    ),
                                    rx.icon(
                                        "moon",
                                        size=14,
                                        class_name="text-slate-600/80 md:size-4 lg:size-4 xl:size-5",
                                    ),
                                ),
                                rx.text(
                                    "Theme",
                                    class_name=rx.cond(
                                        State.is_dark_theme,
                                        "text-white/90 font-medium text-xs md:text-xs lg:text-sm xl:text-base",
                                        "text-gray-800/90 font-medium text-xs md:text-xs lg:text-sm xl:text-base",
                                    ),
                                ),
                                align="center",
                                justify="center",
                                gap="1",
                                class_name="md:gap-1 lg:gap-2 xl:gap-2",
                            ),
                            class_name=(
                                "group relative px-3 py-2 md:px-2 md:py-1 lg:px-3 lg:py-1 xl:px-5 xl:py-3 "
                                "cursor-pointer transition-all duration-300 ease-in-out "
                                "hover:bg-gray-500/20 hover:scale-105 active:scale-95 "
                                "rounded-xl border-2 border-transparent hover:border-gray-400/50 "
                                "backdrop-blur-sm"
                            ),
                            on_click=State.toggle_theme,
                        ),
                        align="center",
                        justify="center",
                        gap="1",
                        class_name="md:gap-0.5 lg:gap-1 xl:gap-3",
                    ),
                    class_name=rx.cond(
                        State.is_dark_theme,
                        (
                            "hidden md:flex absolute left-1/2 transform -translate-x-1/2 "
                            "px-2 py-1 md:px-2 md:py-3 lg:px-3 lg:py-2 xl:px-6 xl:py-3 rounded-2xl "
                            "backdrop-blur-xl border border-white/10 "
                            "shadow-[0px_8px_32px_0px_rgba(0,0,0,0.37)] "
                            "hover:shadow-[0px_12px_40px_0px_rgba(0,0,0,0.5)] "
                            "transition-all duration-300 ease-in-out "
                            "bg-gradient-to-r from-white/5 via-white/10 to-white/5"
                        ),
                        (
                            "hidden md:flex absolute left-1/2 transform -translate-x-1/2 "
                            "px-2 py-1 md:px-2 md:py-3 lg:px-3 lg:py-2 xl:px-6 xl:py-3 rounded-2xl "
                            "backdrop-blur-xl border border-gray-200/50 "
                            "shadow-[0px_8px_32px_0px_rgba(0,0,0,0.1)] "
                            "hover:shadow-[0px_12px_40px_0px_rgba(0,0,0,0.15)] "
                            "transition-all duration-300 ease-in-out "
                            "bg-gradient-to-r from-white/80 via-white/90 to-white/80"
                        ),
                    ),
                ),
                # Right section - Authentication buttons only
                rx.hstack(
                    clerk.signed_out(
                        clerk.sign_in_button(
                            rx.button(
                                rx.text(
                                    "Sign In", class_name="text-white font-semibold"
                                ),
                                class_name=(
                                    "p-2 rounded-xl text-white text-sm transition-all duration-200 font-[dm] font-semibold flex items-center justify-center "
                                    "shadow-[0px_4px_0px_0px_rgb(34,197,94,0.6)] "
                                    "hover:shadow-[0px_6px_0px_0px_rgb(34,197,94,0.8)] "
                                    "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgb(34,197,94,0.6)] active:translate-y-1 "
                                    "md:px-3 md:py-4 md:rounded-xl md:text-lg "
                                    "lg:px-2 lg:py-3 lg:rounded-lg lg:text-base "
                                    "xl:px-6 xl:py-8 xl:rounded-3xl xl:text-xl"
                                ),
                                style={
                                    "background": "linear-gradient(135deg, rgba(34,197,94,0.7) 0%, rgba(22,163,74,0.7) 50%, rgba(21,128,61,0.7) 100%)",
                                    "border": "1px solid rgba(21,128,61,0.7)",
                                },
                            )
                        ),
                    ),
                    clerk.signed_in(
                        clerk.sign_out_button(
                            rx.button(
                                rx.text(
                                    "Sign Out", class_name="text-white font-semibold"
                                ),
                                class_name=(
                                    "p-2 rounded-xl text-white text-sm transition-all duration-200 font-[dm] font-semibold flex items-center justify-center "
                                    "shadow-[0px_4px_0px_0px_rgb(239,68,68,0.6)] "
                                    "hover:shadow-[0px_6px_0px_0px_rgb(239,68,68,0.8)] "
                                    "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgb(239,68,68,0.6)] active:translate-y-1 "
                                    "md:px-3 md:py-4 md:rounded-xl md:text-lg "
                                    "lg:px-2 lg:py-3 lg:rounded-lg lg:text-base "
                                    "xl:px-6 xl:py-8 xl:rounded-3xl xl:text-xl"
                                ),
                                style={
                                    "background": "linear-gradient(135deg, rgba(239,68,68,0.7) 0%, rgba(220,38,38,0.7) 50%, rgba(185,28,28,0.7) 100%)",
                                    "border": "1px solid rgba(185,28,28,0.7)",
                                },
                            )
                        ),
                    ),
                    class_name="hidden md:flex ml-auto",
                ),
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4",
    )
