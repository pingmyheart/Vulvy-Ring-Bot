from persistence.model.user_model import UserModel, UserInformation, RingInformation, TimeZoneInformation
from persistence.repository import UserRepository


class UserService:
    def __init__(self, user_repository):
        self.user_repository: UserRepository = user_repository

    def start_user(self, username: str,
                   chat_id: int):
        user: UserModel = UserModel(user=UserInformation(username=username,
                                                         chat_id=chat_id,
                                                         language="en"),
                                    ring=RingInformation(ring_insertion_time="13:00"),
                                    timezone=TimeZoneInformation(time_zone="Europe/Rome"))
        self.user_repository.save(user=user)

    def update_user_language_preference(self, chat_id: int,
                                        language: str, ):
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        user.user.language = language
        self.user_repository.save(user=user)

    def retrieve_user_language_preference(self, chat_id: int) -> str:
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is not None:
            return user.user.language
        return "en"

    def retrieve_user(self, chat_id) -> UserModel:
        return self.user_repository.find_by_chat_id(chat_id=chat_id)

    def retrieve_all_users(self):
        return self.user_repository.find_all()

    def update_user_timezone(self, chat_id: int,
                             time_zone: str):
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is not None:
            user.timezone.time_zone = time_zone
            self.user_repository.save(user=user)
        else:
            raise ValueError("User not found")
