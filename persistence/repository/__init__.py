from configuration import mongodb_bean
from persistence.repository.user_repository import UserRepository

user_repository_bean = UserRepository(database=mongodb_bean)
