import datetime

from .base_schema import BaseChema


class MembershipCreate(BaseChema):
    user_id: int
    office_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime


class MembershipGet(MembershipCreate):
    id: int
