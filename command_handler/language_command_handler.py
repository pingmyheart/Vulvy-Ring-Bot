from telebot import TeleBot, types

from service import RingService, UserService
from util import MessageUtil
from util.constant import Constant


class LanguageCommandHandler:
    def __init__(self, tg_bot: TeleBot,
                 constant_bean: Constant,
                 ring_service_bean: RingService,
                 user_service_bean: UserService,
                 message_util_bean: MessageUtil):
        self.bot = tg_bot
        self.constant_bean = constant_bean
        self.ring_service_bean = ring_service_bean
        self.user_service_bean = user_service_bean
        self.message_util_bean = message_util_bean

    def handle(self, message):
        markup = types.InlineKeyboardMarkup()
        italian_flag = types.InlineKeyboardButton('🇮🇹 Italiano', callback_data="it-set")
        english_flag = types.InlineKeyboardButton('🇬🇧 English', callback_data="en-set")
        spanish_flag = types.InlineKeyboardButton('🇪🇸 Español', callback_data="es-set")
        french_flag = types.InlineKeyboardButton('🇫🇷 Français', callback_data="fr-set")
        german_flag = types.InlineKeyboardButton('🇩🇪 Deutsch', callback_data="de-set")
        markup.add(italian_flag, english_flag, spanish_flag, french_flag, german_flag)
        self.bot.send_message(chat_id=message.chat.id,
                              text=self.constant_bean.select_language(
                                  self.user_service_bean.retrieve_user_language_preference(
                                      chat_id=message.chat.id)).format(
                                  username=self.message_util_bean.extract_user_name(message)),
                              parse_mode=self.constant_bean.parser(),
                              reply_markup=markup)
