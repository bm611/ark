import reflex as rx
from reflex.experimental import ClientStateVar

ActiveTab = ClientStateVar.create("tab_v2", 0)
TabList = [["GitHub", "github"], ["Twitter", "twitter"], ["YouTube", "youtube"]]


def card_component(title, content):
    return rx.box(
        rx.vstack(
            rx.heading(title, size="6", class_name="text-lg font-bold mb-2 text-white"),
            rx.text(content, class_name="text-gray-300 leading-relaxed"),
            class_name="space-y-4",
        ),
        class_name="bg-gray-800 rounded-lg border border-gray-700 p-6 shadow-md max-w-md mx-auto mt-6",
    )


def tab_v2():
    return rx.box(
        rx.hstack(
            rx.foreach(
                TabList,
                lambda tab, i: rx.button(
                    rx.icon(
                        tag=tab[1],
                        width="20px",
                        height="20px",
                        color=rx.cond(
                            ActiveTab.value == i,
                            rx.color("slate", 12),
                            rx.color("slate", 10),
                        ),
                    ),
                    rx.text(
                        tab[0],
                        color=rx.cond(
                            ActiveTab.value == i,
                            rx.color("slate", 12),
                            rx.color("slate", 10),
                        ),
                    ),
                    on_click=[
                        rx.call_function(ActiveTab.set_value(i)),
                    ],
                    aria_disabled="false",
                    background=rx.cond(
                        ActiveTab.value == i,
                        rx.color("gray", 3),
                        "transparent",
                    ),
                    class_name="flex items-center justify-center whitespace-nowrap py-3 align-middle font-semibold min-w-12 gap-2 text-sm h-10 px-4 cursor-pointer",
                    style={
                        "border_radius": rx.cond(
                            ActiveTab.value == i, "0.375rem", "0.5rem"
                        ),
                        "box_shadow": rx.cond(
                            ActiveTab.value == i,
                            "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                            "none",
                        ),
                    },
                ),
            ),
            class_name="inline-flex min-h-[3rem] items-baseline justify-start rounded-lg p-2",
            style={
                "border": f"1.25px dashed {rx.color('gray', 4)}",
            },
        ),
        rx.cond(
            ActiveTab.value == 0,
            card_component(
                TabList[0][0],
                "Explore repositories, collaborate on code, and manage your projects with the world's leading platform for version control and software development.",
            ),
            rx.cond(
                ActiveTab.value == 1,
                card_component(
                    TabList[1][0],
                    "Stay connected with the latest trends, share your thoughts, and engage with a global community through real-time conversations and updates.",
                ),
                card_component(
                    TabList[2][0],
                    "Discover, watch, and share videos from creators around the world. Learn new skills, stay entertained, and explore endless content possibilities.",
                ),
            ),
        ),
        class_name="flex flex-col items-center justify-center",
    )
