from flask import Blueprint, render_template, redirect, request, flash
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import NoResultFound

from src.repositories.user_repository import user_repository


auth = Blueprint("auth", __name__, template_folder="templates")

argon2_hasher = PasswordHasher()


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = user_repository.get_single(email=email)

        argon2_hasher.verify(user.hashed_password, password)  # type: ignore

        assert user.is_superuser

        login_user(user)
        return redirect("/admin")

    except NoResultFound:
        flash("Invalid credentials. Please try again.")
        return redirect("/login")

    except VerifyMismatchError:
        flash("Invalid password. Please try again.")
        return redirect("/login")

    except AssertionError:
        flash("You are not an admin.")
        return redirect("/login")

    except Exception:
        flash("Something went wrong. Please try again.")
        return redirect("/login")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
