"""
модуль обробки запитів
"""
from telegram import Update
from telegram.ext import ContextTypes
from open_weather_api import get_current_weather_by_city, weather_to_text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обробник команди /start
    """
    text = (
        "Привіт! Я бот прогнозу погоди.\n\n"
        "Надішли мені назву міста, і я покажу поточну погоду.\n"
        "Наприклад: Київ, Львів, London."
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обробник команди /help
    """
    text = (
        "Список команд:\n"
        "/start – початок роботи\n"
        "/help – довідка\n\n"
        "Щоб дізнатися погоду, напиши назву міста."
    )
    await update.message.reply_text(text)


async def handled_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обробка тексту, який не є командою.
    """
    if not update.message:
        return

    city = update.message.text.strip()

    if len(city) < 2:
        await update.message.reply_text("Введи коректну назву міста.")
        return

    await update.message.reply_text("Зачекай, отримую погоду...")

    data = await get_current_weather_by_city(city)
    reply = weather_to_text(data)

    await update.message.reply_text(reply)
