from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config, make_driver_dict

db = SQLAlchemy()
driver_dict = make_driver_dict()
working_drivers = []


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from VahanApp.VahanFlaskSelenium.model import Cookies, SearchCount

    with app.app_context():
        from VahanApp.VahanFlaskSelenium import api

        # initializing app
        api.init_app(app)
        db.init_app(app)

    return app
