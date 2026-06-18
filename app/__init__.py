from pathlib import Path

from flask import Flask

from .auth import auth_bp
from .book_collections import collections_bp
from .books import books_bp
from .extensions import db, login_manager
from .filters import register_filters
from .models import User
from .reviews import reviews_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("app.default_config.Config")
    app.config.from_pyfile("config.py", silent=True)

    upload_dir = Path(app.root_path).parent / app.config["UPLOAD_FOLDER"]
    upload_dir.mkdir(parents=True, exist_ok=True)
    app.config["UPLOAD_PATH"] = upload_dir

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = (
        "Для выполнения данного действия необходимо пройти процедуру аутентификации"
    )

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    register_filters(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(collections_bp)

    return app
