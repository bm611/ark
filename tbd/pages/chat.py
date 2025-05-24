import reflex as rx


class ChatState(rx.State):
    messages: list[dict[str, str]] = [
        {"role": "user", "content": "What's the weather like today?"},
        {
            "role": "assistant",
            "content": "I don't have access to real-time weather data, but I can help you find weather information! You can check your local weather by:\n\n1. Looking at a weather app on your phone\n2. Visiting websites like Weather.com or AccuWeather\n3. Asking a voice assistant like Siri or Google Assistant\n\nIs there anything else I can help you with?",
        },
        {
            "role": "user",
            "content": "Can you explain machine learning in simple terms?",
        },
        {
            "role": "assistant",
            "content": "Sure! Machine learning is like teaching a computer to recognize patterns and make decisions, similar to how humans learn from experience.\n\nImagine you're teaching a child to recognize cats:\n- You show them many pictures of cats\n- They start noticing patterns (pointy ears, whiskers, etc.)\n- Eventually, they can identify cats in new pictures\n\nMachine learning works similarly:\n1. **Training**: Feed the computer lots of data\n2. **Learning**: It finds patterns in that data\n3. **Predicting**: It uses those patterns to make decisions about new, unseen data\n\nCommon examples include email spam detection, recommendation systems (like Netflix suggestions), and voice assistants!",
        },
    ]


def chat_nav():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("zap", size=34),
                rx.text("Ark", class_name="text-4xl"),
                class_name="flex justify-center items-center gap-1 cursor-pointer",
                on_click=rx.redirect("/"),
            ),
            rx.button(
                rx.text("New Chat"),
                class_name="bg-blue-300 hover:bg-blue-500 px-4 md:px-6 py-6 md:py-8 rounded-3xl text-black text-lg md:text-xl transition-colors font-[dm] font-bold flex items-center justify-center",
            ),
            class_name="flex justify-between items-center",
        ),
        class_name="p-4",
    )


def response_message(message: dict) -> rx.Component:
    return rx.box(
        rx.cond(
            message["role"] == "user",
            rx.text(message["content"], class_name="text-xl md:text-4xl"),
            rx.box(
                rx.markdown(
                    message["content"],
                    class_name="font-[dm] text-sm md:text-xl",
                ),
                class_name="bg-white border-2 border-black rounded-3xl p-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] mb-20",
            ),
        ),
        class_name="",
    )


def chat_messages():
    return rx.box(
        rx.foreach(
            ChatState.messages,
            response_message,
        ),
        class_name="flex-1 overflow-y-scroll p-4 md:p-6 space-y-4 max-w-4xl mx-auto w-full pb-24 md:pb-32 hide-scrollbar",
    )
