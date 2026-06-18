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

