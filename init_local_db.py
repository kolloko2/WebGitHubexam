from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Genre, Role, User


app = create_app()

with app.app_context():
    db.create_all()

    roles = [
        ("администратор", "Полный доступ к системе, включая создание и удаление книг"),
        ("модератор", "Редактирование книг и модерация рецензий"),
        ("пользователь", "Создание рецензий"),
    ]
    for name, description in roles:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name, description=description))

    genres = ["Роман", "Фантастика", "Детектив", "Научная литература", "Учебная литература", "Классика"]
    for name in genres:
        if not Genre.query.filter_by(name=name).first():
            db.session.add(Genre(name=name))

    db.session.flush()

    users = [
        ("admin", "admin123", "Админов", "Алексей", "Петрович", "администратор"),
        ("moderator", "moder123", "Модеров", "Мария", "Игоревна", "модератор"),
        ("reader", "user123", "Читателев", "Иван", "Сергеевич", "пользователь"),
    ]
    for login, password, last_name, first_name, middle_name, role_name in users:
        if not User.query.filter_by(login=login).first():
            role = Role.query.filter_by(name=role_name).first()
            db.session.add(
                User(
                    login=login,
                    password_hash=generate_password_hash(password, method="pbkdf2:sha256"),
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name,
                    role=role,
                )
            )

    db.session.commit()
    print("Local database is ready.")

