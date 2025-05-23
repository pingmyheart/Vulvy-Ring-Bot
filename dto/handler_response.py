from pydantic import BaseModel
from telebot.types import InlineKeyboardMarkup


class HandlerResponse(BaseModel):
    """
    Handler response model.
    """
    text: str
    markup: InlineKeyboardMarkup | None = None
