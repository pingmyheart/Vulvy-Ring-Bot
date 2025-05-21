from persistence.model.user_model import UserModel, UserInformation
from persistence.repository import UserRepository


class UserService:
    def __init__(self, user_repository):
        self.user_repository: UserRepository = user_repository

    def start_user(self, username: str,
                   chat_id: str):
        user: UserModel = UserModel(user=UserInformation(username=username,
                                                         chat_id=chat_id,
                                                         language="en"))
        self.user_repository.save(user=user)

    def update_user_language_preference(self, chat_id: str,
                                        language: str, ):
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        user.user.language = language
        self.user_repository.save(user=user)

    def retrieve_user_language_preference(self, chat_id: str) -> str:
        user = self.user_repository.find_by_chat_id(chat_id=chat_id)
        if user is not None:
            return user.user.language
        return "en"
