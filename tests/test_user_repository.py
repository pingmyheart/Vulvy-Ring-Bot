from datetime import datetime
from unittest import TestCase

from testcontainers.mongodb import MongoDbContainer

from enumerated.ring_status_enum import RingStatusEnum
from persistence.model.user_model import UserModel, UserInformation, RingInformation
from persistence.repository.user_repository import UserRepository


class TestUserRepository(TestCase):
    def test_insert_and_retrieve(self):
        with MongoDbContainer("mongo:7.0.17") as mongo:
            database = mongo.get_connection_client()["test"]
            repository = UserRepository(database=database)

            user = UserModel(user=UserInformation(username="mario_rossi",
                                                  chat_id=1234567890,
                                                  date_of_birth=datetime.strptime("1990-10-10", "%Y-%m-%d").__str__()),
                             ring=RingInformation(ring_date=datetime.now().strftime("%Y-%m-%d"),
                                                  ring_insertion_time="15:00",
                                                  ring_status=RingStatusEnum.INSERTED.code))
            user2 = UserModel(user=UserInformation(username="marco_rossi",
                                                   chat_id=12345637890,
                                                   date_of_birth=datetime.strptime("1990-10-10", "%Y-%m-%d").__str__()),
                              ring=RingInformation(ring_date=datetime.now().strftime("%Y-%m-%d"),
                                                   ring_insertion_time="15:00",
                                                   ring_status=RingStatusEnum.INSERTED.code))

            repository.save(user=user)
            repository.save(user=user2)
            user_from_db = repository.find_by_username("mario_rossi")
            user2_from_db = repository.find_by_username("marco_rossi")
            print(user_from_db)
            print(user2_from_db)
            assert user_from_db is not None
            assert user2_from_db is not None
