from datetime import datetime, timedelta, time
from typing import List

from enumerated.ring_status_enum import RingStatusEnum
from persistence.model.user_model import UserModel, RingInformation
from persistence.repository import UserRepository


class RingService:
    def __init__(self, user_repository):
        self.user_repository: UserRepository = user_repository

    def generate_ring_calendar(self, chat_id: int) -> List | None:
        """
        Generate a ring calendar for the user.
        """
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is None:
            return None
        if user.ring is None:
            return None
        if user.ring.ring_status is None or user.ring.ring_date is None:
            return None
        if user.ring.ring_status == RingStatusEnum.INSERTED.code:
            calendar: List = []
            relative_date: datetime = datetime.strptime(user.ring.ring_date, "%Y-%m-%d")
            for _ in range(6):
                calendar.append({"date": relative_date + timedelta(days=21), "status": RingStatusEnum.REMOVED})
                calendar.append({"date": relative_date + timedelta(days=28), "status": RingStatusEnum.INSERTED})
                relative_date = relative_date + timedelta(days=28)
        else:
            calendar = []
            relative_date: datetime = datetime.strptime(user.ring.ring_date, "%Y-%m-%d")
            for _ in range(6):
                calendar.append({"date": relative_date + timedelta(days=7), "status": RingStatusEnum.INSERTED})
                calendar.append({"date": relative_date + timedelta(days=28), "status": RingStatusEnum.REMOVED})
                relative_date = relative_date + timedelta(days=28)
        return calendar

    def update_ring_status(self, chat_id: int,
                           ring_status: RingStatusEnum):
        """
        Update the ring status of the user.
        """
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is not None:
            user.ring.ring_status = ring_status.code
            self.user_repository.save(user=user)

    def update_ring_date(self, chat_id: int,
                         ring_date: str):
        """
        Update the ring date of the user.
        """
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is not None:
            if user.ring is None:
                user.ring = RingInformation()
            user.ring.ring_date = ring_date
            self.user_repository.save(user=user)

    def update_ring_insertion_time(self, chat_id: int,
                                   ring_insertion_time: str):
        """
        Update the ring insertion time of the user.
        """
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is not None:
            user.ring.ring_insertion_time = ring_insertion_time
            self.user_repository.save(user=user)

    def verify_ring_day(self, chat_id: int,
                        ring_date: datetime,
                        ring_time: time = None):
        """
        Verify if given date is a ring day for the user and apply time control if provided.
        """
        calendar: List = self.generate_ring_calendar(chat_id=chat_id)
        user: UserModel = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if calendar is not None:
            calendar_date = calendar[0]["date"]
            status = calendar[0]["status"]
            if ring_time:
                if ring_date.day == calendar_date.day and \
                        ring_date.month == calendar_date.month and \
                        user.ring.ring_insertion_time.split(":")[0] == str(ring_time.hour) and \
                        user.ring.ring_insertion_time.split(":")[1] == str(ring_time.minute):
                    return status
            else:
                if ring_date.day == calendar_date.day and \
                        ring_date.month == calendar_date.month:
                    return status
        return None
