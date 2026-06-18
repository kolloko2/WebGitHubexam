from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


ADMIN = "администратор"
MODERATOR = "модератор"
USER = "пользователь"


def has_role(*roles):
    return current_user.is_authenticated and current_user.role_name in roles


def can_create_book():
    return has_role(ADMIN)


def can_edit_book():
    return has_role(ADMIN, MODERATOR)


def can_delete_book():
    return has_role(ADMIN)


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Для выполнения данного действия необходимо пройти процедуру аутентификации", "warning")
                return redirect(url_for("auth.login"))
            if not has_role(*roles):
                flash("У вас недостаточно прав для выполнения данного действия", "danger")
                return redirect(url_for("books.index"))
            return view(*args, **kwargs)

        return wrapper

    return decorator

