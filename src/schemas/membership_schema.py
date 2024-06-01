from pydantic import FutureDate, Field

from .base_schema import BaseChema


class MembershipCreate(BaseChema):
    user_id: int
    office_id: int
    start_date: FutureDate
    period: int = Field(default=30, ge=30, le=365)


class MembershipGet(MembershipCreate):
    id: int
