from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from .extensions import db
from .models import Book, Review
from .permissions import ADMIN, MODERATOR, USER, role_required


reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/books/<int:book_id>/reviews/create", methods=["GET", "POST"])
@role_required(ADMIN, MODERATOR, USER)
def create_review(book_id):
    book = Book.query.get_or_404(book_id)
    existing = Review.query.filter_by(book_id=book.id, user_id=current_user.id).first()
    if existing:
        flash("Вы уже оставили рецензию на эту книгу", "warning")
        return redirect(url_for("books.show", book_id=book.id))

    if request.method == "POST":
        if not request.form.get("text", "").strip():
            flash("Заполните текст рецензии", "danger")
            return render_template("reviews/form.html", book=book)

        try:
            review = Review(
                book=book,
                user=current_user,
                rating=int(request.form["rating"]),
                text=request.form["text"].strip(),
            )
            db.session.add(review)
            db.session.commit()
            flash("Рецензия сохранена", "success")
            return redirect(url_for("books.show", book_id=book.id))
        except Exception:
            db.session.rollback()
            flash("При сохранении рецензии возникла ошибка", "danger")

    return render_template("reviews/form.html", book=book)
