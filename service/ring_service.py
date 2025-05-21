from datetime import datetime, timedelta
from typing import List

from enumerated.ring_status_enum import RingStatusEnum
from persistence.repository import UserRepository


class RingService:
    def __init__(self, user_repository):
        self.user_repository: UserRepository = user_repository

    def generate_ring_calendar(self, chat_id: int) -> List | None:
        """
        Generate a ring calendar for the user.
        """
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is not None:
            if user.ring.ring_status == RingStatusEnum.INSERTED.code:
                calendar: List = []
                relative_date: datetime = user.ring.ring_date
                for _ in range(6):
                    calendar.append({"date": relative_date + timedelta(days=21), "status": RingStatusEnum.REMOVED})
                    calendar.append({"date": relative_date + timedelta(days=28), "status": RingStatusEnum.INSERTED})
                    relative_date = relative_date + timedelta(days=28)
            else:
                calendar = []
                relative_date: datetime = user.ring.ring_date
                for _ in range(6):
                    calendar.append({"date": relative_date + timedelta(days=7), "status": RingStatusEnum.INSERTED})
                    calendar.append({"date": relative_date + timedelta(days=28), "status": RingStatusEnum.REMOVED})
                    relative_date = relative_date + timedelta(days=28)
            return calendar
        return None

    def update_ring_status(self, chat_id: int,
                           ring_status: RingStatusEnum):
        """
        Update the ring status of the user.
        """
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is not None:
            user.ring.ring_status = ring_status.code
            self.user_repository.save(user=user)

    def is_today_a_ring_day(self, chat_id: int):
        """
        Check if today is a ring day for the user.
        """
        calendar: List = self.generate_ring_calendar(chat_id=chat_id)
        if calendar is not None:
            date = calendar[0]["date"]
            status = calendar[0]["status"]
            if date.day == datetime.now().day and date.month == datetime.now().month:
                return status
        return None
