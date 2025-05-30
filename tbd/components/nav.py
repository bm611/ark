import reflex as rx


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
                    rx.icon("scroll-text", class_name="block md:hidden", size=18),
                    rx.text("Changelog", class_name="hidden md:block"),
                    class_name="p-2 rounded-xl md:px-6 md:py-8 md:rounded-3xl text-white text-sm md:text-xl transition-all duration-200 font-[dm] font-semibold flex items-center justify-center shadow-[0px_4px_0px_0px_rgba(147,51,234,0.6)] hover:shadow-[0px_2px_0px_0px_rgba(147,51,234,0.6)] hover:translate-y-1 md:shadow-none md:hover:shadow-none md:hover:translate-y-0",
                    style={
                        "background": "linear-gradient(135deg, #a855f7 0%, #9333ea 50%, #7c3aed 100%)",
                        "border": "1px solid #7c3aed",
                    },
                    on_click=rx.redirect("/changelog"),
                ),
                rx.button(
                    rx.icon("github", class_name="block md:hidden", size=18),
                    rx.text("Github", class_name="hidden md:block"),
                    class_name="p-2 rounded-xl md:px-6 md:py-8 md:rounded-3xl text-white text-sm md:text-xl transition-all duration-200 font-[dm] font-semibold flex items-center justify-center shadow-[0px_4px_0px_0px_rgba(59,130,246,0.6)] hover:shadow-[0px_2px_0px_0px_rgba(59,130,246,0.6)] hover:translate-y-1 md:shadow-none md:hover:shadow-none md:hover:translate-y-0",
                    style={
                        "background": "linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #2563eb 100%)",
                        "border": "1px solid #2563eb",
                    },
                    on_click=rx.redirect(
                        "https://github.com/bm611/ark", is_external=True
                    ),
                ),
                class_name="flex gap-3",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4",
    )
