from enum import Enum, auto


class BadgeType(Enum):
    INDIVIDUAL = 'IND'
    PLATFORM = 'PLT'

    @classmethod
    def choices(cls):
        return ((key.name, key.value) for key in cls)
