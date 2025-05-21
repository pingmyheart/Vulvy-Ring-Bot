from persistence import user_repository_bean
from service.user_service import UserService

user_service_bean = UserService(user_repository=user_repository_bean)
