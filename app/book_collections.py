from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from .extensions import db
from .models import Book, Collection
from .permissions import USER, role_required


collections_bp = Blueprint("collections", __name__, url_prefix="/collections")


@collections_bp.get("/")
@role_required(USER)
def index():
    collections = Collection.query.filter_by(user_id=current_user.id).order_by(Collection.title).all()
    return render_template("collections/index.html", collections=collections)


@collections_bp.post("/")
@role_required(USER)
def create():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Введите название подборки", "danger")
        return redirect(url_for("collections.index"))

    exists = Collection.query.filter_by(user_id=current_user.id, title=title).first()
    if exists:
        flash("Подборка с таким названием уже существует", "warning")
        return redirect(url_for("collections.index"))

    collection = Collection(title=title, user=current_user)
    db.session.add(collection)
    db.session.commit()
    flash("Подборка успешно добавлена", "success")
    return redirect(url_for("collections.index"))


@collections_bp.get("/<int:collection_id>")
@role_required(USER)
def show(collection_id):
    collection = Collection.query.filter_by(id=collection_id, user_id=current_user.id).first_or_404()
    return render_template("collections/show.html", collection=collection)


@collections_bp.post("/<int:collection_id>/books/<int:book_id>")
@role_required(USER)
def add_book(collection_id, book_id):
    collection = Collection.query.filter_by(id=collection_id, user_id=current_user.id).first_or_404()
    book = Book.query.get_or_404(book_id)

    if book not in collection.books:
        collection.books.append(book)
        db.session.commit()
        flash("Книга успешно добавлена в подборку", "success")
    else:
        flash("Эта книга уже есть в выбранной подборке", "warning")

    return redirect(url_for("books.show", book_id=book.id))
