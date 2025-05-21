import os

import telebot
from dotenv import load_dotenv
from telebot import types

from service import user_service_bean
from util import constant_bean

load_dotenv()

bot_token = os.getenv("TG_BOT_TOKEN")

if bot_token is None:
    raise IOError("TG_BOT_TOKEN env variable required")

bot = telebot.TeleBot(bot_token)

# Define bot commands
commands = [
    types.BotCommand("/start", "Start interacting with the bot"),
    types.BotCommand("/help", "Show help information"),
    types.BotCommand("/configure", "Configure ring information"),
    types.BotCommand("/calendar", "Show next ring calendar")
]

bot.set_my_commands(commands)


def extract_user_name(message):
    if hasattr(message.from_user, "first_name"):
        return message.from_user.first_name
    elif hasattr(message.from_user, "username"):
        return message.from_user.username
    else:
        return "there"


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup()
    italian_flag = types.InlineKeyboardButton('🇮🇹 Italiano', callback_data="it")
    english_flag = types.InlineKeyboardButton('🇬🇧 English', callback_data="en")
    spanish_flag = types.InlineKeyboardButton('🇪🇸 Español', callback_data="es")
    french_flag = types.InlineKeyboardButton('🇫🇷 Français', callback_data="fr")
    german_flag = types.InlineKeyboardButton('🇩🇪 Deutsch', callback_data="de")
    markup.add(italian_flag, english_flag, spanish_flag, french_flag, german_flag)
    response, markup = constant_bean.select_language().format(username=extract_user_name(message)), markup

    # start new user interaction
    user_service_bean.start_user(username=extract_user_name(message),
                                 chat_id=message.chat.id)
    # send a welcome message
    bot.send_message(chat_id=message.chat.id,
                     text=response,
                     parse_mode=constant_bean.parser(),
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def handle_help(message):
    response = constant_bean.help_commands(user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))
    bot.send_message(chat_id=message.chat.id,
                     text=response,
                     parse_mode=constant_bean.parser())


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "it":
        user_service_bean.update_user_language_preference(call.from_user.id, "it")
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.welcome_message(lang="it").format(
                             username=extract_user_name(call)),
                         parse_mode=constant_bean.parser())
        handle_help(call.message)
    elif call.data == "en":
        user_service_bean.update_user_language_preference(call.from_user.id, "en")
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.welcome_message(lang="en").format(
                             username=extract_user_name(call)),
                         parse_mode=constant_bean.parser())
        handle_help(call.message)
    elif call.data == "es":
        user_service_bean.update_user_language_preference(call.from_user.id, "es")
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.welcome_message(lang="es").format(
                             username=extract_user_name(call)),
                         parse_mode=constant_bean.parser())
        handle_help(call.message)
    elif call.data == "fr":
        user_service_bean.update_user_language_preference(call.from_user.id, "fr")
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.welcome_message(lang="fr").format(
                             username=extract_user_name(call)),
                         parse_mode=constant_bean.parser())
        handle_help(call.message)
    elif call.data == "de":
        user_service_bean.update_user_language_preference(call.from_user.id, "de")
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.welcome_message(lang="de").format(
                             username=extract_user_name(call)),
                         parse_mode=constant_bean.parser())
        handle_help(call.message)
    else:
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.unknown_option(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser())


# Fallback handler for any other message
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=constant_bean.fallback(user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
        parse_mode=constant_bean.parser())


bot.infinity_polling()
