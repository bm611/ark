import reflex as rx
from ark.components.nav import navbar
from ark.components.hero import hero, input_section
from ark.pages.changelog import changelog_entry, changelog_header, load_changelog_data
from ark.pages.chat import chat_nav, chat_messages
from ark.state import State, UserState
from ark.components.upload import upload_component
import os
import reflex_clerk_api as clerk


@rx.page(route="/", title="Ark - Chat | Search | Learn")
def index() -> rx.Component:
    return clerk.clerk_provider(
        clerk.clerk_loading(
            rx.spinner(),
        ),
        clerk.clerk_loaded(
            rx.box(
                navbar(),
                hero(),
                input_section(),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "min-h-screen bg-gray-900 text-white transition-colors duration-300",
                    "min-h-screen bg-white text-gray-900 transition-colors duration-300",
                ),
            )
        ),
        publishable_key=os.environ.get("CLERK_PUBLISHABLE_KEY", ""),
        secret_key=os.environ.get("CLERK_SECRET_KEY", ""),
        register_user_state=True,
        user_state=UserState,
    )


@rx.page(route="/chat", title="Ark - Chat")
def chat() -> rx.Component:
    return clerk.clerk_provider(
        clerk.clerk_loading(
            rx.spinner(),
        ),
        clerk.clerk_loaded(
            rx.box(
                chat_nav(),
                chat_messages(),
                input_section(),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "h-screen flex flex-col bg-gray-900 text-white transition-colors duration-300",
                    "h-screen flex flex-col bg-white text-gray-900 transition-colors duration-300",
                ),
            )
        ),
        publishable_key="pk_test_Y29udGVudC1waG9lbml4LTQ3LmNsZXJrLmFjY291bnRzLmRldiQ",
        secret_key=os.environ.get("CLERK_SECRET_KEY", ""),
        register_user_state=True,
        user_state=UserState,
    )


@rx.page(route="/demo", title="demo")
def demo() -> rx.Component:
    return rx.container(
        upload_component(),
    )


@rx.page(route="/changelog", title="Changelog - Ark")
def changelog() -> rx.Component:
    # Load changelog entries from JSON
    changelog_entries = load_changelog_data()

    return clerk.clerk_provider(
        clerk.clerk_loading(
            rx.spinner(),
        ),
        clerk.clerk_loaded(
            rx.box(
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
                    "min-h-screen bg-gray-900 text-white transition-colors duration-300",
                    "min-h-screen bg-white text-gray-900 transition-colors duration-300",
                ),
            )
        ),
        publishable_key="pk_test_Y29udGVudC1waG9lbml4LTQ3LmNsZXJrLmFjY291bnRzLmRldiQ",
        secret_key=os.environ.get("CLERK_SECRET_KEY", ""),
        register_user_state=True,
        user_state=UserState,
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
