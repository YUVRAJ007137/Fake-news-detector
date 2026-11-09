"""
Module: models.py
Description: SQLAlchemy ORM models matching the 11 MySQL schema tables.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user", index=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    predictions = db.relationship("PredictionHistory", backref="user", lazy=True, cascade="all, delete-orphan")
    saved_articles = db.relationship("SavedNews", backref="user", lazy=True, cascade="all, delete-orphan")
    uploaded_files = db.relationship("UploadedFile", backref="user", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "username": self.username,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("admin_record", uselist=False))

class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    article = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default="General", index=True)
    source = db.Column(db.String(255), default="User Input")
    content_hash = db.Column(db.String(64), unique=True, nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    predictions = db.relationship("PredictionHistory", backref="news", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "article": self.article,
            "category": self.category,
            "source": self.source,
            "content_hash": self.content_hash,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    news_id = db.Column(db.Integer, db.ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    prediction_label = db.Column(db.String(20), nullable=False, index=True) # 'FAKE', 'REAL', 'INCONCLUSIVE'
    confidence_score = db.Column(db.Float, nullable=False)
    model_version = db.Column(db.String(50), nullable=False, default="v1.0.0")
    analysis_type = db.Column(db.String(50), nullable=False) # 'ml_previous', 'gemini_latest', 'file_batch'
    prediction_source = db.Column(db.String(50), nullable=False, default="web_ui")
    result_status = db.Column(db.String(50), nullable=False, default="COMPLETED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    gemini_verification = db.relationship("GeminiVerification", backref="prediction", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "news_id": self.news_id,
            "news_title": self.news.title if self.news else "",
            "news_article": self.news.article if self.news else "",
            "category": self.news.category if self.news else "General",
            "source": self.news.source if self.news else "Unknown",
            "prediction_label": self.prediction_label,
            "confidence_score": round(self.confidence_score, 4),
            "model_version": self.model_version,
            "analysis_type": self.analysis_type,
            "prediction_source": self.prediction_source,
            "result_status": self.result_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "gemini_verification": self.gemini_verification.to_dict() if self.gemini_verification else None
        }

class SavedNews(db.Model):
    __tablename__ = "saved_news"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    news_id = db.Column(db.Integer, db.ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    news = db.relationship("News", backref="saved_instances")
    __table_args__ = (db.UniqueConstraint("user_id", "news_id", name="uq_user_news_saved"),)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "news_id": self.news_id,
            "title": self.news.title if self.news else "",
            "article": self.news.article if self.news else "",
            "category": self.news.category if self.news else "",
            "source": self.news.source if self.news else "",
            "saved_at": self.created_at.isoformat() if self.created_at else None
        }

class UploadedFile(db.Model):
    __tablename__ = "uploaded_files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False) # 'pdf', 'docx', 'txt', 'csv'
    analysis_mode = db.Column(db.String(50), nullable=False) # 'ml_previous', 'gemini_latest'
    processing_status = db.Column(db.String(50), nullable=False, default="COMPLETED")
    records_count = db.Column(db.Integer, nullable=False, default=1)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "original_filename": self.original_filename,
            "file_type": self.file_type,
            "analysis_mode": self.analysis_mode,
            "processing_status": self.processing_status,
            "records_count": self.records_count,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }

class Dataset(db.Model):
    __tablename__ = "datasets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataset_name = db.Column(db.String(150), nullable=False)
    dataset_type = db.Column(db.String(50), nullable=False, index=True) # 'self_generated', 'kaggle', 'hybrid'
    file_path = db.Column(db.String(255), nullable=False)
    record_count = db.Column(db.Integer, nullable=False, default=0)
    dataset_version = db.Column(db.String(50), nullable=False, default="v1.0.0")
    status = db.Column(db.String(50), nullable=False, default="ACTIVE")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "dataset_name": self.dataset_name,
            "dataset_type": self.dataset_type,
            "file_path": self.file_path,
            "record_count": self.record_count,
            "dataset_version": self.dataset_version,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class GeminiVerification(db.Model):
    __tablename__ = "gemini_verification"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prediction_history_id = db.Column(db.Integer, db.ForeignKey("prediction_history.id", ondelete="CASCADE"), unique=True, nullable=False)
    assessment = db.Column(db.String(50), nullable=False) # 'FAKE', 'REAL', 'UNVERIFIED', 'INCONCLUSIVE'
    confidence_score = db.Column(db.Float, nullable=True)
    evidence_summary = db.Column(db.Text, nullable=True)
    sources_json = db.Column(db.JSON, nullable=True)
    agreement_status = db.Column(db.String(50), nullable=False) # 'AGREE', 'DISAGREE', 'INCONCLUSIVE'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "prediction_history_id": self.prediction_history_id,
            "assessment": self.assessment,
            "confidence_score": self.confidence_score,
            "evidence_summary": self.evidence_summary,
            "sources": self.sources_json if self.sources_json else [],
            "agreement_status": self.agreement_status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class ModelVersion(db.Model):
    __tablename__ = "model_versions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    version_name = db.Column(db.String(100), unique=True, nullable=False)
    model_path = db.Column(db.String(255), nullable=False)
    vectorizer_path = db.Column(db.String(255), nullable=False)
    training_dataset_version = db.Column(db.String(50), nullable=False)
    evaluation_metrics_json = db.Column(db.JSON, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "version_name": self.version_name,
            "model_path": self.model_path,
            "vectorizer_path": self.vectorizer_path,
            "training_dataset_version": self.training_dataset_version,
            "evaluation_metrics": self.evaluation_metrics_json,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class TrainingLog(db.Model):
    __tablename__ = "training_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataset_version = db.Column(db.String(50), nullable=False)
    model_version = db.Column(db.String(100), nullable=False)
    training_status = db.Column(db.String(50), nullable=False) # 'RUNNING', 'COMPLETED', 'FAILED'
    metrics_json = db.Column(db.JSON, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "dataset_version": self.dataset_version,
            "model_version": self.model_version,
            "training_status": self.training_status,
            "metrics": self.metrics_json,
            "error_message": self.error_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class AdminLog(db.Model):
    __tablename__ = "admin_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action = db.Column(db.String(150), nullable=False)
    target_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin_user = db.relationship("User", backref="performed_admin_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "admin_name": self.admin_user.full_name if self.admin_user else "Admin",
            "action": self.action,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
