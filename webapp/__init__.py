from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

from webapp.models import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.event.forms import SearchForm
from webapp.event.views import blueprint as event_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app():  # Initialize the core application
    app = Flask(__name__)
    mail = Mail(app)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    mail.init_app(app)

    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(event_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader 
    def load_user(user_id):
        return User.query.get(user_id)

    return app
