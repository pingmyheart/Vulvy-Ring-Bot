import os
import re

import telebot
from dotenv import load_dotenv
from telebot import types

from decorator.before_bot_decorator import log_trigger
from service import user_service_bean
from util import constant_bean
from util import message_util_bean

load_dotenv()

bot_token = os.getenv("TG_BOT_TOKEN")

if bot_token is None:
    raise IOError("TG_BOT_TOKEN env variable required")

bot = telebot.TeleBot(bot_token)
user_state = {}

# Define bot commands
commands = [
    types.BotCommand("/start", "Start interacting with the bot"),
    types.BotCommand("/help", "Show help information"),
    types.BotCommand("/language", "Imposta lingua"),
    types.BotCommand("/configure", "Configure information"),
    types.BotCommand("/calendar", "Show next ring calendar")
]

bot.set_my_commands(commands)


@bot.message_handler(commands=['start'])
@log_trigger
def handle_start(message):
    markup = types.InlineKeyboardMarkup()
    italian_flag = types.InlineKeyboardButton('🇮🇹 Italiano', callback_data="it")
    english_flag = types.InlineKeyboardButton('🇬🇧 English', callback_data="en")
    spanish_flag = types.InlineKeyboardButton('🇪🇸 Español', callback_data="es")
    french_flag = types.InlineKeyboardButton('🇫🇷 Français', callback_data="fr")
    german_flag = types.InlineKeyboardButton('🇩🇪 Deutsch', callback_data="de")
    markup.add(italian_flag, english_flag, spanish_flag, french_flag, german_flag)
    response, markup = constant_bean.select_language().format(
        username=message_util_bean.extract_user_name(message)), markup

    # start new user interaction
    user_service_bean.start_user(username=message_util_bean.extract_user_name(message),
                                 chat_id=message.chat.id)
    # send a welcome message
    bot.send_message(chat_id=message.chat.id,
                     text=response,
                     parse_mode=constant_bean.parser(),
                     reply_markup=markup)


@bot.message_handler(commands=['configure'])
@log_trigger
def handle_configure(message):
    markup = types.InlineKeyboardMarkup()
    ring = types.InlineKeyboardButton('📅 Ring', callback_data="ring")
    user = types.InlineKeyboardButton('👤 User', callback_data="user")
    markup.add(ring, user)
    bot.send_message(chat_id=message.chat.id,
                     text=constant_bean.select_configuration_option(
                         user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                     parse_mode=constant_bean.parser(),
                     reply_markup=markup)


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "await_config_selection")
@log_trigger
def track(message):
    pass


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "awaiting_insertion_time")
@log_trigger
def track(message):
    pass


@bot.message_handler(commands=['help'])
@log_trigger
def handle_help(message):
    response = constant_bean.help_commands(user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))
    bot.send_message(chat_id=message.chat.id,
                     text=response,
                     parse_mode=constant_bean.parser())


@bot.callback_query_handler(func=lambda call: True)
@log_trigger
def handle_query(call):
    if re.match(r'^it$|^en$|^es$|^fr$|^de$', call.data):
        user_service_bean.update_user_language_preference(call.from_user.id, call.data)
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.welcome_message(lang=call.data).format(
                             username=message_util_bean.extract_user_name(call)),
                         parse_mode=constant_bean.parser())
        handle_help(call.message)
    elif call.data == "ring":
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.service_not_implemented(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser())
    elif call.data == "user":
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.service_not_implemented(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser())
    else:
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.unknown_option(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser())


# Fallback handler for any other message
@bot.message_handler(func=lambda message: True)
@log_trigger
def handle_all_messages(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=constant_bean.fallback(user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
        parse_mode=constant_bean.parser())


bot.infinity_polling()
