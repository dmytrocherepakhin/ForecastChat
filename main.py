"""
модуль запуску бота
"""
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot_handlers import start, help_command, handled_message


load_dotenv()
TELEGRAM_TOKEN: str = os.getenv('BOT_TOKEN')


def main():
    """
    створення бота
    :return: None
    """
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handled_message))
    app.run_polling()


if __name__ == "__main__":
    main()
