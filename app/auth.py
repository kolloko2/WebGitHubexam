from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from .models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(login=request.form.get("login", "").strip()).first()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            flash("Вы успешно вошли в систему", "success")
            return redirect(request.args.get("next") or url_for("books.index"))

        flash("Невозможно аутентифицироваться с указанными логином и паролем", "danger")

    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(request.referrer or url_for("books.index"))

