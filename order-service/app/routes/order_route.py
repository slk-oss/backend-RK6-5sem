from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from redis.exceptions import RedisError

from app.access import group_required
from app.database import db
from app.services.order_service import CartError, CatalogUnavailable, OrderService

bp = Blueprint("order", __name__, url_prefix="/order")


def _get_service() -> OrderService:
    return OrderService(
        db=db.session,
        redis=current_app.extensions["redis"],
        product_service_url=current_app.config["PRODUCT_SERVICE_URL"],
    )


@bp.get("/<int:order_id>")
@login_required
@group_required
def order_detail(order_id: int):
    order = _get_service().order_repo.get_by_id(order_id)

    if order is None or order.user_id != current_user.user_id:
        abort(404)

    return render_template("orders/detail.html", order=order)


@bp.get("/cart")
@login_required
@group_required
def cart():
    try:
        items = _get_service().get_cart(current_user.user_id)
    except CatalogUnavailable as exc:
        return render_template(
            "orders/cart.html", items=[], total=None, cart_error=str(exc)
        ), 503
    except RedisError:
        current_app.logger.exception("Failed to read cart from Redis")
        return render_template(
            "orders/cart.html",
            items=[],
            total=None,
            cart_error="Корзина временно недоступна.",
        ), 503

    subtotals = [item.subtotal for item in items]
    total = (
        sum(value for value in subtotals if value is not None)
        if all(value is not None for value in subtotals)
        else None
    )
    return render_template("orders/cart.html", items=items, total=total)


@bp.post("/cart/add/<int:product_id>")
@login_required
@group_required
def add_to_cart(product_id: int):
    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        flash("Количество должно быть целым числом.", "error")
        return redirect(url_for("order.cart"), code=303)

    try:
        _get_service().add_to_cart(current_user.user_id, product_id, quantity)
    except CatalogUnavailable as exc:
        abort(503, description=str(exc))
    except CartError as exc:
        flash(str(exc), "error")
    except RedisError:
        current_app.logger.exception("Failed to update cart in Redis")
        abort(503, description="Корзина временно недоступна.")
    else:
        flash("Товар добавлен в корзину.", "success")

    return redirect(url_for("order.cart"), code=303)


@bp.get("/")
@login_required
@group_required
def list_orders():
    orders = _get_service().order_repo.get_by_user(current_user.user_id)
    return render_template("orders/list.html", orders=orders)