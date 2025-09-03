import reflex as rx
from ark.state import State
import reflex_clerk_api as clerk


def search_bar():
    """Search bar component for filtering chat history"""
    return rx.box(
        rx.input(
            placeholder="Search conversations...",
            class_name="w-full h-14 bg-white/90 border-2 border-black rounded-lg pl-4 pr-4 py-3.5 text-gray-800 placeholder-gray-400 focus:border-gray-300 focus:bg-white focus:ring-0 focus:outline-none transition-all duration-300 backdrop-blur-sm shadow-sm",
            style={
                "background": "white",
                "color": "#111827",
                "outline": "none",
                "& input::placeholder": {
                    "color": "#6b7280",
                },
            },
        ),
        class_name="relative mb-6",
    )


def new_chat_button():
    """New chat button component with improved style and hover effects"""
    return (
        rx.button(
            rx.hstack(
                rx.icon(
                    "plus",
                    class_name="block md:hidden",
                    size=20,
                ),
                rx.text("New Chat", class_name="hidden md:block md:text-xl font-bold"),
                spacing="2",
            ),
            on_click=rx.redirect("/"),
            variant="outline",
            class_name="mr-2 px-4 md:px-6 py-4 md:py-6 bg-black border-2 border-black text-white rounded-lg transition-all duration-200 shadow-sm hover:shadow-lg hover:scale-105 hover:bg-gray-900 hover:border-black hover:text-gray-100 hover:ring-2 hover:ring-gray-400/40 focus:outline-none focus:ring-2 focus:ring-gray-400/60 active:scale-100",
            style={
                "cursor": "pointer",
                "boxShadow": "0 2px 8px 0 rgba(0,0,0,0.08)",
            },
        ),
    )


def chat_history_item(chat):
    """Individual chat history item component"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    chat["title"],
                    class_name="text-gray-900 font-semibold text-lg md:text-xl leading-tight line-clamp-2 md:line-clamp-1",
                    style={
                        "display": "-webkit-box",
                        "WebkitLineClamp": "1",
                        "WebkitBoxOrient": "vertical",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                    },
                ),
                rx.text(
                    chat["updated_at"],
                    class_name="text-gray-600 text-xs md:text-sm mt-1",
                ),
                spacing="1",
                align="start",
                class_name="w-full cursor-pointer",
                on_click=[
                    rx.redirect(f"/chat/{chat['id']}"),
                    State.load_chat_history(chat["id"]),
                ],
            ),
            rx.button(
                rx.icon(
                    "trash-2",
                    size=24,
                ),
                variant="ghost",
                class_name="text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg p-2 transition-all duration-200",
                on_click=State.delete_chat(chat["id"]),
            ),
            spacing="2",
            align="center",
            class_name="w-full",
        ),
        class_name="w-full bg-white/60 hover:bg-gray-100 border-2 border-black rounded-lg p-4 transition-all duration-200 shadow-sm hover:shadow-md",
    )


def empty_state_not_logged_in():
    """Empty state when user is not logged in"""
    return rx.center(
        rx.vstack(
            rx.icon(
                "message-circle",
                size=48,
                class_name="text-gray-400 mb-4",
            ),
            rx.text(
                "Login to see your chat history",
                class_name="text-gray-600 text-lg font-medium",
            ),
            rx.text(
                "Sign in to access your previous conversations",
                class_name="text-gray-500 text-sm text-center",
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
                class_name="text-gray-400 mb-4",
            ),
            rx.text(
                "Nothing to display yet",
                class_name="text-gray-600 text-lg font-medium",
            ),
            rx.text(
                "Start chatting to see your conversation history appear here",
                class_name="text-gray-500 text-sm text-center",
            ),
            rx.button(
                "Start New Chat",
                on_click=rx.redirect("/"),
                class_name="mt-4 px-6 py-3 bg-black hover:bg-gray-900 border-2 border-black text-white hover:text-gray-100 rounded-lg transition-all duration-200",
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
                rx.foreach(State.user_chats, chat_history_item),
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
                class_name="text-2xl md:text-4xl ml-2 font-bold text-black",
                as_="h1",
            ),
            new_chat_button(),
            class_name="flex justify-between items-center w-full mb-4",
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
                    "You have ",
                    State.user_chats.length(),
                    " previous chats",
                    class_name="text-gray-600 text-sm ml-2",
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
