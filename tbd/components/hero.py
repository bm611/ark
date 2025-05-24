import reflex as rx


def input_section():
    return (
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


def card(
    title: str,
    description: str,
    image_src: str,
    background_color: str = "bg-blue-300",
):
    return rx.box(
        # Mobile: horizontal layout, Desktop: vertical layout
        rx.flex(
            # Image container
            rx.box(
                rx.image(
                    src=image_src,
                    class_name="w-24 md:w-32 h-24 md:h-32 object-contain",
                ),
                class_name="flex-shrink-0 mr-4 md:mr-0 md:mb-6",
            ),
            # Content container
            rx.box(
                # Title
                rx.heading(
                    title,
                    class_name="text-2xl md:text-4xl font-bold mb-2 md:mb-4 tracking-wider text-black text-left",
                    as_="h2",
                ),
                # Description
                rx.text(
                    description,
                    class_name="font-[dm] text-sm md:text-xl text-black font-medium text-left leading-relaxed",
                ),
                class_name="flex-1",
            ),
            direction="row",
            class_name="md:flex-col",
            align="start",
        ),
        class_name=f"{background_color} rounded-xl p-4 md:p-8 h-full flex flex-col border-3 border-black transform transition-all duration-300 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] md:hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 hover:-translate-x-1",
    )


def hero():
    return (
        rx.box(
            rx.flex(
                rx.box(
                    rx.heading(
                        "Ask Anything",
                        class_name="text-4xl md:text-6xl font-bold mb-8 md:mb-12 tracking-wide text-black",
                        as_="h1",
                    ),
                    rx.flex(
                        card(
                            title="Chat",
                            description="Engage in intelligent conversations powered by advanced AI technology.",
                            image_src="/go_pop.png",
                            background_color="bg-amber-300",
                        ),
                        card(
                            title="Search",
                            description="Find accurate information quickly with AI-powered search capabilities.",
                            image_src="/g_search.png",
                            background_color="bg-sky-300",
                        ),
                        card(
                            title="Learn",
                            description="Expand your knowledge with personalized learning experiences.",
                            image_src="/g_learn.png",
                            background_color="bg-purple-300",
                        ),
                        class_name="flex flex-col md:grid md:grid-cols-3 gap-6 md:gap-6 max-w-lg md:max-w-6xl mx-auto px-4",
                    ),
                    class_name="text-center",
                ),
                direction="column",
                align="center",
                justify="center",
            ),
            class_name="flex items-center justify-center min-h-[70vh] pb-4",
        ),
    )
