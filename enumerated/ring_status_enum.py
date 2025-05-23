from enum import Enum


class RingStatusEnum(Enum):
    """
    Enum for the status of the ring.
    """
    INSERTED = (1000, "Inserted", "enum.ring.inserted")
    REMOVED = (2000, "Removed", "enum.ring.removed")

    def __init__(self, code: int,
                 enum_name: str,
                 i18n_key: str):
        self.code = code
        self.enum_name = enum_name
        self.i18n_key = i18n_key

    @classmethod
    def get_by_code(cls, code: int):
        """Return the enum member by its code, or None if not found."""
        for member in cls:
            if member.code == code:
                return member
        return None
