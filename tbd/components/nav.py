import reflex as rx


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("zap", size=34),
                rx.text("Ark", class_name="text-4xl"),
                class_name="flex justify-center items-center gap-1 cursor-pointer",
                on_click=rx.redirect("/"),
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon("scroll-text", class_name="block md:hidden", size=20),
                        rx.text("Changelog", class_name="hidden md:block"),
                        class_name="bg-purple-300 hover:bg-purple-500 px-4 md:px-6 py-6 md:py-8 rounded-3xl text-black text-lg md:text-xl transition-colors font-[dm] font-bold flex items-center justify-center",
                    ),
                    href="/changelog",
                ),
                rx.button(
                    rx.icon("github", class_name="block md:hidden", size=20),
                    rx.text("Github", class_name="hidden md:block"),
                    class_name="bg-blue-300 hover:bg-blue-500 px-4 md:px-6 py-6 md:py-8 rounded-3xl text-black text-lg md:text-xl transition-colors font-[dm] font-bold flex items-center justify-center",
                ),
                class_name="flex gap-3",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4",
    )
