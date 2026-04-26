from flask import Flask
from flasgger import Swagger
from app.modules.main.route import main_bp
from app.db.db import db


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(main_bp)


def initialize_db(app: Flask):
    with app.app_context():
        try:
            db.init_app(app)
            db.create_all()
        except Exception as e:
            print(f"Warning: Could not initialize database: {e}")
            pass

def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger