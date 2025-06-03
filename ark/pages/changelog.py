import reflex as rx
import json
import os


def changelog_entry(
    version: str, date: str, changes: list[dict], is_latest: bool = False
):
    """Create a changelog entry with version, date, and changes"""
    return rx.box(
        # Header with date and version badges
        rx.flex(
            # Date - takes remaining space
            rx.text(
                date,
                class_name="text-lg md:text-xl font-medium text-gray-700 flex-1",
            ),
            # Version and Latest badges - always on the right side
            rx.hstack(
                rx.text(
                    f"v{version}",
                    class_name="text-xs md:text-lg font-bold text-black px-2 md:px-4 py-0.5 md:py-2 bg-amber-300 rounded-full border-1 md:border-2 border-black",
                ),
                rx.cond(
                    is_latest,
                    rx.text(
                        "Latest",
                        class_name="text-xs md:text-sm font-medium text-white px-1.5 md:px-3 py-0.5 md:py-1 bg-green-600 rounded-full border-1 md:border-2 border-black",
                    ),
                ),
                direction="row",
                gap="2",
                class_name="items-center",
            ),
            direction="row",
            class_name="items-center justify-between mb-6",
        ),
        # Changes list
        rx.box(
            *[
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.text(
                                change["type"].upper(),
                                class_name=f"text-xs font-bold px-2 py-1 rounded {
                                    'bg-green-200 text-green-800'
                                    if change['type'] == 'added'
                                    else 'bg-blue-200 text-blue-800'
                                    if change['type'] == 'improved'
                                    else 'bg-orange-200 text-orange-800'
                                    if change['type'] == 'fixed'
                                    else 'bg-red-200 text-red-800'
                                    if change['type'] == 'removed'
                                    else 'bg-purple-200 text-purple-800'
                                }",
                            ),
                            class_name="flex-shrink-0 w-24 text-center",
                        ),
                        rx.text(
                            change["description"],
                            class_name="font-[dm] text-sm md:text-lg text-black font-medium leading-relaxed",
                        ),
                        align="start",
                        class_name="w-full flex",
                    ),
                )
                for change in changes
            ],
            class_name="space-y-2",
        ),
        class_name="bg-white rounded-xl p-4 md:p-8 border-2 md:border-3 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] md:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] mb-4 md:mb-6",
    )


def changelog_header():
    """Header section for the changelog page"""
    return rx.box(
        rx.flex(
            rx.heading(
                "Changelog",
                class_name="text-4xl md:text-7xl font-bold text-black tracking-wider mb-4",
                as_="h1",
            ),
            rx.text(
                "Keep track of all the exciting features and improvements shipped",
                class_name="font-[dm] text-base md:text-2xl text-gray-700 font-medium max-w-3xl text-center leading-relaxed px-4",
            ),
            direction="column",
            align="center",
            class_name="text-center",
        ),
        class_name="py-8 md:py-20",
    )


def load_changelog_data():
    """Load changelog data from JSON file"""
    try:
        # Get the path to the changelog.json file
        data_file = os.path.join(os.path.dirname(__file__), "..", "data", "changelog.json")

        with open(data_file, "r") as f:
            data = json.load(f)
        return data.get("entries", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading changelog data: {e}")
        return []
