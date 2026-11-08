from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.database import db
from config.config import Config


csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    @app.get("/health")
    def health():
        return {"service": "auth-service", "status": "ok"}

    return app