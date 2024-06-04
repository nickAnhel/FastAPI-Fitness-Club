import pytest
from sqlalchemy import create_engine

from ..models.base_model import Base
from ..repositories.user_repository import user_repository
from ..schemas.user_schemas import UserCreate, UserUpdateEmail, UserUpdatePhoneNumber


@pytest.fixture
def clear_db():
    engine = create_engine("sqlite:///db.sqlite3", echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_user_create(clear_db):
    user = user_repository.create(
        data=UserCreate(**{"first_name": "Test", "last_name": "Testik", "email": "test@mail.com"})
    )
    assert user.first_name == "Test"
    assert user.last_name == "Testik"
    assert user.email == "test@mail.com"


def test_user_get_all(clear_db):
    user_repository.create(data=UserCreate(first_name="Test1", last_name="Testik1", email="test1@mail.com"))
    user_repository.create(data=UserCreate(first_name="Test2", last_name="Testik2", email="test2@mail.com"))

    users = user_repository.get_all()
    assert len(users) == 2

    assert users[0].first_name == "Test1"
    assert users[0].last_name == "Testik1"
    assert users[0].email == "test1@mail.com"

    assert users[1].first_name == "Test2"
    assert users[1].last_name == "Testik2"
    assert users[1].email == "test2@mail.com"


def test_user_get_single(clear_db):
    user_repository.create(data=UserCreate(first_name="Test", last_name="Testik", email="test@mail.com"))

    user = user_repository.get_single(id=1)
    assert user.first_name == "Test"
    assert user.last_name == "Testik"
    assert user.email == "test@mail.com"


def test_user_update_email(clear_db):
    user = user_repository.create(data=UserCreate(first_name="Test", last_name="Testik", email="test@mail.com"))

    user_repository.update(
        data=UserUpdateEmail(email="changed_test@mail.com"),
        id=user.id,
    )

    user = user_repository.get_single(id=user.id)
    assert user.email == "changed_test@mail.com"


def test_user_update_phone_number(clear_db):
    user = user_repository.create(
        data=UserCreate(first_name="Test", last_name="Testik", email="test@mail.com", phone_number="89998887766")
    )

    user_repository.update(
        data=UserUpdatePhoneNumber(phone_number="87776665544"),
        id=user.id,
    )

    user = user_repository.get_single(id=user.id)
    assert user.phone_number == "87776665544"


def test_user_delete(clear_db):
    user = user_repository.create(data=UserCreate(first_name="Test", last_name="Testik", email="test@mail.com"))

    users = user_repository.get_all()
    assert len(users) == 1

    user_repository.delete(id=user.id)
    users = user_repository.get_all()
    assert len(users) == 0
