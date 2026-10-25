from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.services.auth_service import (
    AuthService,
    AuthError,
    WeakPassword,
    EmailAlreadyRegistered,
    InvalidCredentials,
)

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/register")
def register_page():
    return render_template("auth/register.html")


@bp.post("/register")
def register_action():
    try:
        user = AuthService().register(
            email=request.form["email"],
            password=request.form["password"],
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
        )
    except WeakPassword as e:
        flash(str(e), "error")
        return render_template("auth/register.html"), 400
    except EmailAlreadyRegistered as e:
        flash(str(e), "error")
        return render_template("auth/register.html"), 400
    except AuthError as e:
        flash(str(e), "error")
        return render_template("auth/register.html"), 400

    login_user(user)
    flash("Аккаунт успешно создан!", "success")
    return redirect(url_for("main.index"))

@bp.get("/login")
def login_page():
    """Показывает пустую форму входа (GET)."""
    return render_template("auth/login.html")


@bp.post("/login")
def login_action():
    try:
        user = AuthService().login(
            email=request.form["email"],
            password=request.form["password"],
        )
    except InvalidCredentials as e:
        flash(str(e), "error")
        return render_template("auth/login.html"), 401
    except AuthError as e:
        flash(str(e), "error")
        return render_template("auth/login.html"), 401

    login_user(user)
    flash("Добро пожаловать!", "success")
    
    next_url = request.args.get("next") or url_for("main.index")
    return redirect(next_url)

@bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("main.index"))