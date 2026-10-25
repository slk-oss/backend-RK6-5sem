from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.database import db

login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    

    app.config.from_object("config.config.Config")

    db.init_app(app)

    csrf.init_app(app)

    login_manager.init_app(app)
    

    login_manager.login_view = "auth.login_page"
    login_manager.login_message = "Пожалуйста, войдите в аккаунт, чтобы продолжить."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))

    with app.app_context():
        from app.models.user import User
        from app.models.order import Order
        from app.models.order_item import OrderItem
        from app.models.product import Product

    from app.routes.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.main_routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.product_routes import bp as products_bp
    app.register_blueprint(products_bp)

    return app