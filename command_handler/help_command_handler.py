from telebot import TeleBot

from service import RingService, UserService
from util.constant import Constant


class HelpCommandHandler:
    def __init__(self, tg_bot: TeleBot,
                 constant_bean: Constant,
                 ring_service_bean: RingService,
                 user_service_bean: UserService):
        self.bot = tg_bot
        self.constant_bean = constant_bean
        self.ring_service_bean = ring_service_bean
        self.user_service_bean = user_service_bean

    def handle(self, message):
        response = self.constant_bean.help_commands(
            self.user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))
        self.bot.send_message(chat_id=message.chat.id,
                              text=response,
                              parse_mode=self.constant_bean.parser())
