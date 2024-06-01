import datetime
from decimal import Decimal
import enum
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str | None]

    memberships: Mapped[list["MembershipModel"]] = relationship(  # type: ignore
        back_populates="user",
        cascade="all, delete",
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),  # type: ignore
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),  # type: ignore
        server_onupdate=func.now(),  # type: ignore
    )


class ServiceType(enum.StrEnum):
    GYM = "Gym"
    POOL = "Pool"
    SAUNA = "Sauna"
    YOGA = "Yoga"
    CROSSFIT = "Crossfit"


class ServiceModel(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)

    service_type: Mapped[ServiceType]

    offices: Mapped[list["OfficeModel"]] = relationship(  # type: ignore
        back_populates="services",
        secondary="office_services",
    )


class OfficeModel(Base):
    __tablename__ = "offices"

    id: Mapped[int] = mapped_column(primary_key=True)

    address: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str]

    services: Mapped[list["ServiceModel"]] = relationship(  # type: ignore
        back_populates="offices",
        secondary="office_services",
    )
    memberships: Mapped[list["MembershipModel"]] = relationship(  # type: ignore
        back_populates="office",
        cascade="all, delete",
    )


class OfficeService(Base):
    __tablename__ = "office_services"

    office_id: Mapped[int] = mapped_column(
        ForeignKey("offices.id"),
        primary_key=True,
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id"),
        primary_key=True,
    )


class MembershipModel(Base):
    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(primary_key=True)

    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    office_id: Mapped[int] = mapped_column(ForeignKey("offices.id"))

    tariff: Mapped["TariffModel"] = relationship(
        back_populates="memberships",
    )
    user: Mapped["UserModel"] = relationship(
        back_populates="memberships",
    )
    office: Mapped["OfficeModel"] = relationship(
        back_populates="memberships",
    )

    start_date: Mapped[datetime.datetime]


class TariffModel(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)

    period: Mapped[int]
    price: Mapped[Decimal]

    memberships: Mapped[list["MembershipModel"]] = relationship(
        back_populates="tariff",
    )
