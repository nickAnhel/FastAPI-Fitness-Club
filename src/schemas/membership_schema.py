from pydantic import FutureDate

from .base_schema import BaseChema
from .tariff_schema import TariffGet, TariffPeriod


class MembershipCreate(BaseChema):
    user_id: int
    office_id: int
    start_date: FutureDate


class MembershipCreateWithPeriod(MembershipCreate):
    period: TariffPeriod


class MembershipGet(MembershipCreate):
    id: int
    tariff: TariffGet
