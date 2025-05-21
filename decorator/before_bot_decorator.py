import functools

from configuration.logging_configuration import logger


def __extract_chat_id(message):
    if hasattr(message, "chat"):
        return message.chat.id
    else:
        return message.from_user.id


def log_trigger(func):
    @functools.wraps(func)  # Preserve the original function's name and docstring
    def wrapper(*args, **kwargs):
        # Get the name of the method
        method_name = func.__name__

        # Get the first argument if it exists
        message = args[0] if len(args) > 0 else None

        # Log the method name and the first argument
        logger.info(f"User `{__extract_chat_id(message)}` triggered method : `{method_name}`")

        # Call the original function
        return func(*args, **kwargs)

    return wrapper
