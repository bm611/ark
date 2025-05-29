import reflex as rx
from tbd.components.nav import navbar
from tbd.components.hero import hero, input_section
from tbd.pages.changelog import changelog_entry, changelog_header, load_changelog_data
from tbd.pages.chat import chat_nav, chat_messages, model_provider


@rx.page(route="/", title="Ark - Chat | Search | Learn")
def index() -> rx.Component:
    return rx.box(
        navbar(),
        hero(),
        input_section(),
    )


@rx.page(route="/chat", title="Ark - Chat")
def chat() -> rx.Component:
    return rx.box(
        chat_nav(),
        model_provider(),
        chat_messages(),
        input_section(),
        class_name="h-screen flex flex-col",
    )


@rx.page(route="/changelog", title="Changelog - Ark")
def changelog() -> rx.Component:
    # Load changelog entries from JSON
    changelog_entries = load_changelog_data()

    return rx.box(
        navbar(),
        # Header section
        changelog_header(),
        # Changelog entries
        rx.box(
            *[
                changelog_entry(
                    version=entry["version"],
                    date=entry["date"],
                    is_latest=entry.get("is_latest", False),
                    changes=entry["changes"],
                )
                for entry in changelog_entries
            ],
            class_name="max-w-4xl mx-auto px-4 pb-16 md:pb-20",
        ),
        class_name="min-h-screen",
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
