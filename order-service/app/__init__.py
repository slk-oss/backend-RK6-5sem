from flask import Flask

from app.database import db
from config.config import Config
from flask_wtf.csrf import CSRFProtect
from redis import Redis

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    csrf.init_app(app)

    app.extensions["redis"] = Redis.from_url(
        app.config["REDIS_URL"],
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
    )

    app = Flask(__name__, static_url_path="/order/static")

    from app.routes.order_route import bp as order_bp

    app.register_blueprint(order_bp)
    return app