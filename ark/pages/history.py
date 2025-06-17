import reflex as rx
from ark.state import State


def search_bar():
    """Search bar component for filtering chat history"""
    return rx.box(
        rx.input(
            placeholder="Search conversations...",
            class_name=rx.cond(
                State.is_dark_theme,
                "w-full h-14 bg-neutral-900/70 border border-neutral-700/60 rounded-2xl pl-4 pr-4 py-3.5 text-neutral-100 placeholder-neutral-500 focus:border-neutral-600 focus:bg-neutral-900/90 focus:ring-0 focus:outline-none transition-all duration-300 backdrop-blur-sm",
                "w-full h-14 bg-white/90 border border-gray-200/80 rounded-2xl pl-4 pr-4 py-3.5 text-gray-800 placeholder-gray-400 focus:border-gray-300 focus:bg-white focus:ring-0 focus:outline-none transition-all duration-300 backdrop-blur-sm shadow-sm",
            ),
            style={
                "fontSize": "15px",
                "fontWeight": "500",
                "boxShadow": rx.cond(
                    State.is_dark_theme,
                    "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                    "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                ),
            },
        ),
        class_name="relative mb-6",
    )


def new_chat_button():
    """New chat button component"""
    return (
        rx.button(
            rx.icon(
                "plus",
                class_name="block md:hidden",
                size=20,
            ),
            rx.text("New Chat", class_name="hidden md:block"),
            on_click=rx.redirect("/"),
            variant="outline",
            class_name=rx.cond(
                State.is_dark_theme,
                "mr-2 px-4 md:px-6 py-4 md:py-6 bg-neutral-800 hover:bg-neutral-700 border-neutral-600 hover:border-neutral-500 text-neutral-200 hover:text-neutral-100 rounded-xl transition-all duration-200 backdrop-blur-sm",
                "mr-2 px-4 md:px-6 py-4 md:py-6 bg-black hover:bg-gray-900 border-gray-900 hover:border-black text-white hover:text-gray-100 rounded-xl transition-all duration-200 backdrop-blur-sm shadow-sm hover:shadow-md",
            ),
        ),
    )


def chat_history_item(title: str, last_message: str, timestamp: str):
    """Individual chat history item component"""
    return rx.box(
        rx.vstack(
            rx.text(
                title,
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-200 font-medium text-md leading-tight",
                    "text-gray-900 font-medium text-md leading-tight",
                ),
                style={
                    "display": "-webkit-box",
                    "webkitLineClamp": "1",
                    "webkitBoxOrient": "vertical",
                    "overflow": "hidden",
                },
            ),
            rx.text(
                last_message,
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-400 text-sm mt-1",
                    "text-gray-600 text-sm mt-1",
                ),
            ),
            spacing="1",
            align="start",
            class_name="w-full",
        ),
        class_name=rx.cond(
            State.is_dark_theme,
            "w-full bg-neutral-800/30 hover:bg-neutral-800/50 border border-neutral-700/50 hover:border-neutral-600/70 rounded-xl p-4 cursor-pointer transition-all duration-200 backdrop-blur-sm",
            "w-full bg-white/60 hover:bg-white/80 border border-gray-200/60 hover:border-gray-300/80 rounded-xl p-4 cursor-pointer transition-all duration-200 backdrop-blur-sm shadow-sm hover:shadow-md",
        ),
        on_click=rx.redirect("/chat"),
    )


def chat_history_list():
    """List of chat history items"""
    # Mock data - replace with actual state data later
    chat_items = [
        {
            "title": "Removing Active Tab Light Effect in Reflex",
            "last_message": "Last message 2 hours ago",
            "timestamp": "2 hours ago",
        },
        {
            "title": "Kinde Auth Google Social Login Setup",
            "last_message": "Last message 2 days ago",
            "timestamp": "2 days ago",
        },
        {
            "title": "Google Auth Setup for Reflex",
            "last_message": "Last message 2 days ago",
            "timestamp": "2 days ago",
        },
        {
            "title": "Google Sign-In for Reflex App",
            "last_message": "Last message 2 days ago",
            "timestamp": "2 days ago",
        },
        {
            "title": "Reflex Python Authentication Setup",
            "last_message": "Last message 2 days ago",
            "timestamp": "2 days ago",
        },
        {
            "title": "Clerk Auth DNS Configuration Issue",
            "last_message": "Last message 2 days ago",
            "timestamp": "2 days ago",
        },
        {
            "title": "Umami Analytics Tracking in Reflex",
            "last_message": "Last message 3 days ago",
            "timestamp": "3 days ago",
        },
        {
            "title": "Self-Hosting Plausible Analytics",
            "last_message": "Last message 3 days ago",
            "timestamp": "3 days ago",
        },
    ]

    return rx.vstack(
        *[
            chat_history_item(
                title=item["title"],
                last_message=item["last_message"],
                timestamp=item["timestamp"],
            )
            for item in chat_items
        ],
        spacing="3",
        class_name="w-full",
    )


def history_header():
    """Header section with title and new chat button"""
    return rx.box(
        rx.flex(
            rx.heading(
                "Chat History",
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-2xl md:text-4xl ml-2 font-bold text-neutral-200",
                    "text-2xl md:text-4xl ml-2 font-bold text-gray-600",
                ),
                as_="h1",
            ),
            new_chat_button(),
            align="center",
            justify="between",
            class_name="w-full mb-4",
        ),
        class_name="w-full max-w-4xl mx-auto",
    )


def chat_count_info():
    """Information about number of previous chats"""
    return rx.hstack(
        rx.text(
            "You have 450 previous chats with Claude ",
            class_name=rx.cond(
                State.is_dark_theme,
                "text-neutral-400 text-sm",
                "text-gray-600 text-sm",
            ),
        ),
        spacing="0",
        class_name="mb-6 max-w-4xl mx-auto",
    )


def history_nav():
    """Main history navigation component"""
    return rx.box(
        rx.box(
            history_header(),
            search_bar(),
            chat_count_info(),
            chat_history_list(),
            class_name="w-full max-w-4xl mx-auto px-4 py-6 md:py-8",
        ),
        class_name="min-h-screen pt-4 md:pt-8",
    )
