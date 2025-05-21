class MessageUtil:
    def extract_user_name(self, message):
        if hasattr(message.from_user, "first_name"):
            return message.from_user.first_name
        elif hasattr(message.from_user, "username"):
            return message.from_user.username
        else:
            return "there"
