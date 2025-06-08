from telebot import TeleBot

from enumerated.ring_status_enum import RingStatusEnum
from service import RingService, UserService
from util.constant import Constant


class CalendarCommandHandler:
    def __init__(self, tg_bot: TeleBot,
                 constant_bean: Constant,
                 ring_service_bean: RingService,
                 user_service_bean: UserService):
        self.bot = tg_bot
        self.constant_bean = constant_bean
        self.ring_service_bean = ring_service_bean
        self.user_service_bean = user_service_bean

    def handle(self, message):
        calendar = self.ring_service_bean.generate_ring_calendar(chat_id=message.chat.id)
        if calendar:
            formatted_string = ""
            for element in calendar:
                status = self.constant_bean.ring_insert(
                    self.user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id)) \
                    if (element["status"] == RingStatusEnum.INSERTED) \
                    else self.constant_bean.ring_remove(
                    self.user_service_bean.retrieve_user_language_preference(chat_id=message.chat.id))
                status_emoji = "🛟⬆️" if element["status"] == RingStatusEnum.INSERTED else "🛟⬇️"
                status_emoji_rev = "⬆️🛟" if element["status"] == RingStatusEnum.INSERTED else "⬇️🛟"
                formatted_string += f'📆 {element["date"]} - {status_emoji} {status} {status_emoji_rev}\n'
            self.bot.send_message(chat_id=message.chat.id,
                                  text=formatted_string,
                                  parse_mode=self.constant_bean.parser())
        else:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=self.constant_bean.date_not_available(
                                      self.user_service_bean.retrieve_user_language_preference(
                                          chat_id=message.chat.id)),
                                  parse_mode=self.constant_bean.parser())
