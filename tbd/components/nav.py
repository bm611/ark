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
                rx.button(
                    rx.icon("scroll-text", class_name="block md:hidden", size=20),
                    rx.text("Changelog", class_name="hidden md:block"),
                    class_name="bg-purple-200 hover:bg-purple-300 p-3 rounded-xl md:bg-purple-300 md:hover:bg-purple-500 md:px-6 md:py-8 md:rounded-3xl text-black text-lg md:text-xl transition-colors font-[dm] font-bold flex items-center justify-center",
                    on_click=rx.redirect("/changelog"),
                ),
                rx.button(
                    rx.icon("github", class_name="block md:hidden", size=20),
                    rx.text("Github", class_name="hidden md:block"),
                    class_name="bg-blue-200 hover:bg-blue-300 p-3 rounded-xl md:bg-blue-300 md:hover:bg-blue-500 md:px-6 md:py-8 md:rounded-3xl text-black text-lg md:text-xl transition-colors font-[dm] font-bold flex items-center justify-center",
                ),
                class_name="flex gap-3",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4",
    )
