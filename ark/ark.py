import reflex as rx
from ark.components.navigation.nav import navbar
from ark.components.chat.hero import hero, input_section
from ark.pages.changelog import changelog_entry, changelog_header, load_changelog_data
from ark.pages.chat import chat_nav, chat_messages, chat_input
from ark.state import State
import reflex_clerk_api as clerk
import os
from ark.pages.history import history_nav


@rx.page(route="/", title="Ark - Chat | Search | Learn")
def index() -> rx.Component:
    return rx.box(
        navbar(),
        hero(),
        input_section(),
        class_name=rx.cond(
            State.is_dark_theme,
            "min-h-screen bg-gray-950 text-gray-50 transition-colors duration-300",
            "min-h-screen bg-white text-gray-900 transition-colors duration-300",
        ),
    )


@rx.page(route="/chat/[conversation]", title="Ark - Chat", on_load=State.handle_chat_page_load)
def chat() -> rx.Component:
    return rx.box(
        chat_nav(),
        chat_messages(),
        chat_input(),
        class_name=rx.cond(
            State.is_dark_theme,
            "h-screen flex flex-col bg-gray-950 text-gray-50 transition-colors duration-300",
            "h-screen flex flex-col bg-white text-gray-900 transition-colors duration-300",
        ),
    )


@rx.page(route="/history", title="Ark - History")
def history() -> rx.Component:
    return rx.box(
        history_nav(),
        class_name=rx.cond(
            State.is_dark_theme,
            "min-h-screen bg-gray-950 text-gray-50 transition-colors duration-300",
            "min-h-screen bg-white text-gray-900 transition-colors duration-300",
        ),
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
        class_name=rx.cond(
            State.is_dark_theme,
            "min-h-screen bg-gray-900 text-gray-50 transition-colors duration-300",
            "min-h-screen bg-white text-gray-900 transition-colors duration-300",
        ),
    )


style = {
    "font_family": "styrene",
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
        # for website analytics
        rx.el.script(
            src="https://cloud.umami.is/script.js",
            defer=True,
            custom_attrs={"data-website-id": os.environ.get("UMAMI_WEBSITE_ID", "")},
        ),
    ],
)

# Register authentication change handler
clerk.register_on_auth_change_handler(State.handle_auth_change)

# Wrap the entire app with ClerkProvider
clerk.wrap_app(
    app,
    publishable_key=os.environ["CLERK_PUBLISHABLE_KEY"],
    secret_key=os.environ.get("CLERK_SECRET_KEY"),
    register_user_state=True,
)

# Add sign-in and sign-up pages
clerk.add_sign_in_page(app)
clerk.add_sign_up_page(app)
