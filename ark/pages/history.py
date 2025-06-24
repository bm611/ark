import reflex as rx
from ark.state import State
import reflex_clerk_api as clerk


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
                "background": rx.cond(State.is_dark_theme, "#1f2937", "white"),
                "color": rx.cond(State.is_dark_theme, "white", "#111827"),
                "outline": "none",
                "& input::placeholder": {
                    "color": rx.cond(State.is_dark_theme, "#a3a3a3", "#6b7280"),
                },
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


def chat_history_item(chat):
    """Individual chat history item component"""
    return rx.box(
        rx.vstack(
            rx.text(
                chat["title"],
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-200 font-medium text-sm md:text-md leading-tight",
                    "text-gray-900 font-medium text-sm md:text-md leading-tight",
                ),
                style={
                    "display": "-webkit-box",
                    "webkitLineClamp": "1",
                    "webkitBoxOrient": "vertical",
                    "overflow": "hidden",
                },
            ),
            rx.text(
                f"Last updated {chat['updated_at']}",
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-400 text-xs md:text-sm mt-1",
                    "text-gray-600 text-xs md:text-sm mt-1",
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
        on_click=[
            State.load_chat_history(chat["id"]),
            rx.redirect(f"/chat/{chat['id']}"),
        ],
    )


def empty_state_not_logged_in():
    """Empty state when user is not logged in"""
    return rx.center(
        rx.vstack(
            rx.icon(
                "message-circle",
                size=48,
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-500 mb-4",
                    "text-gray-400 mb-4",
                ),
            ),
            rx.text(
                "Login to see your chat history",
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-400 text-lg font-medium",
                    "text-gray-600 text-lg font-medium",
                ),
            ),
            rx.text(
                "Sign in to access your previous conversations",
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-500 text-sm text-center",
                    "text-gray-500 text-sm text-center",
                ),
            ),
            spacing="2",
            align="center",
            class_name="py-16",
        ),
        class_name="w-full",
    )


def empty_state_no_chats():
    """Empty state when user is logged in but has no chats"""
    return rx.center(
        rx.vstack(
            rx.icon(
                "message-circle-off",
                size=48,
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-500 mb-4",
                    "text-gray-400 mb-4",
                ),
            ),
            rx.text(
                "Nothing to display yet",
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-400 text-lg font-medium",
                    "text-gray-600 text-lg font-medium",
                ),
            ),
            rx.text(
                "Start chatting to see your conversation history appear here",
                class_name=rx.cond(
                    State.is_dark_theme,
                    "text-neutral-500 text-sm text-center",
                    "text-gray-500 text-sm text-center",
                ),
            ),
            rx.button(
                "Start New Chat",
                on_click=rx.redirect("/"),
                class_name=rx.cond(
                    State.is_dark_theme,
                    "mt-4 px-6 py-3 bg-neutral-700 hover:bg-neutral-600 border-neutral-600 hover:border-neutral-500 text-neutral-200 hover:text-neutral-100 rounded-lg transition-all duration-200",
                    "mt-4 px-6 py-3 bg-black hover:bg-gray-900 border-gray-900 hover:border-black text-white hover:text-gray-100 rounded-lg transition-all duration-200",
                ),
            ),
            spacing="2",
            align="center",
            class_name="py-16",
        ),
        class_name="w-full",
    )


def chat_history_list():
    """List of chat history items"""
    return rx.cond(
        clerk.ClerkState.is_signed_in,
        # User is logged in - show chats or empty state
        rx.cond(
            State.user_chats,
            # User has chats
            rx.vstack(
                rx.foreach(
                    State.user_chats,
                    chat_history_item
                ),
                spacing="3",
                class_name="w-full",
            ),
            # User has no chats
            empty_state_no_chats(),
        ),
        # User is not logged in
        empty_state_not_logged_in(),
    )


def history_header():
    """Header section with title and new chat button"""
    return rx.box(
        rx.flex(
            rx.heading(
                "Chats",
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
    return rx.cond(
        clerk.ClerkState.is_signed_in,
        rx.cond(
            State.user_chats,
            rx.hstack(
                rx.text(
                    "You have ", State.user_chats.length(), " previous chats",
                    class_name=rx.cond(
                        State.is_dark_theme,
                        "text-neutral-400 text-sm ml-2",
                        "text-gray-600 text-sm ml-2",
                    ),
                ),
                spacing="0",
                class_name="mb-6 max-w-4xl mx-auto",
            ),
            rx.fragment(),
        ),
        rx.fragment(),
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
        on_mount=State.load_user_chats,
    )
