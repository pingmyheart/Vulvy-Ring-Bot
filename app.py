import re
from datetime import datetime

from telebot import types
from timezonefinder import TimezoneFinder

import scheduling
from configuration import bot
from configuration.logging_configuration import logger as log
from decorator.before_bot_decorator import log_triggered_method
from enumerated.ring_status_enum import RingStatusEnum
from service import user_service_bean, ring_service_bean
from util import constant_bean
from util import message_util_bean

tf = TimezoneFinder()
[log.info(f"Import {_module} module") for _module in [scheduling]]
user_state = {}

# Define bot commands
commands = [
    types.BotCommand("/start", "Start interacting with the bot"),
    types.BotCommand("/help", "Show help information"),
    types.BotCommand("/language", "Configure language preferences"),
    types.BotCommand("/configure", "Configure information"),
    types.BotCommand("/calendar", "Show next ring calendar")
]

bot.set_my_commands(commands)


@bot.message_handler(commands=['start'])
@log_triggered_method
def handle_start(message):
    from command_handler import start_command_handler_bean
    start_command_handler_bean.handle(message=message)


@bot.message_handler(commands=['configure'])
@log_triggered_method
def handle_configure(message):
    from command_handler import configure_command_handler_bean
    configure_command_handler_bean.handle(message=message)


@bot.message_handler(commands=['calendar'])
@log_triggered_method
def handle_calendar(message):
    from command_handler import calendar_command_handler_bean
    calendar_command_handler_bean.handle(message=message)


@bot.message_handler(commands=['help'])
@log_triggered_method
def handle_help(message):
    from command_handler import help_command_handler_bean
    help_command_handler_bean.handle(message=message)


@bot.message_handler(commands=['language'])
@log_triggered_method
def handle_language(message):
    from command_handler import language_command_handler_bean
    language_command_handler_bean.handle(message=message)


@bot.message_handler(content_types=["location"])
@log_triggered_method
def handle_location(message):
    from command_handler import location_command_handler_bean
    location_command_handler_bean.handle(message=message)


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "awaiting_birth_date_insertion")
@log_triggered_method
def handle_birth_date_insertion(message):
    try:
        provided_date = datetime.strptime(message.text, "%Y-%m-%d")
        parsed_time = f'{provided_date.year}-{provided_date.month}-{provided_date.day}'
        user_service_bean.update_birth_date(chat_id=message.chat.id,
                                            birth_date=parsed_time)
        user_state[message.chat.id] = None
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.ring_date_accepted(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())
    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.invalid_date(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "awaiting_ring_insertion_date")
@log_triggered_method
def handle_ring_insertion_date(message):
    try:
        provided_date = datetime.strptime(message.text, "%Y-%m-%d")
        parsed_time = f'{provided_date.year}-{provided_date.month}-{provided_date.day}'
        ring_service_bean.update_ring_date(chat_id=message.chat.id,
                                           ring_date=parsed_time)
        ring_service_bean.update_ring_status(chat_id=message.chat.id,
                                             ring_status=RingStatusEnum.INSERTED)
        user_state[message.chat.id] = "awaiting_ring_insertion_time"
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.ring_date_accepted(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.insertion_time(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())
    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.invalid_date(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "awaiting_ring_insertion_time")
@log_triggered_method
def handle_ring_insertion_time(message):
    try:
        provided_time = datetime.strptime(message.text, "%H:%M")
        parsed_time = f'{provided_time.hour}:{provided_time.minute}'
        ring_service_bean.update_ring_insertion_time(chat_id=message.chat.id,
                                                     ring_insertion_time=parsed_time)
        user_state[message.chat.id] = None
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.ring_time_accepted(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())
        handle_configure(message)
    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text=constant_bean.invalid_time(
                             user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                         parse_mode=constant_bean.parser())


@bot.message_handler(func=lambda
        message: message.text == f'🎂 {constant_bean.birthday_placeholder(user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))}')
@log_triggered_method
def handle_birth_date_button(message):
    user_state[message.chat.id] = "awaiting_birth_date_insertion"


@bot.callback_query_handler(func=lambda call: True)
@log_triggered_method
def handle_query(call):
    if re.match(r'^it$|^en$|^es$|^fr$|^de$', call.data):
        user_service_bean.update_user_language_preference(call.from_user.id, call.data)
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.welcome_message(lang=call.data).format(
                             username=message_util_bean.extract_user_name(call)),
                         parse_mode=constant_bean.parser())
        handle_configure(call.message)
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
            f'📅 {constant_bean.insertion_date_time_placeholder(user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id))}',
            callback_data="insertion-date-time-set")
        markup.add(date_insertion)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.choose_option(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser(),
                         reply_markup=markup)
    elif call.data == "insertion-date-time-set":
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        user_state[call.message.chat.id] = "awaiting_ring_insertion_date"
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.insertion_date(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser())
    elif call.data == "user":
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True)
        location_button = types.KeyboardButton(
            f'📍 {constant_bean.location_for_timezone_placeholder(user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id))}',
            request_location=True)
        birthday_button = types.KeyboardButton(
            f'🎂 {constant_bean.birthday_placeholder(user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id))}')
        markup.add(location_button, birthday_button)
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.choose_option(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser(),
                         reply_markup=markup)
    else:
        bot.send_message(chat_id=call.message.chat.id,
                         text=constant_bean.unknown_option(
                             user_service_bean.retrieve_user_language_preference(chat_id=call.message.chat.id)),
                         parse_mode=constant_bean.parser())


# Fallback handler for any other message
@bot.message_handler(func=lambda message: True)
@log_triggered_method
def handle_all_messages(message):
    bot.send_message(chat_id=message.chat.id,
                     text=constant_bean.fallback(
                         user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                     parse_mode=constant_bean.parser())


bot.infinity_polling()
