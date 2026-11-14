from functools import wraps

from flask import abort, request
from flask_login import current_user, login_required


GROUP_ACCESS = {
    'customer': {
        'main.index',
        'products.list_products',
        'products.detail',
        'order.cart',
        'order.add_to_cart',
        'order.order_detail',
        'order.list_orders',
    },

    'manager': {
        'main.index',
        'products.list_products',
        'products.detail',
        'manager.orders',
    },

    'admin': {
        'main.index',
        'products.list_products',
        'products.detail',
        'manager.orders',
        'admin.users',
        'admin.change_role',
    },
}


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        role = current_user.role.value
        endpoint = request.endpoint

        allowed_endpoints = GROUP_ACCESS.get(role, set())

        if endpoint not in allowed_endpoints:
            abort(403)

        return func(*args, **kwargs)

    return login_required(wrapper)