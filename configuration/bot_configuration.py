import os

from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()


def bot() -> TeleBot:
    bot_token = os.getenv("TG_BOT_TOKEN")

    if bot_token is None:
        raise IOError("TG_BOT_TOKEN env variable required")

    return TeleBot(bot_token)
