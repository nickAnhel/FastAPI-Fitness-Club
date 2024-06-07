import re
from fastapi import Request


class UserCreateForm:
    def __init__(self, request: Request):
        self.request = request
        self.errors = []
        self.first_name: str | None = None
        self.last_name: str | None = None
        self.email: str | None = None
        self.phone_number: str | None = None
        self.password: str | None = None

    async def load(self):
        form = await self.request.form()
        self.first_name = form.get("first_name")  # type: ignore
        self.last_name = form.get("last_name")  # type: ignore
        self.email = form.get("email")  # type: ignore
        self.phone_number = form.get("phone_number")  # type: ignore
        self.password = form.get("password")  # type: ignore

    def is_valid(self):
        if not re.match(re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"), self.email):  # type: ignore
            self.errors.append("Invalid email")
        if not re.match(re.compile(r"^[+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"), self.phone_number):  # type: ignore
            self.errors.append("Invalid phone number")
        if not self.errors:
            return True
        return False
