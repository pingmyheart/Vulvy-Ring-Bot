from telebot import TeleBot, types
from timezonefinder import TimezoneFinder

from service import RingService, UserService
from util.constant import Constant


class LocationCommandHandler:
    def __init__(self, tg_bot: TeleBot,
                 constant_bean: Constant,
                 ring_service_bean: RingService,
                 user_service_bean: UserService):
        self.bot = tg_bot
        self.constant_bean = constant_bean
        self.ring_service_bean = ring_service_bean
        self.user_service_bean = user_service_bean
        self.timezone_finder = TimezoneFinder()

    def handle(self, message):
        lat = message.location.latitude
        lon = message.location.longitude
        timezone = self.timezone_finder.timezone_at(lat=lat, lng=lon)
        if timezone:
            self.user_service_bean.update_user_timezone(chat_id=message.chat.id,
                                                        time_zone=timezone)
            self.bot.send_message(chat_id=message.chat.id,
                                  text=self.constant_bean.timezone_correctly_settled(
                                      self.user_service_bean.retrieve_user_language_preference(
                                          chat_id=message.chat.id)),
                                  parse_mode=self.constant_bean.parser(),
                                  reply_markup=types.ReplyKeyboardRemove())
        else:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=self.constant_bean.timezone_set_error(
                                      self.user_service_bean.retrieve_user_language_preference(
                                          chat_id=message.chat.id)),
                                  parse_mode=self.constant_bean.parser(),
                                  reply_markup=types.ReplyKeyboardRemove())
