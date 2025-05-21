from enum import Enum


class RingStatusEnum(Enum):
    """
    Enum for the status of the ring.
    """
    INSERTED = (1000, "Inserted")
    REMOVED = (2000, "Removed")

    def __init__(self, code: int, enum_name: str):
        self.code = code
        self.enum_name = enum_name

    @classmethod
    def get_by_code(cls, code: int):
        """Return the enum member by its code, or None if not found."""
        for member in cls:
            if member.code == code:
                return member
        return None
