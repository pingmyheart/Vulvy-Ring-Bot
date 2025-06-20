from telebot import TeleBot, types

from service import RingService, UserService
from util import MessageUtil
from util.constant import Constant


class StartCommandHandler:
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
        italian_flag = types.InlineKeyboardButton('🇮🇹 Italiano', callback_data="it")
        english_flag = types.InlineKeyboardButton('🇬🇧 English', callback_data="en")
        spanish_flag = types.InlineKeyboardButton('🇪🇸 Español', callback_data="es")
        french_flag = types.InlineKeyboardButton('🇫🇷 Français', callback_data="fr")
        german_flag = types.InlineKeyboardButton('🇩🇪 Deutsch', callback_data="de")
        markup.add(italian_flag, english_flag, spanish_flag, french_flag, german_flag)
        response, markup = self.constant_bean.select_language().format(
            username=self.message_util_bean.extract_user_name(message)), markup

        # start new user interaction
        self.user_service_bean.start_user(username=self.message_util_bean.extract_user_name(message),
                                          chat_id=message.chat.id)
        # send a welcome message
        self.bot.send_message(chat_id=message.chat.id,
                              text=response,
                              parse_mode=self.constant_bean.parser(),
                              reply_markup=markup)
