from flask import Blueprint, render_template
from flask_login import login_required

from app import db
from app.access import group_required
from app.services.manager_service import ManagerService


bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.get("/orders")
@login_required
@group_required
def orders():
    service = ManagerService(db.session)
    orders = service.get_orders()

    return render_template("manager/orders.html", orders=orders)