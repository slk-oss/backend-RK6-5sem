from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.database import db
from config.config import Config

from redis import Redis

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, static_url_path="/products/static")

    app.config.from_object(Config)

    app.extensions["redis"] = Redis.from_url(
        app.config["REDIS_URL"],
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
    )

    db.init_app(app)
    csrf.init_app(app)

    from app.routes.product_routes import bp as product_bp
    app.register_blueprint(product_bp)

    
    return app