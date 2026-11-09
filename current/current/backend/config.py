"""
Module: config.py
Description: Centralized backend configuration loading environment variables.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Search for .env in current folder, backend folder, and root
basedir = os.path.abspath(os.path.dirname(__file__))
rootdir = os.path.abspath(os.path.join(basedir, ".."))

load_dotenv(os.path.join(basedir, ".env"))
load_dotenv(os.path.join(rootdir, ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fakenews-super-secret-key-mca-2025")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fakenews-jwt-super-secret-key-2025")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "24")))

    # Admin Enrollment Secret
    ADMIN_REGISTRATION_SECRET = os.getenv("ADMIN_REGISTRATION_SECRET", "AdminSecretPasscode2025!")

    # Database Configuration
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "fake_news_detection")
    USE_SQLITE_FALLBACK = os.getenv("USE_SQLITE_FALLBACK", "false").lower() in ("true", "1", "yes")

    if USE_SQLITE_FALLBACK:
        sqlite_path = os.path.join(basedir, "fake_news_dev.db").replace("\\", "/")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"
    else:
        # Default MySQL connection via PyMySQL
        if DB_PASSWORD:
            SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
        else:
            SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # File Uploads
    UPLOAD_FOLDER = os.path.join(basedir, "uploads")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(10 * 1024 * 1024))) # 10MB
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "csv"}

    # ML Model Artifacts
    ACTIVE_MODEL_PATH = os.path.join(rootdir, os.getenv("ACTIVE_MODEL_PATH", "trained_models/fake_news_model.pkl"))
    ACTIVE_VECTORIZER_PATH = os.path.join(rootdir, os.getenv("ACTIVE_VECTORIZER_PATH", "trained_models/tfidf_vectorizer.pkl"))
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))

    # CORS
    CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")]
