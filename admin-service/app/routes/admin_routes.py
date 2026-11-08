from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app import db
from app.access import group_required
from app.services.admin_service import AdminService


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/users")
@login_required
@group_required
def users():
    service = AdminService(db.session)
    users = service.get_users()

    return render_template("admin/users.html", users=users)


@bp.post("/users/<int:user_id>/role")
@login_required
@group_required
def change_role(user_id):
    service = AdminService(db.session)

    try:
        service.change_role(
            actor_id=current_user.user_id,
            user_id=user_id,
            role_value=request.form.get("role", ""),
        )

        db.session.commit()
        flash("Роль пользователя изменена.", "success")

    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")

    return redirect(url_for("admin.users"))