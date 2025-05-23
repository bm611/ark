import reflex as rx
from tbd.components.nav import navbar
from tbd.components.hero import hero


@rx.page(route="/", title="Beeb Boop")
def index() -> rx.Component:
    return rx.box(
        navbar(),
        hero(),
        rx.box(
            rx.hstack(
                rx.input(
                    # value=State.habit,
                    class_name="w-full font-[dm] mt-4 mx-auto text-black text-lg md:text-2xl bg-white rounded-2xl h-16 shadow-inner border-2 border-gray-600",
                    # on_change=State.set_habit,
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("arrow-up", size=28, color="white"),
                        class_name="flex items-center justify-center",
                    ),
                    class_name="mt-4 mx-auto text-black bg-black rounded-2xl h-16 px-4 md:px-8",
                    # on_click=State.handle_submit,
                ),
                class_name="w-full flex gap-1 items-center justify-center max-w-4xl mx-auto",
            ),
            class_name="fixed bottom-2 md:bottom-6 left-0 right-0 p-2 md:p-4 bg-[#edede9]",
        ),
    )


style = {
    "font_family": "Bouge",
    "background_color": "#edede9",
}


app = rx.App(
    style=style,
    stylesheets=["/fonts/fonts.css"],
    theme=rx.theme(
        appearance="light",
    ),
)
