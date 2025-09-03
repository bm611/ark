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
                class_name="text-gray-900",
            ),
            rx.text(
                text,
                class_name="font-bold text-gray-900 text-4xl",
            ),
            class_name="w-full gap-6 justify-start items-center",
        ),
        on_click=on_click_action,
        class_name="py-3 hover:bg-gray-100/50 cursor-pointer transition-colors duration-200",
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
            class_name="md:hidden backdrop-blur-sm bg-white/95",
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
                    rx.icon("ship", size=24),
                    rx.text(
                        "ARK",
                        class_name="text-xl md:text-2xl font-black uppercase tracking-tight text-black",
                    ),
                    class_name=(
                        "px-4 py-3 bg-yellow-400 border-4 border-black "
                        "shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] "
                        "hover:shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] "
                        "hover:translate-x-1 hover:translate-y-1 "
                        "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                        "active:translate-x-2 active:translate-y-2 "
                        "transition-all duration-100 "
                        "md:px-6 md:py-4 "
                        "lg:px-8 lg:py-6"
                    ),
                    style={
                        "background": "#FBBF24",
                        "border": "4px solid #000000",
                    },
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
                                    class_name="w-6 h-0.5 bg-black transform rotate-45 translate-y-1.5 transition-all duration-300"
                                ),
                                rx.box(
                                    class_name="w-6 h-0.5 bg-black opacity-0 transition-all duration-300"
                                ),
                                rx.box(
                                    class_name="w-6 h-0.5 bg-black transform -rotate-45 -translate-y-1.5 transition-all duration-300"
                                ),
                                class_name="flex flex-col justify-center items-center space-y-1",
                            ),
                            rx.box(
                                rx.box(
                                    class_name="w-6 h-0.5 bg-black transition-all duration-300"
                                ),
                                rx.box(
                                    class_name="w-6 h-0.5 bg-black transition-all duration-300"
                                ),
                                rx.box(
                                    class_name="w-6 h-0.5 bg-black transition-all duration-300"
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
                        style={
                            "background": "linear-gradient(135deg, rgba(107,114,128,0.7) 0%, rgba(75,85,99,0.7) 50%, rgba(55,65,81,0.7) 100%)",
                            "border": "1px solid rgba(55,65,81,0.7)",
                        },
                        on_click=State.toggle_mobile_menu,
                    ),
                ),
                class_name="flex gap-2 md:hidden ml-auto",
            ),
            # Desktop navigation (hidden on mobile) - Neo-Brutal tab design
            rx.hstack(
                # Center navigation with neo-brutal tab-style design
                rx.box(
                    rx.hstack(
                        # History Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "history",
                                    size=18,
                                    class_name="text-black"
                                ),
                                rx.text(
                                    "HISTORY",
                                    class_name="text-black font-black text-xs md:text-sm uppercase tracking-wider",
                                ),
                                align="center",
                                justify="center",
                                gap="2",
                            ),
                            class_name=(
                                "bg-pink-400 border-4 border-black px-3 py-2 "
                                "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                                "hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] "
                                "hover:translate-x-1 hover:translate-y-1 "
                                "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                "active:translate-x-2 active:translate-y-2 "
                                "cursor-pointer transition-all duration-100"
                            ),
                            on_click=rx.redirect("/history"),
                        ),
                        # Changelog Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "scroll-text",
                                    size=18,
                                    class_name="text-black"
                                ),
                                rx.text(
                                    "CHANGELOG",
                                    class_name="text-black font-black text-xs md:text-sm uppercase tracking-wider",
                                ),
                                align="center",
                                justify="center",
                                gap="2",
                            ),
                            class_name=(
                                "bg-green-400 border-4 border-black px-3 py-2 "
                                "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                                "hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] "
                                "hover:translate-x-1 hover:translate-y-1 "
                                "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                "active:translate-x-2 active:translate-y-2 "
                                "cursor-pointer transition-all duration-100"
                            ),
                            on_click=rx.redirect("/changelog"),
                        ),
                        # How it Works Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "circle-help",
                                    size=18,
                                    class_name="text-black"
                                ),
                                rx.text(
                                    "HOW IT WORKS",
                                    class_name="text-black font-black text-xs md:text-sm uppercase tracking-wider",
                                ),
                                align="center",
                                justify="center",
                                gap="2",
                            ),
                            class_name=(
                                "bg-blue-400 border-4 border-black px-3 py-2 "
                                "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                                "hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] "
                                "hover:translate-x-1 hover:translate-y-1 "
                                "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                "active:translate-x-2 active:translate-y-2 "
                                "cursor-pointer transition-all duration-100"
                            ),
                            on_click=rx.redirect("/how-it-works"),
                        ),
                        # Github Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "github",
                                    size=18,
                                    class_name="text-black"
                                ),
                                rx.text(
                                    "GITHUB",
                                    class_name="text-black font-black text-xs md:text-sm uppercase tracking-wider",
                                ),
                                align="center",
                                justify="center",
                                gap="2",
                            ),
                            class_name=(
                                "bg-purple-400 border-4 border-black px-3 py-2 "
                                "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                                "hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] "
                                "hover:translate-x-1 hover:translate-y-1 "
                                "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                "active:translate-x-2 active:translate-y-2 "
                                "cursor-pointer transition-all duration-100"
                            ),
                            on_click=rx.redirect("https://github.com/bm611/ark", is_external=True),
                        ),
                        # Theme Toggle Tab
                        rx.box(
                            rx.flex(
                                rx.icon(
                                    "sun",
                                    size=18,
                                    class_name="text-black"
                                ),
                                rx.text(
                                    "THEME",
                                    class_name="text-black font-black text-xs md:text-sm uppercase tracking-wider",
                                ),
                                align="center",
                                justify="center",
                                gap="2",
                            ),
                            class_name=(
                                "bg-orange-400 border-4 border-black px-3 py-2 "
                                "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                                "hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] "
                                "hover:translate-x-1 hover:translate-y-1 "
                                "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                "active:translate-x-2 active:translate-y-2 "
                                "cursor-pointer transition-all duration-100"
                            ),
                        ),
                        align="center",
                        justify="center",
                        gap="3",
                    ),
                    class_name="hidden md:flex absolute left-1/2 transform -translate-x-1/2",
                ),
                # Right section - Neo-Brutal Authentication buttons
                rx.hstack(
                    clerk.signed_out(
                        clerk.sign_in_button(
                            rx.button(
                                rx.text(
                                    "SIGN IN", class_name="text-black font-black uppercase tracking-wider"
                                ),
                                class_name=(
                                    "px-4 py-2 bg-green-400 border-4 border-black text-base "
                                    "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                                    "hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] "
                                    "hover:translate-x-1 hover:translate-y-1 "
                                    "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                    "active:translate-x-2 active:translate-y-2 "
                                    "transition-all duration-100 "
                                    "md:px-6 md:py-3"
                                ),
                                style={
                                    "background": "#4ADE80",
                                    "border": "4px solid #000000",
                                },
                            )
                        ),
                    ),
                    clerk.signed_in(
                        clerk.sign_out_button(
                            rx.button(
                                rx.text(
                                    "SIGN OUT", class_name="text-white font-black uppercase tracking-wider"
                                ),
                                class_name=(
                                    "px-4 py-2 bg-red-500 border-4 border-black text-base "
                                    "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                                    "hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] "
                                    "hover:translate-x-1 hover:translate-y-1 "
                                    "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                    "active:translate-x-2 active:translate-y-2 "
                                    "transition-all duration-100 "
                                    "md:px-6 md:py-3"
                                ),
                                style={
                                    "background": "#EF4444",
                                    "border": "4px solid #000000",
                                },
                            )
                        ),
                    ),
                    class_name="hidden md:flex ml-auto",
                ),
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4 bg-white border-b-4 border-black",
    )