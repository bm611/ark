import reflex as rx
from ark.state import State


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("zap", size=24, class_name="md:h-8 md:w-8"),
                rx.text("Ark", class_name="text-3xl md:text-4xl"),
                class_name="flex justify-center items-center gap-1 cursor-pointer",
                on_click=rx.redirect("/"),
            ),
            rx.hstack(
                rx.button(
                    rx.icon(
                        "scroll-text",
                        class_name="block md:hidden",
                        size=18,
                    ),
                    rx.text("Changelog", class_name="hidden md:block"),
                    class_name="p-2 rounded-xl md:px-6 md:py-8 md:rounded-3xl text-white text-sm md:text-xl transition-all duration-200 font-[dm] font-semibold flex items-center justify-center shadow-[0px_4px_0px_0px_rgb(147,51,234,0.6)] active:shadow-[0px_2px_0px_0px_rgb(147,51,234,0.6)] active:translate-y-1 md:shadow-[0px_4px_0px_0px_rgb(147,51,234,0.6)] md:hover:shadow-[0px_6px_0px_0px_rgb(147,51,234,0.8)] md:hover:brightness-110 md:active:shadow-[0px_2px_0px_0px_rgb(147,51,234,0.6)] md:active:translate-y-1",
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
                    class_name="p-2 rounded-xl md:px-6 md:py-8 md:rounded-3xl text-white text-sm md:text-xl transition-all duration-200 font-[dm] font-semibold flex items-center justify-center shadow-[0px_4px_0px_0px_rgb(59,130,246,0.6)] active:shadow-[0px_2px_0px_0px_rgb(59,130,246,0.6)] active:translate-y-1 md:shadow-[0px_4px_0px_0px_rgb(59,130,246,0.6)] md:hover:shadow-[0px_6px_0px_0px_rgb(59,130,246,0.8)] md:hover:brightness-110 md:active:shadow-[0px_2px_0px_0px_rgb(59,130,246,0.6)] md:active:translate-y-1",
                    style={
                        "background": "linear-gradient(135deg, rgba(96,165,250,0.7) 0%, rgba(59,130,246,0.7) 50%, rgba(37,99,235,0.7) 100%)",
                        "border": "1px solid rgba(37,99,235,0.7)",
                    },
                    on_click=rx.redirect(
                        "https://github.com/bm611/ark", is_external=True
                    ),
                ),
                rx.button(
                    rx.cond(
                        State.is_dark_theme,
                        rx.icon("sun", size=18, class_name="text-white"),
                        rx.icon("moon", size=18, class_name="text-white"),
                    ),
                    # rx.text("Theme", class_name="hidden md:block text-white font-semibold"),
                    class_name="p-2 rounded-xl md:px-6 md:py-8 md:rounded-3xl text-white text-sm md:text-xl transition-all duration-200 font-[dm] font-semibold flex items-center justify-center gap-2 shadow-[0px_4px_0px_0px_rgb(75,85,99,0.6)] active:shadow-[0px_2px_0px_0px_rgb(75,85,99,0.6)] active:translate-y-1 md:shadow-[0px_4px_0px_0px_rgb(75,85,99,0.6)] md:hover:shadow-[0px_6px_0px_0px_rgb(75,85,99,0.8)] md:hover:brightness-110 md:active:shadow-[0px_2px_0px_0px_rgb(75,85,99,0.6)] md:active:translate-y-1",
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
