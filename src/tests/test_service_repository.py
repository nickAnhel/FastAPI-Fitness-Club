import pytest
from sqlalchemy import create_engine

from ..models.base_model import Base
from ..models.models import ServiceType
from ..repositories.service_repository import service_repository
from ..schemas.service_schemas import ServiceCreate


@pytest.fixture
def clear_db():
    engine = create_engine("sqlite:///db.sqlite3", echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_service_create_get_all(clear_db):
    service_repository.create_all()
    services = service_repository.get_all()

    assert len(services) == len(ServiceType)
    assert services[0].service_type == ServiceType.GYM
    assert services[1].service_type == ServiceType.POOL
    assert services[2].service_type == ServiceType.SAUNA
    assert services[3].service_type == ServiceType.YOGA
    assert services[4].service_type == ServiceType.CROSSFIT


def test_service_create(clear_db):
    service = service_repository.create(
        data=ServiceCreate(service_type=ServiceType.GYM),
    )
    assert service.service_type == ServiceType.GYM


def test_user_get_single(clear_db):
    service_repository.create(data=ServiceCreate(service_type=ServiceType.GYM))
    service = service_repository.get_single(id=1)
    assert service.service_type == ServiceType.GYM


def test_service_delete(clear_db):
    service_repository.create(
        data=ServiceCreate(service_type=ServiceType.GYM),
    )

    services = service_repository.get_all()
    assert len(services) == 1

    service_repository.delete(id=1)

    services = service_repository.get_all()
    assert len(services) == 0
