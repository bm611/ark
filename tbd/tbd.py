import reflex as rx
from tbd.components.nav import navbar
from tbd.components.hero import hero, input_section
from tbd.pages.changelog import changelog


@rx.page(route="/", title="Beeb Boop")
def index() -> rx.Component:
    return rx.box(
        navbar(),
        hero(),
        input_section(),
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
    head_components=[
        rx.el.link(rel="manifest", href="/manifest.json"),
        rx.el.meta(name="theme-color", content="#ffffff"),
    ],
)
