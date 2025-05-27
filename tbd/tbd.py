import reflex as rx
from tbd.components.nav import navbar
from tbd.components.hero import hero, input_section
from tbd.pages.changelog import changelog
from tbd.pages.chat import chat_nav, chat_messages


@rx.page(route="/", title="Beeb Boop")
def index() -> rx.Component:
    return rx.box(
        navbar(),
        hero(),
        input_section(),
    )


@rx.page(route="/chat", title="Chat")
def chat() -> rx.Component:
    return rx.box(
        chat_nav(),
        chat_messages(),
        input_section(),
        class_name="h-screen flex flex-col",
    )


style = {
    "font_family": "Bouge",
}


app = rx.App(
    style=style,
    stylesheets=["/fonts/fonts.css"],
    theme=rx.theme(
        appearance="light",
    ),
    head_components=[
        rx.el.link(rel="manifest", href="/manifest.json"),
        rx.el.meta(name="theme-color", content="#ffffff"),
    ],
)
