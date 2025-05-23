import os
import re
from datetime import datetime

import telebot
from dotenv import load_dotenv
from telebot import types

from decorator.before_bot_decorator import log_trigger
from enumerated.ring_status_enum import RingStatusEnum
from service import user_service_bean, ring_service_bean
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
    ring = types.InlineKeyboardButton(
        f'💊 {constant_bean.ring_placeholder(user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))}',
        callback_data="ring")
    user = types.InlineKeyboardButton(
        f'👤 {constant_bean.user_placeholder(user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))}',
        callback_data="user")
    markup.add(ring, user)
    bot.send_message(chat_id=message.chat.id,
                     text=constant_bean.select_configuration_option(
                         user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                     parse_mode=constant_bean.parser(),
                     reply_markup=markup)


@bot.message_handler(commands=['calendar'])
@log_trigger
def handle_calendar(message):
    calendar = ring_service_bean.generate_ring_calendar(chat_id=message.chat.id)
    if calendar:
        formatted_string = ""
        for element in calendar:
            formatted_string += f'{element["date"]} - {element["status"].i18n_key}\n'
        bot.send_message(chat_id=message.chat.id,
                         text=formatted_string,
                         parse_mode=constant_bean.parser())
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.date_not_available(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "awaiting_ring_insertion_time")
@log_trigger
def handle_ring_insertion_time(message):
    data = message.text
    try:
        parsed_time = f'{datetime.strptime(data, "%H:%M").hour}:{datetime.strptime(data, "%H:%M").minute}'
        ring_service_bean.update_ring_insertion_time(chat_id=message.chat.id,
                                                     ring_insertion_time=parsed_time)
        user_state[message.chat.id] = None
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.ring_time_accepted(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())
    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.invalid_time(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "awaiting_ring_insertion_date")
@log_trigger
def handle_ring_insertion_date(message):
    data = message.text
    try:
        parsed_time = f'{datetime.strptime(data, "%Y-%m-%d").year}-{datetime.strptime(data, "%Y-%m-%d").month}-{datetime.strptime(data, "%Y-%m-%d").day}'
        ring_service_bean.update_ring_date(chat_id=message.chat.id,
                                           ring_date=parsed_time)
        ring_service_bean.update_ring_status(chat_id=message.chat.id,
                                             ring_status=RingStatusEnum.INSERTED)
        user_state[message.chat.id] = None
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.ring_date_accepted(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())
    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.invalid_time(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())


@bot.message_handler(commands=['help'])
@log_trigger
def handle_help(message):
    response = constant_bean.help_commands(user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))
    bot.send_message(chat_id=message.chat.id,
                     text=response,
                     parse_mode=constant_bean.parser())


@bot.message_handler(commands=['language'])
@log_trigger
def handle_language(message):
    markup = types.InlineKeyboardMarkup()
    italian_flag = types.InlineKeyboardButton('🇮🇹 Italiano', callback_data="it-set")
    english_flag = types.InlineKeyboardButton('🇬🇧 English', callback_data="en-set")
    spanish_flag = types.InlineKeyboardButton('🇪🇸 Español', callback_data="es-set")
    french_flag = types.InlineKeyboardButton('🇫🇷 Français', callback_data="fr-set")
    german_flag = types.InlineKeyboardButton('🇩🇪 Deutsch', callback_data="de-set")
    markup.add(italian_flag, english_flag, spanish_flag, french_flag, german_flag)
    bot.send_message(chat_id=message.chat.id,
                     text=constant_bean.select_language(
                         user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)).format(
                         username=message_util_bean.extract_user_name(message)),
                     parse_mode=constant_bean.parser(),
                     reply_markup=markup)


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
    elif re.match(r'(^it|^en|^es|^fr|^de)-set$', call.data):
        language = call.data.replace("-set", "")
        user_service_bean.update_user_language_preference(chat_id=call.from_user.id,
                                                          language=language)
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.language_settled(lang=language).format(
                             username=message_util_bean.extract_user_name(message=call)),
                         parse_mode=constant_bean.parser())
    elif call.data == "ring":
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        date_insertion = types.InlineKeyboardButton(
            f'📅 {constant_bean.insertion_date_placeholder(user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id))}',
            callback_data="insertion-date-set")
        time_insertion = types.InlineKeyboardButton(
            f'⏱️ {constant_bean.insertion_time_placeholder(user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id))}',
            callback_data="insertion-time-set")
        markup.add(date_insertion, time_insertion)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.choose_option(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser(),
                         reply_markup=markup)
    elif call.data == "insertion-date-set":
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        user_state[call.message.chat.id] = "awaiting_ring_insertion_date"
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.insertion_date(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser())
    elif call.data == "insertion-time-set":
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        user_state[call.message.chat.id] = "awaiting_ring_insertion_time"
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.insertion_time(
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
