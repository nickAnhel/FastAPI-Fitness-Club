from repositories.user_repository import user_repository
from schemas.user_schema import UserCreate, UserGet, UserUpdateEmail, UserUpdatePhoneNumber


class UserService:
    def create_user(self, data: UserCreate) -> UserGet:
        return UserGet.model_validate(user_repository.create(data))

    def get_users(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ):
        return [
            UserGet.model_validate(user) for user in user_repository.get_all(order=order, limit=limit, offset=offset)
        ]

    def get_user_by_id(self, pk: int):
        return UserGet.model_validate(user_repository.get_single(id=pk))

    def get_user_by_email(self, email: str):
        return UserGet.model_validate(user_repository.get_single(email=email))

    def change_user_email(self, pk: int, email: str):
        return UserGet.model_validate(user_repository.update(data=UserUpdateEmail.model_validate({"email": email}), id=pk))

    def change_user_phone_number(self, pk: int, phone_number: str):
        return UserGet.model_validate(
            user_repository.update(data=UserUpdatePhoneNumber(phone_number=phone_number), id=pk)
        )

    def delete_user_by_id(self, pk: int):
        return user_repository.delete(id=pk)


user_service = UserService()
