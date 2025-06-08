import reflex as rx
from ark.state import State


def get_weather_icon(weather_main: str, is_sunny: bool) -> str:
    """Get the appropriate weather icon based on weather conditions"""
    if is_sunny:
        return "sun"
    elif weather_main == "Rain":
        return "cloud-rain"
    elif weather_main == "Snow":
        return "snowflake"
    elif weather_main == "Clouds":
        return "cloud"
    else:
        return "sun"


def weather_card():
    """Weather card component with amber-to-orange gradient and neo-brutalist design"""
    return rx.cond(
        State.weather_data,
        rx.box(
            rx.vstack(
                # Top Section: Current Weather
                rx.hstack(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(
                                rx.cond(
                                    State.weather_data["current"]["is_sunny"],
                                    "sun",
                                    rx.cond(
                                        State.weather_data["current"]["weather_main"]
                                        == "Rain",
                                        "cloud-rain",
                                        rx.cond(
                                            State.weather_data["current"][
                                                "weather_main"
                                            ]
                                            == "Snow",
                                            "snowflake",
                                            rx.cond(
                                                State.weather_data["current"][
                                                    "weather_main"
                                                ]
                                                == "Clouds",
                                                "cloud",
                                                "sun",
                                            ),
                                        ),
                                    ),
                                ),
                                size=rx.breakpoints(initial=32, md=48),
                                class_name="text-black",
                            ),
                            rx.text(
                                State.weather_data["current"]["temperature"],
                                State.weather_data["units"]["temperature"],
                                class_name="font-[dm] text-3xl md:text-5xl font-bold text-black",
                            ),
                            align="center",
                            spacing=rx.breakpoints(initial="2", md="3"),
                        ),
                        rx.text(
                            State.weather_data["current"]["weather_main"],
                            class_name="font-[dm] text-base md:text-2xl text-black font-medium",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.text(
                            State.weather_data["location"]["city"],
                            ", ",
                            State.weather_data["location"]["state"],
                            class_name="font-[dm] text-sm md:text-xl text-black font-medium",
                        ),
                        rx.text(
                            State.weather_data["timestamp"]["current_day"],
                            ", ",
                            State.weather_data["timestamp"]["current_time"],
                            class_name="font-[dm] text-xs md:text-lg text-black",
                        ),
                        rx.cond(
                            State.weather_data["daily_forecast"],
                            rx.text(
                                "H: ",
                                State.weather_data["daily_forecast"][0]["high_temp"],
                                "° L: ",
                                State.weather_data["daily_forecast"][0]["low_temp"],
                                "°",
                                class_name="font-[dm] text-xs md:text-lg text-black",
                            ),
                        ),
                        align="end",
                        spacing="1",
                    ),
                    class_name="w-full",
                    align="center",
                    spacing="4",
                ),
                # Bottom Section: 6-Day Forecast
                rx.cond(
                    State.weather_data["daily_forecast"],
                    rx.hstack(
                        rx.foreach(
                            State.weather_data["daily_forecast"],
                            lambda day, index: rx.vstack(
                                rx.text(
                                    day["day_short"],
                                    class_name="font-[dm] text-sm md:text-lg text-black font-medium",
                                ),
                                rx.icon(
                                    rx.cond(
                                        day["is_sunny"],
                                        "sun",
                                        rx.cond(
                                            day["weather_main"] == "Rain",
                                            "cloud-rain",
                                            rx.cond(
                                                day["weather_main"] == "Snow",
                                                "snowflake",
                                                rx.cond(
                                                    day["weather_main"] == "Clouds",
                                                    "cloud",
                                                    "sun",
                                                ),
                                            ),
                                        ),
                                    ),
                                    size=rx.breakpoints(initial=20, md=32),
                                    class_name="text-black my-1 md:my-2",
                                ),
                                rx.text(
                                    day["high_temp"],
                                    "°",
                                    class_name="font-[dm] text-base md:text-xl text-black font-bold",
                                ),
                                rx.text(
                                    day["low_temp"],
                                    "°",
                                    class_name="font-[dm] text-sm md:text-lg text-black",
                                ),
                                align="center",
                                class_name="flex-1 min-w-0",
                                spacing="1",
                            ),
                        ),
                        class_name="w-full pt-4",
                        spacing=rx.breakpoints(initial="1", md="4"),
                        justify="between",
                        wrap="nowrap",
                    ),
                ),
                class_name="w-full",
                spacing="6",
            ),
            class_name="bg-gradient-to-br from-amber-300 to-orange-400 p-4 md:p-6 rounded-2xl md:rounded-3xl shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] border-2 md:border-4 border-black",
            width="100%",
            # max_width=rx.breakpoints(initial="100%", md="800px"),
        ),
    )
