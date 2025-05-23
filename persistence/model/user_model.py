from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserInformation(BaseModel):
    """
    User information model.
    """
    username: str
    chat_id: int
    date_of_birth: Optional[datetime] = None
    language: Optional[str] = None


class RingInformation(BaseModel):
    """
    Ring information.
    """
    ring_date: Optional[str] = None  # Formatted string like "YYYY-MM-DD"
    ring_insertion_time: Optional[str] = None  # Formatted string like "HH:MM"
    ring_status: Optional[int] = None


class TimeZoneInformation(BaseModel):
    """
    Time zone information.
    """
    time_zone: Optional[str] = None  # e.g. "Europe/Rome"
    time_offset: Optional[int] = None  # e.g. 3600 for UTC+1
    time_offset_str: Optional[str] = None  # e.g. "+01:00"


class UserModel(BaseModel):
    """
    User model for MongoDB.
    """
    id: Optional[str] = Field(None, alias="_id")
    user: Optional[UserInformation] = None
    ring: Optional[RingInformation] = None
