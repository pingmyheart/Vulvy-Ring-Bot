from datetime import datetime
from zoneinfo import ZoneInfo

from telebot import TeleBot

from service import UserService
from util import Constant


class BirthdayNotificationScheduler:
    def __init__(self, user_service_bean: UserService,
                 constant_bean: Constant,
                 tg_bot: TeleBot):
        self.user_service_bean = user_service_bean
        self.constant_bean = constant_bean
        self.tg_bot = tg_bot

    def schedule(self):
        now = datetime.now(ZoneInfo("UTC"))
        users_with_birthdays_today = self.user_service_bean.get_users_with_birthdays_today()
        for user in users_with_birthdays_today:
            now_at_user_timezone = now.astimezone(ZoneInfo(user.timezone.time_zone))
            if now_at_user_timezone.hour == 11 and \
                    now_at_user_timezone.minute == 0:
                self.tg_bot.send_message(chat_id=user.user.chat_id,
                                         text=f"🎊🎉🥳{self.constant_bean.happy_birthday(self.user_service_bean.retrieve_user_language_preference(chat_id=user.user.chat_id)).format(username=user.user.username)}",
                                         parse_mode=self.constant_bean.parser())
