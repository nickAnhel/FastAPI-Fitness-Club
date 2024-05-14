import pytest
from sqlalchemy import create_engine

from ..models.base_model import Base
from ..models.models import ServiceType
from ..repositories.office_repository import office_repository
from ..repositories.service_repository import service_repository
from ..schemas.office_schema import OfficeCreate, OfficeUpdatePhoneNumber
from ..schemas.service_schema import ServiceCreate


@pytest.fixture
def clear_db():
    engine = create_engine("sqlite:///db.sqlite3", echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_office_create(clear_db):
    office = office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))
    assert office.address == "Test City, Test st."
    assert office.phone_number == "89998887766"


def test_office_get_all(clear_db):
    office_repository.create(data=OfficeCreate(address="A City, Test1 st.", phone_number="89998887766"))
    office_repository.create(data=OfficeCreate(address="B City, Test2 st.", phone_number="87776665544"))

    offices = office_repository.get_all()
    assert len(offices) == 2

    assert offices[0].address == "A City, Test1 st."
    assert offices[0].phone_number == "89998887766"
    assert offices[1].address == "B City, Test2 st."
    assert offices[1].phone_number == "87776665544"


def test_office_get(clear_db):
    office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))

    office = office_repository.get_single(id=1)
    assert office.address == "Test City, Test st."
    assert office.phone_number == "89998887766"


def test_office_update_phone_number(clear_db):
    office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))

    office_repository.update(data=OfficeUpdatePhoneNumber(phone_number="87776665544"), id=1)

    office = office_repository.get_single(id=1)
    assert office.phone_number == "87776665544"


def test_office_add_sesrvice(clear_db):
    service_repository.create(data=ServiceCreate(service_type=ServiceType.GYM))
    office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))

    office_repository.add_service(service_type=ServiceType.GYM, id=1)

    office = office_repository.get_single(id=1)

    assert office.services[0].service_type == ServiceType.GYM


def test_office_delete(clear_db):
    office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))

    offices = office_repository.get_all()
    assert len(offices) == 1

    office_repository.delete(id=1)

    offices = office_repository.get_all()
    assert len(offices) == 0
