from flask import redirect
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from wtforms import validators


class IndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated  # and current_user.is_superuser

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/login")


class BaseView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated  # and current_user.is_superuser

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/login")


class UserView(BaseView):
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True

    column_list = ["id", "first_name", "last_name", "email", "is_active", "is_superuser", "is_verified"]
    column_searchable_list = ["first_name", "last_name", "email"]
    column_exclude_list = ("hashed_password",)

    form_args = {
        "first_name": {
            "label": "First Name",
            "validators": [validators.DataRequired()],
        },
        "last_name": {
            "label": "Last Name",
            "validators": [validators.DataRequired()],
        },
        "email": {
            "label": "Email",
            "validators": [validators.Email()],
        },
        "phone_number": {
            "label": "Phone Number",
            "validators": [validators.DataRequired()],
        },
        "hashed_password": {
            "label": "Password",
            "validators": [validators.DataRequired()],
        },
    }


class ServiceView(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    column_list = ["id", "service_type"]
    column_searchable_list = ("service_type",)


class OfficeView(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    column_list = ["id", "address", "phone_number", "services"]
    column_searchable_list = ("address",)


class TariffView(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    column_list = ["id", "name", "price", "period"]

    form_choices = {
        "period": [
            (30, 30),
            (90, 90),
            (180, 180),
            (365, 365),
        ]
    }


class MembershipView(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    column_list = ["id", "user", "office", "tariff", "start_date"]
