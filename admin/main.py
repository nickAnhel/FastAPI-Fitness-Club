from flask import Flask, redirect
from flask_admin import Admin
from flask_login import LoginManager

from src.auth.models import UserModel
from src.models.models import MembershipModel, OfficeModel, ServiceModel, TariffModel
from src.config.db_config import session_maker
from src.repositories.user_repository import user_repository
from .views import UserView, ServiceView, OfficeView, TariffView, MembershipView, IndexView
from .auth import auth


app = Flask(__name__)

app.secret_key = "SECRET"
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
app.register_blueprint(auth)


@app.route("/")
def index():
    return redirect("/admin")


admin = Admin(app, name="Fitness Club", template_mode="bootstrap3", index_view=IndexView())

admin.add_view(UserView(UserModel, session_maker(), name="Users", endpoint="users"))
admin.add_view(ServiceView(ServiceModel, session_maker(), name="Services", endpoint="services"))
admin.add_view(OfficeView(OfficeModel, session_maker(), name="Offices", endpoint="offices"))
admin.add_view(MembershipView(MembershipModel, session_maker(), name="Memberships", endpoint="memberships"))
admin.add_view(TariffView(TariffModel, session_maker(), name="Tariffs", endpoint="tariffs"))


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return user_repository.get_single(id=user_id)


if __name__ == "__main__":
    app.run()
