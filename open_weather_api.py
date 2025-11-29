"""
модуль взаємодії з API openweathermap.
"""
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_TOKEN: str = os.getenv("OPEN_WEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_LANG = "ua"
DEFAULT_UNITS = "metric"


async def get_current_weather_by_city(city: str) -> dict | None:
    """
    Запит до OpenWeatherMap за назвою міста.
    :return: dict or None.
    """

    params = {
        "q": city,
        "appid": OPEN_WEATHER_TOKEN,
        "lang": DEFAULT_LANG,
        "units": DEFAULT_UNITS,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL, params=params, timeout=5) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
    except Exception:
        return None


def weather_to_text(data: dict | None) -> str:
    """
    Форматує відповідь OpenWeatherMap.
    :return: str
    """
    if not data:
        return "Не вдалося отримати дані з сервера погоди. Спробуй ще раз пізніше."

    if str(data.get("cod")) != "200":
        msg = data.get("message", "невідома помилка")
        return f"Не вдалося знайти погоду для цього міста. Деталі: {msg}."

    name = data.get("name", "Невідоме місце")
    main = data.get("main", {})
    weather_list = data.get("weather", [])
    wind = data.get("wind", {})

    temp = main.get("temp")
    feels_like = main.get("feels_like")
    humidity = main.get("humidity")
    pressure = main.get("pressure")
    description = weather_list[0]["description"] if weather_list else "немає опису"
    wind_speed = wind.get("speed")

    lines = [
        f"Погода в місті: {name}",
        f"Опис: {description.capitalize()}",
        f"Температура: {temp} °C (відчувається як {feels_like} °C)",
        f"Вологість: {humidity} %",
        f"Тиск: {pressure} гПа",
        f"Швидкість вітру: {wind_speed} м/с",
    ]

    return "\n".join(lines)
