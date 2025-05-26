from telebot import TeleBot, types

from service import RingService, UserService
from util.constant import Constant


class ConfigureCommandHandler:
    def __init__(self, tg_bot: TeleBot,
                 constant_bean: Constant,
                 ring_service_bean: RingService,
                 user_service_bean: UserService):
        self.bot = tg_bot
        self.constant_bean = constant_bean
        self.ring_service_bean = ring_service_bean
        self.user_service_bean = user_service_bean

    def handle(self, message):
        markup = types.InlineKeyboardMarkup()
        ring = types.InlineKeyboardButton(
            f'💊 {self.constant_bean.ring_placeholder(self.user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))}',
            callback_data="ring")
        user = types.InlineKeyboardButton(
            f'👤 {self.constant_bean.user_placeholder(self.user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))}',
            callback_data="user")
        markup.add(ring, user)
        self.bot.send_message(chat_id=message.chat.id,
                              text=self.constant_bean.select_configuration_option(
                                  self.user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)),
                              parse_mode=self.constant_bean.parser(),
                              reply_markup=markup)
