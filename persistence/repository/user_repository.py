import uuid
from typing import List

from persistence.model.user_model import UserModel


class UserRepository:
    def __init__(self, database):
        self.database = database["user_collection"]

    def save(self, user: UserModel):
        """
        Insert a user into the database.
        """
        temp: UserModel = self.find_by_chat_id(user.user.chat_id)
        if temp is None:
            temp = self.find_by_username(user.user.username)
        if temp is not None:
            user.id = temp.id
        else:
            user.id = uuid.uuid4().__str__()
        user_dict = user.model_dump(by_alias=True)

        if temp is not None:
            self.database.update_one({"_id": temp.id}, {"$set": user_dict})
        else:
            self.database.insert_one(user_dict)

    def find_by_username(self, username: str) -> UserModel | None:
        """
        Find a user by username.
        """
        user = self.database.find_one({"user.username": username})
        if user:
            return UserModel.model_validate(user)
        return None

    def find_by_chat_id(self, chat_id: int) -> UserModel | None:
        """
        Find a user by chat_id.
        """
        user = self.database.find_one({"user.chat_id": chat_id})
        if user:
            return UserModel.model_validate(user)
        return None

    def find_all(self) -> List[UserModel]:
        """
        Find all users inside the database
        :return: List of UserModel
        """
        return [UserModel.model_validate(model) for model in self.database.find()]

    def find_all_by_birth_day_and_month(self, day: int,
                                        month: int) -> List[UserModel]:
        """
        Find all users with a birthday on the specified day and month.
        """
        return [UserModel.model_validate(model) for model in
                self.database.find({"user.date_of_birth": {"$regex": f".*{month:02d}-{day:02d}"}})]
