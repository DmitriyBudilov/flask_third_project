from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_login import LoginManager

from app.models import db, Order, Meal, User
from app import configuration

app = Flask(__name__)
app.config.from_object(configuration.Config)

migrate = Migrate(app, db)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

admin = Admin(app)
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(User, db.session))


from app import routes