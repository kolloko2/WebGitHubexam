from flask_login import UserMixin

from .extensions import db


book_genres = db.Table(
    "book_genres",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)

collection_books = db.Table(
    "collection_books",
    db.Column("collection_id", db.Integer, db.ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
)


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    role = db.relationship("Role", backref="users")

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(part for part in parts if part)

    @property
    def role_name(self):
        return self.role.name if self.role else ""


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)


class Cover(db.Model):
    __tablename__ = "covers"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(128), nullable=False)
    md5_hash = db.Column(db.String(32), nullable=False, unique=True)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cover_id = db.Column(db.Integer, db.ForeignKey("covers.id", ondelete="CASCADE"), nullable=False)

    cover = db.relationship("Cover")
    genres = db.relationship("Genre", secondary=book_genres, backref="books")
    reviews = db.relationship("Review", back_populates="book", cascade="all, delete-orphan")

    @property
    def average_rating(self):
        if not self.reviews:
            return None
        return sum(review.rating for review in self.reviews) / len(self.reviews)


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    book = db.relationship("Book", back_populates="reviews")
    user = db.relationship("User")

    __table_args__ = (db.UniqueConstraint("book_id", "user_id", name="uq_reviews_book_user"),)


class Collection(db.Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", backref="collections")
    books = db.relationship("Book", secondary=collection_books, backref="collections")

    __table_args__ = (db.UniqueConstraint("title", "user_id", name="uq_collections_title_user"),)
