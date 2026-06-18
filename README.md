# Электронная библиотека

Экзаменационный Flask-проект: CRUD книг, аутентификация, авторизация по ролям, рецензии, загрузка обложек и Markdown-описания.

## Запуск локально

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy config.example.py config.py
flask --app app run --debug --port 5051
```

В `config.py` укажите параметры MySQL. Для университета имя БД обычно `std_NNNN_exam`.
Если `config.py` не создан, проект запускается локально на SQLite.

## Демо-пользователи из `seed.sql`

- `admin` / `admin123` — администратор
- `moderator` / `moder123` — модератор
- `reader` / `user123` — пользователь

Автор: группа 241-372, Кодзаев Николай Петрович.

