from ..repositories.user_repository import user_repository
from ..auth.schemas import UserReadWithMemberships, UserUpdateEmail, UserUpdatePhoneNumber
from .base_service import BaseService


class UserService(BaseService):
    # def create(self, data: UserCreate) -> UserRead:
    #     return UserRead.model_validate(user_repository.create(data))

    def get_all(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> list[UserReadWithMemberships]:
        return [
            UserReadWithMemberships.model_validate(user)
            for user in user_repository.get_all(order=order, limit=limit, offset=offset)
        ]

    def get_by_id(self, pk: int) -> UserReadWithMemberships:
        return UserReadWithMemberships.model_validate(user_repository.get_single(id=pk))

    def get_by_email(self, email: str) -> UserReadWithMemberships:
        return UserReadWithMemberships.model_validate(user_repository.get_single(email=email))

    def change_email(self, pk: int, email: str) -> UserReadWithMemberships:
        return UserReadWithMemberships.model_validate(
            user_repository.update(data=UserUpdateEmail.model_validate({"email": email}), id=pk)
        )

    def change_phone_number(self, pk: int, phone_number: str) -> UserReadWithMemberships:
        return UserReadWithMemberships.model_validate(
            user_repository.update(data=UserUpdatePhoneNumber(phone_number=phone_number), id=pk)
        )

    def delete_by_id(self, pk: int) -> None:
        return user_repository.delete(id=pk)


user_service = UserService()
