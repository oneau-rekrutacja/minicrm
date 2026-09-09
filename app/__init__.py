"""MiniCRM — uproszczony CRM ofertowy (projekt rekrutacyjny)."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-nie-uzywac-na-produkcji"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///minicrm.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if config:
        app.config.update(config)

    db.init_app(app)

    from app.views import bp

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
