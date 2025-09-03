import reflex as rx
from ark.state import State
from ark.components.common.buttons import action_button
import reflex_clerk_api as clerk


def input_section():
    return (
        rx.box(
            rx.vstack(
                rx.cond(
                    (State.img.length() > 0)
                    | (State.pdf_files.length() > 0)
                    | (State.uploaded_files.length() > 0),
                    rx.box(
                        rx.hstack(
                            # R2 uploaded files (preferred)
                            rx.foreach(
                                State.uploaded_files,
                                lambda file_ref: rx.box(
                                    rx.hstack(
                                        rx.icon(
                                            rx.cond(
                                                file_ref["type"] == "image",
                                                "image",
                                                "file-text",
                                            ),
                                            size=18,
                                            color="#000000",
                                        ),
                                        rx.text(
                                            file_ref.get(
                                                "original_filename", "Unknown file"
                                            ),
                                            class_name="text-sm text-black font-medium",
                                        ),
                                        align="center",
                                        spacing="2",
                                    ),
                                    class_name="bg-white border-2 border-black rounded-lg px-4 py-3 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]",
                                ),
                            ),
                            # Legacy image files (fallback)
                            rx.foreach(
                                State.img,
                                lambda filename: rx.box(
                                    rx.hstack(
                                        rx.icon(
                                            "image",
                                            size=18,
                                            color="#3b82f6",
                                        ),
                                        rx.text(
                                            filename,
                                            class_name="text-sm text-black font-medium",
                                        ),
                                        rx.button(
                                            rx.icon("x", size=14),
                                            variant="ghost",
                                            class_name="ml-2 p-1 rounded-full hover:bg-gray-200/50 text-gray-500 hover:text-gray-700 border-0 bg-transparent",
                                            on_click=State.clear_images,
                                        ),
                                        align="center",
                                        spacing="2",
                                    ),
                                    class_name="bg-white/90 border border-gray-300/60 rounded-xl px-4 py-3 backdrop-blur-sm shadow-lg",
                                ),
                            ),
                            # Legacy PDF files (fallback)
                            rx.foreach(
                                State.pdf_files,
                                lambda filename: rx.box(
                                    rx.hstack(
                                        rx.icon(
                                            "file-text",
                                            size=18,
                                            color="#dc2626",
                                        ),
                                        rx.text(
                                            filename,
                                            class_name="text-sm text-black font-medium",
                                        ),
                                        rx.button(
                                            rx.icon("x", size=14),
                                            variant="ghost",
                                            class_name="ml-2 p-1 rounded-full hover:bg-gray-200/50 text-gray-500 hover:text-gray-700 border-0 bg-transparent",
                                            on_click=State.clear_pdfs,
                                        ),
                                        align="center",
                                        spacing="2",
                                    ),
                                    class_name="bg-white/90 border border-gray-300/60 rounded-xl px-4 py-3 backdrop-blur-sm shadow-lg",
                                ),
                            ),
                            wrap="wrap",
                            spacing="3",
                        ),
                        class_name="mb-1 w-full max-w-4xl mx-auto",
                    ),
                ),
                rx.box(
                    rx.text_area(
                        value=State.prompt,
                        class_name=(
                            "w-full mx-auto text-black text-base sm:text-lg "
                            "min-h-28 sm:min-h-32 max-h-40 sm:max-h-48 "
                            "px-4 sm:px-6 py-4 sm:py-6 pb-12 sm:pb-16 "
                            "resize-none outline-none focus:outline-none "
                            "border-4 border-black bg-yellow-200 "
                            "shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] "
                            "focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                            "focus:translate-x-1 focus:translate-y-1 "
                            "transition-all duration-100 font-bold"
                        ),
                        placeholder="ASK ANYTHING...",
                        style={
                            "background": "#FDE68A",
                            "color": "#000000",
                            "outline": "none",
                            "& textarea::placeholder": {
                                "color": "#374151",
                                "font-weight": "900",
                                "text-transform": "uppercase",
                            },
                        },
                        on_change=State.set_prompt.debounce(500),
                        size="3",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.cond(
                                State.current_url == "/",
                                rx.hstack(
                                    rx.upload(
                                        action_button(
                                            label="",
                                            icon="paperclip",
                                            active_gradient="linear-gradient(135deg, #60a5fa 0%, #2563eb 50%, #1e40af 100%)",
                                            active_border="#1e40af",
                                            shadow_color="rgba(59,130,246,0.8)",
                                        ),
                                        style={},
                                        class_name="",
                                        border=None,
                                        padding=None,
                                        accept={
                                            "image/png": [".png"],
                                            "image/jpeg": [".jpg", ".jpeg"],
                                            "application/pdf": [".pdf"],
                                        },
                                        on_drop=State.handle_upload(
                                            rx.upload_files(upload_id="upload")
                                        ),
                                        id="upload",
                                    ),
                                    action_button(
                                        label="Search",
                                        icon="globe",
                                        is_active=State.selected_action == "Search",
                                        active_gradient="linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%)",
                                        active_border="#166534",
                                        shadow_color="rgba(34,197,94,0.8)",
                                        on_click=State.handle_search_click,
                                    ),
                                    action_button(
                                        label="Think",
                                        icon="lightbulb",
                                        is_active=State.selected_action == "Think",
                                        active_gradient="linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%)",
                                        active_border="#92400e",
                                        shadow_color="rgba(245,158,11,0.8)",
                                        on_click=State.handle_think_click,
                                    ),
                                    class_name="gap-0 mb-2",
                                ),
                            ),
                            rx.button(
                                rx.hstack(
                                    rx.icon(
                                        "arrow-up",
                                        size=20,
                                        color="black",
                                        class_name="sm:hidden w-5 h-5",
                                    ),
                                    rx.text(
                                        "SEND",
                                        class_name="hidden sm:block text-base font-black text-black ml-2 uppercase tracking-wider",
                                    ),
                                    class_name="flex items-center justify-center",
                                ),
                                class_name=(
                                    "ml-auto bg-red-400 border-4 border-black h-10 sm:h-12 w-10 sm:w-auto sm:px-4 "
                                    "shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] "
                                    "hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] "
                                    "hover:translate-x-1 hover:translate-y-1 "
                                    "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                    "active:translate-x-2 active:translate-y-2 "
                                    "transition-all duration-100 flex items-center justify-center mb-2"
                                ),
                                style={
                                    "background": "#F87171",
                                    "border": "4px solid #000000",
                                },
                                on_click=[
                                    State.handle_generation,
                                    State.generate_chat_id_and_redirect,
                                ],
                                loading=State.is_gen,
                                disabled=State.is_gen,
                            ),
                            align="center",
                            class_name="w-full",
                        ),
                        class_name="absolute bottom-2 left-2 right-2 px-2",
                    ),
                    class_name="relative w-full max-w-4xl mx-auto",
                ),
                class_name="w-full mx-auto max-w-4xl",
            ),
            class_name="fixed bottom-2 md:bottom-6 left-0 right-0 p-4 bg-white",
        ),
    )


def hero():
    return (
        rx.box(
            rx.flex(
                rx.box(
                    rx.box(
                        clerk.signed_in(
                            rx.box(
                                rx.heading(
                                    rx.cond(
                                        State.logged_user_name == "",
                                        "WELCOME BACK!",
                                        "WELCOME BACK, " + State.logged_user_name.upper() + "!",
                                    ),
                                    class_name="text-3xl md:text-6xl font-black mb-4 tracking-tight text-black uppercase px-6 py-3 bg-yellow-400 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] inline-block transform -rotate-1",
                                    as_="h1",
                                )
                            )
                        ),
                        clerk.signed_out(
                            rx.box(
                                rx.heading(
                                    "WELCOME TO ARK!",
                                    class_name="text-3xl md:text-6xl font-black mb-4 tracking-tight text-black uppercase px-6 py-3 bg-yellow-400 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] inline-block transform -rotate-1",
                                    as_="h1",
                                )
                            )
                        ),
                        rx.box(
                            rx.heading(
                                "YOUR AI CHAT COMPANION",
                                class_name="text-lg md:text-3xl font-black mb-4 tracking-tight text-white uppercase px-4 py-2 bg-black border-4 border-black inline-block transform rotate-1",
                                as_="h2",
                            )
                        ),
                        rx.box(
                            rx.text(
                                "CHAT • SEARCH • LEARN—SMARTER, FASTER, ANYWHERE",
                                class_name="hidden sm:block text-sm sm:text-base md:text-xl mb-6 text-black font-black uppercase tracking-wide px-4 py-2 bg-pink-400 border-4 border-black inline-block",
                            )
                        ),
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.text(
                                        "TRY THESE EXAMPLES:",
                                        class_name="text-base sm:text-lg font-black text-black uppercase tracking-wider mb-3 px-3 py-2 bg-white border-4 border-black inline-block shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]",
                                    )
                                ),
                                rx.flex(
                                    rx.button(
                                        rx.vstack(
                                            rx.box(
                                                rx.icon(
                                                    "message-circle",
                                                    size=20,
                                                    color="black",
                                                ),
                                                class_name="mb-2",
                                            ),
                                            rx.text(
                                                "PYTHON TIPS",
                                                class_name="font-black text-center leading-tight text-black uppercase tracking-wide text-xs",
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        class_name=(
                                            "bg-blue-300 border-4 border-black px-4 py-3 "
                                            "shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] "
                                            "hover:shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] "
                                            "hover:translate-x-1 hover:translate-y-1 "
                                            "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                            "active:translate-x-2 active:translate-y-2 "
                                            "transition-all duration-100 min-h-[100px] min-w-[140px]"
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "Give me some Python programming tips with code examples."
                                            ),
                                            State.handle_generation,
                                            State.generate_chat_id_and_redirect,
                                        ],
                                    ),
                                    rx.button(
                                        rx.vstack(
                                            rx.box(
                                                rx.icon(
                                                    "globe",
                                                    size=20,
                                                    color="black",
                                                ),
                                                class_name="mb-2",
                                            ),
                                            rx.text(
                                                "LATEST NEWS",
                                                class_name="font-black text-center leading-tight text-black uppercase tracking-wide text-xs",
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        class_name=(
                                            "bg-green-300 border-4 border-black px-4 py-3 "
                                            "shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] "
                                            "hover:shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] "
                                            "hover:translate-x-1 hover:translate-y-1 "
                                            "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                            "active:translate-x-2 active:translate-y-2 "
                                            "transition-all duration-100 min-h-[100px] min-w-[140px]"
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "What's the latest news in US, World, Technology & Science?"
                                            ),
                                            State.handle_search_click,
                                            State.handle_generation,
                                            State.generate_chat_id_and_redirect,
                                        ],
                                    ),
                                    rx.button(
                                        rx.vstack(
                                            rx.box(
                                                rx.icon(
                                                    "book-open",
                                                    size=20,
                                                    color="black",
                                                ),
                                                class_name="mb-2",
                                            ),
                                            rx.text(
                                                "QUANTUM COMPUTING",
                                                class_name="font-black text-center leading-tight text-black uppercase tracking-wide text-xs",
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        class_name=(
                                            "bg-purple-300 border-4 border-black px-4 py-3 "
                                            "shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] "
                                            "hover:shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] "
                                            "hover:translate-x-1 hover:translate-y-1 "
                                            "active:shadow-[0px_0px_0px_0px_rgba(0,0,0,1)] "
                                            "active:translate-x-2 active:translate-y-2 "
                                            "transition-all duration-100 min-h-[100px] min-w-[140px]"
                                        ),
                                        on_click=[
                                            State.set_prompt(
                                                "Explain quantum computing"
                                            ),
                                            State.handle_generation,
                                            State.generate_chat_id_and_redirect,
                                        ],
                                    ),
                                    wrap="wrap",
                                    spacing="3",
                                    justify="center",
                                    class_name="gap-3 sm:gap-4 max-w-3xl mx-auto px-3 sm:px-4",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            class_name="mb-6 sm:mb-8",
                        ),
                        class_name="text-center relative",
                    ),
                ),
                direction="column",
                align="center",
                justify="center",
            ),
            rx.html(
                """
                <style>
                .example-prompt-card {
                    min-height: 120px;
                    min-width: 180px;
                    max-width: 200px;
                    flex: 1;
                    backdrop-filter: blur(10px);
                }

                @media (max-width: 640px) {
                    .example-prompt-card {
                        min-width: 140px;
                        max-width: 150px;
                        min-height: 85px;
                        font-size: 0.75rem;
                    }
                }

                @media (min-width: 641px) and (max-width: 768px) {
                    .example-prompt-card {
                        min-width: 160px;
                        max-width: 170px;
                        min-height: 95px;
                    }
                }

                .example-prompt-card:active {
                    transform: scale(0.98);
                }
                </style>
                """
            ),
            class_name="flex items-center justify-center min-h-[70vh] pb-4 pt-8 md:pt-0 relative overflow-hidden bg-white",
        ),
    )
