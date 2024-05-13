from repositories.user_repository import user_repository
from schemas.user_schema import UserCreate, UserGet, UserGetWithMemberships, UserUpdateEmail, UserUpdatePhoneNumber


class UserService:
    def create_user(self, data: UserCreate) -> UserGet:
        return UserGet.model_validate(user_repository.create(data))

    def get_users(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> list[UserGetWithMemberships]:
        return [
            UserGetWithMemberships.model_validate(user) for user in user_repository.get_all(order=order, limit=limit, offset=offset)
        ]

    def get_user_by_id(self, pk: int) -> UserGetWithMemberships:
        return UserGetWithMemberships.model_validate(user_repository.get_single(id=pk))

    def get_user_by_email(self, email: str) -> UserGetWithMemberships:
        return UserGetWithMemberships.model_validate(user_repository.get_single(email=email))

    def change_user_email(self, pk: int, email: str) -> UserGetWithMemberships:
        return UserGetWithMemberships.model_validate(user_repository.update(data=UserUpdateEmail.model_validate({"email": email}), id=pk))

    def change_user_phone_number(self, pk: int, phone_number: str) -> UserGetWithMemberships:
        return UserGetWithMemberships.model_validate(
            user_repository.update(data=UserUpdatePhoneNumber(phone_number=phone_number), id=pk)
        )

    def delete_user_by_id(self, pk: int) -> None:
        return user_repository.delete(id=pk)


user_service = UserService()
