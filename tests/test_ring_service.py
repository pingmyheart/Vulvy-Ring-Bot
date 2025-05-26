from datetime import datetime
from unittest import TestCase

from testcontainers.mongodb import MongoDbContainer

from enumerated.ring_status_enum import RingStatusEnum
from persistence.model.user_model import UserModel, UserInformation, RingInformation
from persistence.repository.user_repository import UserRepository
from service.ring_service import RingService


class TestRingService(TestCase):
    def test_generate_ring_calendar(self):
        with MongoDbContainer("mongo:7.0.17") as mongo:
            database = mongo.get_connection_client()["test"]
            repository = UserRepository(database=database)
            ring_service = RingService(user_repository=repository)

            user = UserModel(user=UserInformation(username="maria_rossi",
                                                  chat_id=1234567890,
                                                  date_of_birth=datetime.strptime("1990-10-10", "%Y-%m-%d")),
                             ring=RingInformation(ring_date=datetime.now().strftime("%Y-%m-%d"),
                                                  ring_insertion_time="15:00",
                                                  ring_status=RingStatusEnum.INSERTED.code))

            repository.save(user=user)
            user_from_db = repository.find_by_chat_id(chat_id=1234567890)
            print(user_from_db)
            [print(date["date"]) for date in ring_service.generate_ring_calendar(chat_id=1234567890)]
            assert user_from_db is not None
