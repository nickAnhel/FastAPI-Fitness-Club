import datetime
import pytest
from sqlalchemy import create_engine

from ..models.base_model import Base
from ..repositories.user_repository import user_repository
from ..repositories.office_repository import office_repository
from ..repositories.membership_repository import membership_repository
from ..schemas.user_schema import UserCreate
from ..schemas.office_schema import OfficeCreate
from ..schemas.membership_schema import MembershipCreate


@pytest.fixture
def clear_db():
    engine = create_engine("sqlite:///db.sqlite3", echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_membership_create(clear_db):
    user_repository.create(data=UserCreate(first_name="Test", last_name="Testik", email="test@mail.com"))
    office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))

    membership = membership_repository.create(
        data=MembershipCreate(
            user_id=1,
            office_id=1,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
        )
    )

    assert membership.user_id == 1
    assert membership.office_id == 1


def test_membership_get_all(clear_db):
    user_repository.create(data=UserCreate(first_name="Test1", last_name="Testik1", email="test1@mail.com"))
    user_repository.create(data=UserCreate(first_name="Test2", last_name="Testik2", email="test2@mail.com"))
    office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))

    membership_repository.create(
        data=MembershipCreate(
            user_id=1,
            office_id=1,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
        )
    )
    membership_repository.create(
        data=MembershipCreate(
            user_id=2,
            office_id=1,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=60),
        )
    )

    memberships = membership_repository.get_all()
    assert len(memberships) == 2
    assert memberships[0].user_id == 1
    assert memberships[0].office_id == 1
    assert memberships[1].user_id == 2
    assert memberships[1].office_id == 1


def test_membership_get(clear_db):
    user_repository.create(data=UserCreate(first_name="Test", last_name="Testik", email="test@mail.com"))
    office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))

    membership_repository.create(
        data=MembershipCreate(
            user_id=1,
            office_id=1,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
        )
    )

    membership = membership_repository.get_single(id=1)
    assert membership.user_id == 1
    assert membership.office_id == 1


def test_membership_delete(clear_db):
    user_repository.create(data=UserCreate(first_name="Test", last_name="Testik", email="test@mail.com"))
    office_repository.create(data=OfficeCreate(address="Test City, Test st.", phone_number="89998887766"))

    membership_repository.create(
        data=MembershipCreate(
            user_id=1,
            office_id=1,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
        )
    )

    memberships = membership_repository.get_all()
    assert len(memberships) == 1

    membership_repository.delete(id=1)

    memberships = membership_repository.get_all()
    assert len(memberships) == 0
