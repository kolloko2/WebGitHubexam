import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://std_NNNN_exam:password@std-mysql/std_NNNN_exam?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads/covers")
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

