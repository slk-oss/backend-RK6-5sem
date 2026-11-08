from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from app.services.order_service import OrderService
from app.access import group_required
from app import db

bp = Blueprint('order', __name__, url_prefix='/order')


@bp.route('/<int:order_id>')
@login_required
@group_required
def order_detail(order_id):
    service = OrderService(db.session)
    order = service.order_repo.get_by_id(order_id)

    if not order or order.user_id != current_user.user_id:
        flash('Заказ не найден.', 'error')
        return redirect(url_for('main.index'))

    return render_template('orders/detail.html', order=order)


@bp.route('/cart', methods=['GET'])
@login_required
@group_required
def cart():
    service = OrderService(db.session)
    cart = service.get_or_create_cart(user_id=current_user.user_id)
    db.session.commit()

    total = service.get_cart_total(cart.order_id)
    return render_template('orders/cart.html', cart=cart, total=total)


@bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
@group_required
def add_to_cart(product_id):
    service = OrderService(db.session)
    try:
        quantity = int(request.form.get('quantity', 1))
        service.add_to_cart(
            user_id=current_user.user_id,
            product_id=product_id,
            quantity=quantity,
        )
        db.session.commit()
        flash('Товар добавлен в корзину', 'success')
    except ValueError as e:
        db.session.rollback()
        flash(str(e), 'error')
    return redirect(url_for('order.cart'))

@bp.route('/', methods=['GET'])
@login_required
@group_required
def list_orders():
    service = OrderService(db.session)
    orders = service.order_repo.get_by_user(current_user.user_id)
    return render_template('orders/list.html', orders=orders)
