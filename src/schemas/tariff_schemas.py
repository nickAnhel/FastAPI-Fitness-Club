import enum
from decimal import Decimal
from pydantic import Field

from .base_schema import BaseChema


class TariffPeriod(enum.IntEnum):
    MONTH = 30
    THREE_MONTHS = 90
    SIX_MONTHS = 180
    YEAR = 365


class TariffCreate(BaseChema):
    period: TariffPeriod
    price: Decimal = Field(max_digits=10, decimal_places=2, gt=0)


class TariffGet(TariffCreate):
    id: int
