import reflex as rx
from ark.state import State
import reflex_clerk_api as clerk


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.button(
                    rx.icon("ship"),
                    rx.text(
                        "Ark",
                        class_name="text-xl md:text-2xl lg:text-xl xl:text-3xl font-bold mt-1 text-gray-50",
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
                            "backgroundColor": "rgba(255,255,255,0.10)",
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
                rx.button(
                    rx.icon(
                        "scroll-text",
                        class_name="block md:hidden",
                        size=18,
                    ),
                    rx.text("Changelog", class_name="hidden md:block"),
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
                    rx.icon(
                        "github",
                        class_name="block md:hidden",
                        size=18,
                    ),
                    rx.text("Github", class_name="hidden md:block"),
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
                                rx.icon(
                                    "log-in",
                                    class_name="block md:hidden",
                                    size=18,
                                ),
                                rx.text("Sign In", class_name="hidden md:block"),
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
                                rx.icon(
                                    "log-out",
                                    class_name="block md:hidden",
                                    size=18,
                                ),
                                rx.text("Sign Out", class_name="hidden md:block"),
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
                            "background": "linear-gradient(135deg, rgba(75,85,99,0.7) 0%, rgba(55,65,81,0.7) 50%, rgba(31,41,55,0.7) 100%)",
                            "border": "1px solid rgba(31,41,55,0.7)",
                        },
                        {
                            "background": "linear-gradient(135deg, rgba(107,114,128,0.7) 0%, rgba(75,85,99,0.7) 50%, rgba(55,65,81,0.7) 100%)",
                            "border": "1px solid rgba(55,65,81,0.7)",
                        },
                    ),
                    on_click=State.toggle_theme,
                ),
                class_name="flex gap-3",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4",
    )
