CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL UNIQUE,
    description TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    middle_name VARCHAR(64),
    role_id INT NOT NULL,
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE genres (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE covers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(128) NOT NULL,
    md5_hash VARCHAR(32) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    short_description TEXT NOT NULL,
    year YEAR NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    pages INT NOT NULL,
    cover_id INT NOT NULL,
    CONSTRAINT fk_books_cover FOREIGN KEY (cover_id) REFERENCES covers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE book_genres (
    book_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (book_id, genre_id),
    CONSTRAINT fk_book_genres_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    CONSTRAINT fk_book_genres_genre FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_reviews_book_user (book_id, user_id),
    CONSTRAINT fk_reviews_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_reviews_rating CHECK (rating BETWEEN 0 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE collections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    UNIQUE KEY uq_collections_title_user (title, user_id),
    CONSTRAINT fk_collections_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE collection_books (
    collection_id INT NOT NULL,
    book_id INT NOT NULL,
    PRIMARY KEY (collection_id, book_id),
    CONSTRAINT fk_collection_books_collection FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE,
    CONSTRAINT fk_collection_books_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO roles (id, name, description) VALUES
    (1, 'администратор', 'Полный доступ к системе, включая создание и удаление книг'),
    (2, 'модератор', 'Редактирование книг и модерация рецензий'),
    (3, 'пользователь', 'Создание рецензий');

INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id) VALUES
    ('admin', 'pbkdf2:sha256:600000$k5zQLJXpBWJUkeya$b783d99b6168cd588919ecbde8552539cc309bf5007b3ef470e84ad425415fa2', 'Админов', 'Алексей', 'Петрович', 1),
    ('moderator', 'pbkdf2:sha256:600000$aNW8sYGVFf7TyfnC$d42a2d0dd03decf41b6f0ae51e10b747cea6140a7de70992489ec701271158cd', 'Модеров', 'Мария', 'Игоревна', 2),
    ('reader', 'pbkdf2:sha256:600000$Ql78fcxNPplWKTMR$67eb27852be85ff695b0c829bdf4d56f4a4d8684af44a489ab155558e01b6bb3', 'Читателев', 'Иван', 'Сергеевич', 3);

INSERT INTO genres (name) VALUES
    ('Роман'),
    ('Фантастика'),
    ('Детектив'),
    ('Научная литература'),
    ('Учебная литература'),
    ('Классика');
