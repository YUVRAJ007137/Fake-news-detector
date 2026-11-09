from .auth_routes import auth_bp
from .admin_auth_routes import admin_auth_bp
from .news_routes import news_bp
from .file_routes import file_bp
from .dataset_routes import dataset_bp
from .model_routes import model_bp
from .admin_routes import admin_bp
from .health_routes import health_bp

__all__ = [
    "auth_bp",
    "admin_auth_bp",
    "news_bp",
    "file_bp",
    "dataset_bp",
    "model_bp",
    "admin_bp",
    "health_bp"
]
