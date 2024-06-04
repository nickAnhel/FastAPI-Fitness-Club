from abc import ABC, abstractmethod
from sqlalchemy.orm import Session, sessionmaker


class BaseRepository(ABC):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_single(self, **filters):
        raise NotImplementedError

    def update(self, data, **filters):
        raise NotImplementedError

    @abstractmethod
    def delete(self, **filters):
        raise NotImplementedError
