import hashlib
from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user
from sqlalchemy import desc, func
from werkzeug.utils import secure_filename

from .extensions import db
from .models import Book, Cover, Genre, Review
from .permissions import ADMIN, MODERATOR, can_create_book, can_delete_book, can_edit_book, role_required


books_bp = Blueprint("books", __name__)


@books_bp.app_context_processor
def inject_permissions():
    return {
        "can_create_book": can_create_book,
        "can_edit_book": can_edit_book,
        "can_delete_book": can_delete_book,
    }


@books_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    books = (
        Book.query.outerjoin(Review)
        .group_by(Book.id)
        .order_by(desc(Book.year), Book.title)
        .paginate(page=page, per_page=10, error_out=False)
    )
    return render_template("books/index.html", books=books)


@books_bp.route("/covers/<path:filename>")
def cover_file(filename):
    return send_from_directory(current_app.config["UPLOAD_PATH"], filename)


@books_bp.route("/books/<int:book_id>")
def show(book_id):
    book = Book.query.get_or_404(book_id)
    user_review = None
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(book_id=book.id, user_id=current_user.id).first()
    return render_template("books/show.html", book=book, user_review=user_review)


@books_bp.route("/books/create", methods=["GET", "POST"])
@role_required(ADMIN)
def create():
    genres = Genre.query.order_by(Genre.name).all()
    if request.method == "POST":
        return save_book(None, genres)
    return render_template("books/form.html", book=None, genres=genres)


@books_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
@role_required(ADMIN, MODERATOR)
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    genres = Genre.query.order_by(Genre.name).all()
    if request.method == "POST":
        return save_book(book, genres)
    return render_template("books/form.html", book=book, genres=genres)


@books_bp.post("/books/<int:book_id>/delete")
@role_required(ADMIN)
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    cover = book.cover
    try:
        db.session.delete(book)
        db.session.commit()
        if cover and not Book.query.filter_by(cover_id=cover.id).first():
            remove_cover_file(cover.filename)
            db.session.delete(cover)
            db.session.commit()
        flash("Книга успешно удалена", "success")
    except Exception:
        db.session.rollback()
        flash("При удалении книги возникла ошибка", "danger")
    return redirect(url_for("books.index"))


def save_book(book, genres):
    form = request.form
    if not form.get("short_description", "").strip():
        flash("Заполните краткое описание книги", "danger")
        return render_template("books/form.html", book=book, genres=genres)

    selected_genres = Genre.query.filter(Genre.id.in_(form.getlist("genres"))).all()
    if not selected_genres:
        flash("Выберите хотя бы один жанр", "danger")
        return render_template("books/form.html", book=book, genres=genres)

    try:
        if book is None:
            cover = save_cover(request.files.get("cover"))
            if cover is None:
                flash("Загрузите обложку книги", "danger")
                return render_template("books/form.html", book=book, genres=genres)
            book = Book(cover=cover)
            db.session.add(book)

        book.title = form["title"].strip()
        book.short_description = form["short_description"].strip()
        book.year = int(form["year"])
        book.publisher = form["publisher"].strip()
        book.author = form["author"].strip()
        book.pages = int(form["pages"])
        book.genres = selected_genres

        db.session.commit()
        flash("Данные книги сохранены", "success")
        return redirect(url_for("books.show", book_id=book.id))
    except Exception:
        db.session.rollback()
        flash("При сохранении данных возникла ошибка. Проверьте корректность введённых данных.", "danger")
        return render_template("books/form.html", book=book, genres=genres)


def save_cover(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    payload = file_storage.read()
    digest = hashlib.md5(payload).hexdigest()
    existing = Cover.query.filter_by(md5_hash=digest).first()
    if existing:
        return existing

    extension = Path(secure_filename(file_storage.filename)).suffix.lower() or ".jpg"
    cover = Cover(filename="pending", mime_type=file_storage.mimetype, md5_hash=digest)
    db.session.add(cover)
    db.session.flush()
    cover.filename = f"{cover.id}{extension}"
    target = current_app.config["UPLOAD_PATH"] / cover.filename
    target.write_bytes(payload)
    return cover


def remove_cover_file(filename):
    path = current_app.config["UPLOAD_PATH"] / filename
    if path.exists():
        path.unlink()
