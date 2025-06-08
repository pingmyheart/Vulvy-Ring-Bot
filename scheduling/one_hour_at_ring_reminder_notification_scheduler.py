from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telebot import TeleBot

from configuration.logging_configuration import logger as log
from enumerated.ring_status_enum import RingStatusEnum
from persistence.model.user_model import UserModel
from service.ring_service import RingService
from service.user_service import UserService
from util import constant_bean, Constant


class OneHourAtRingReminderNotificationScheduler:
    def __init__(self, user_service_bean: UserService,
                 ring_service_bean: RingService,
                 constant_bean: Constant,
                 tg_bot: TeleBot):
        self.user_service_bean = user_service_bean
        self.ring_service_bean = ring_service_bean
        self.constant_bean = constant_bean
        self.tg_bot = tg_bot

    def schedule(self):
        now = datetime.now(ZoneInfo("UTC"))
        for user in self.user_service_bean.retrieve_all_users():
            log.info(f"Checking user `{user.id}`")
            try:
                if not user.ring.ring_date or not user.ring.ring_insertion_time:
                    log.info(f"Skipping user `{user.id}` due to missing ring date or insertion time")
                    continue
                tz = ZoneInfo(user.timezone.time_zone)
                now_at_timezone = now.astimezone(tz)
                ring_date = datetime.strptime(user.ring.ring_date, "%Y-%m-%d")
                ring_time = datetime.strptime(user.ring.ring_insertion_time, "%H:%M")
                if user.ring.ring_status == RingStatusEnum.INSERTED.code:
                    if now_at_timezone.day == (ring_date + timedelta(days=21)).day and \
                            now_at_timezone.month == (ring_date + timedelta(days=21)).month and \
                            now_at_timezone.hour == (ring_time.hour + 1) and \
                            now_at_timezone.minute == ring_time.minute:
                        self.__handle_notify(ring_status=RingStatusEnum.REMOVED,
                                             user=user)
                else:
                    if now_at_timezone.day == (ring_date + timedelta(days=7)).day and \
                            now_at_timezone.month == (ring_date + timedelta(days=7)).month and \
                            now_at_timezone.hour == (ring_time.hour + 1) and \
                            now_at_timezone.minute == ring_time.minute:
                        self.__handle_notify(ring_status=RingStatusEnum.INSERTED,
                                             user=user)
            except Exception as e:
                log.warn(f"Error with user {user.id}, {e}")

    def __handle_notify(self, ring_status: RingStatusEnum,
                        user: UserModel):
        log.info(f"Tomorrow is ring day for user `{user.id}` with status `{ring_status}`")
        if RingStatusEnum.INSERTED == ring_status:
            self.tg_bot.send_message(chat_id=user.user.chat_id,
                                     text=self.constant_bean.one_hour_at_ring_insertion(
                                         self.user_service_bean.retrieve_user_language_preference(
                                             chat_id=user.user.chat_id)),
                                     parse_mode=constant_bean.parser())
        else:
            self.tg_bot.send_message(chat_id=user.user.chat_id,
                                     text=self.constant_bean.one_hour_at_ring_removal(
                                         self.user_service_bean.retrieve_user_language_preference(
                                             chat_id=user.user.chat_id)),
                                     parse_mode=constant_bean.parser())
