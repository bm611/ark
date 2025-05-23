import reflex as rx


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("zap", size=34),
                rx.text("Ark", class_name="text-4xl"),
                class_name="flex justify-center items-center gap-1",
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Changelog",
                        class_name="bg-purple-300 hover:bg-purple-500 px-4 md:px-6 py-6 md:py-8 rounded-3xl text-black text-lg md:text-xl transition-colors font-[dm] font-bold",
                    ),
                    href="/changelog",
                ),
                rx.button(
                    "Github",
                    class_name="bg-blue-300 hover:bg-blue-500 px-4 md:px-6 py-6 md:py-8 rounded-3xl text-black text-lg md:text-xl transition-colors font-[dm] font-bold",
                ),
                class_name="flex gap-3",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4",
    )
