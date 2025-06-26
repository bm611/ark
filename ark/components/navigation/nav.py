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
                        class_name="flex gap-3",
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
                class_name="flex justify-center items-center cursor-pointer",
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
                class_name="flex gap-2 md:hidden",
            ),
            # Desktop navigation (hidden on mobile)
            rx.hstack(
                rx.button(
                    rx.text("History", class_name="text-white font-semibold"),
                    class_name=(
                        "p-2 rounded-xl text-white text-sm transition-all duration-200 font-[dm] font-semibold flex items-center justify-center "
                        "shadow-[0px_4px_0px_0px_rgb(251,191,36,0.6)] "
                        "hover:shadow-[0px_6px_0px_0px_rgb(251,191,36,0.8)] "
                        "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgb(251,191,36,0.6)] active:translate-y-1 "
                        "md:px-3 md:py-4 md:rounded-xl md:text-lg "
                        "lg:px-2 lg:py-3 lg:rounded-lg lg:text-base "
                        "xl:px-6 xl:py-8 xl:rounded-3xl xl:text-xl"
                    ),
                    style={
                        "background": "linear-gradient(135deg, rgba(251,191,36,0.85) 0%, rgba(245,158,11,0.85) 50%, rgba(202,138,4,0.85) 100%)",
                        "border": "1px solid rgba(202,138,4,0.7)",
                    },
                    on_click=rx.redirect("/history"),
                ),
                rx.button(
                    rx.text("Changelog", class_name="text-white font-semibold"),
                    class_name=(
                        "p-2 rounded-xl text-white text-sm transition-all duration-200 font-[dm] font-semibold flex items-center justify-center "
                        "shadow-[0px_4px_0px_0px_rgb(147,51,234,0.6)] "
                        "hover:shadow-[0px_6px_0px_0px_rgb(147,51,234,0.8)] "
                        "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgb(147,51,234,0.6)] active:translate-y-1 "
                        "md:px-3 md:py-4 md:rounded-xl md:text-lg "
                        "lg:px-2 lg:py-3 lg:rounded-lg lg:text-base "
                        "xl:px-6 xl:py-8 xl:rounded-3xl xl:text-xl"
                    ),
                    style={
                        "background": "linear-gradient(135deg, rgba(168,85,247,0.7) 0%, rgba(147,51,234,0.7) 50%, rgba(124,58,237,0.7) 100%)",
                        "border": "1px solid rgba(124,58,237,0.7)",
                    },
                    on_click=rx.redirect("/changelog"),
                ),
                rx.button(
                    rx.text("Github", class_name="text-white font-semibold"),
                    class_name=(
                        "p-2 rounded-xl text-white text-sm transition-all duration-200 font-[dm] font-semibold flex items-center justify-center "
                        "shadow-[0px_4px_0px_0px_rgb(59,130,246,0.6)] "
                        "hover:shadow-[0px_6px_0px_0px_rgb(59,130,246,0.8)] "
                        "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgb(59,130,246,0.6)] active:translate-y-1 "
                        "md:px-3 md:py-4 md:rounded-xl md:text-lg "
                        "lg:px-2 lg:py-3 lg:rounded-lg lg:text-base "
                        "xl:px-6 xl:py-8 xl:rounded-3xl xl:text-xl"
                    ),
                    style={
                        "background": "linear-gradient(135deg, rgba(96,165,250,0.7) 0%, rgba(59,130,246,0.7) 50%, rgba(37,99,235,0.7) 100%)",
                        "border": "1px solid rgba(37,99,235,0.7)",
                    },
                    on_click=rx.redirect(
                        "https://github.com/bm611/ark", is_external=True
                    ),
                ),
                # Authentication buttons
                clerk.signed_out(
                    rx.hstack(
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
                        class_name="flex gap-3",
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
                        class_name="flex gap-3",
                    )
                ),
                rx.button(
                    rx.cond(
                        State.is_dark_theme,
                        rx.icon("sun", size=18, class_name="text-white"),
                        rx.icon("moon", size=18, class_name="text-white"),
                    ),
                    class_name=(
                        "p-2 rounded-xl text-white text-sm transition-all duration-200 font-[dm] font-semibold flex items-center justify-center gap-2 "
                        "shadow-[0px_4px_0px_0px_rgb(75,85,99,0.6)] "
                        "hover:shadow-[0px_6px_0px_0px_rgb(75,85,99,0.8)] "
                        "hover:brightness-110 active:shadow-[0px_2px_0px_0px_rgb(75,85,99,0.6)] active:translate-y-1 "
                        "md:px-3 md:py-4 md:rounded-xl md:text-lg "
                        "lg:px-2 lg:py-3 lg:rounded-lg lg:text-base "
                        "xl:px-6 xl:py-8 xl:rounded-3xl xl:text-xl"
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
                    on_click=State.toggle_theme,
                ),
                class_name="hidden md:flex gap-3",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4",
    )
