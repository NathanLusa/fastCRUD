import enum


class AccountTypeEnum(enum.IntEnum):
    CHECKING_ACCOUNT = 0
    SAVING_ACCOUNT = 1
    CREDIT_CARD = 2
    INVESTMENT_ACCOUNT = 3


class AccountStatusEnum(enum.IntEnum):
    PENDING = 0
    OPENED = 1
    CLOSED = 2
    BLOQUED = 3
