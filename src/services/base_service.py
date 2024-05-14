from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pk: int):
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, pk: int):
        raise NotImplementedError
