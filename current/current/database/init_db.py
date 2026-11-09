"""
Script: init_db.py
Description: Bootstraps the database schema, creates tables, and populates seed data
             for users, admins, datasets, and initial models. Supports MySQL and SQLite.
"""

import os
import sys
import json
from werkzeug.security import generate_password_hash

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import Config
from backend.models import (
    db, User, Admin, News, PredictionHistory, SavedNews,
    UploadedFile, Dataset, GeminiVerification, ModelVersion,
    TrainingLog, AdminLog
)
from flask import Flask

def init_database():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        print(f"Connecting to database using URI: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1] if '@' in app.config['SQLALCHEMY_DATABASE_URI'] else app.config['SQLALCHEMY_DATABASE_URI']}")
        try:
            db.create_all()
            print("[SUCCESS] All relational database tables created successfully.")
        except Exception as e:
            print(f"[ERROR] Could not connect to database or create tables: {e}")
            if "mysql" in app.config["SQLALCHEMY_DATABASE_URI"].lower():
                print("\n[TIP] If MySQL is running but requires credentials, configure DB_USER and DB_PASSWORD in backend/.env")
                print("Alternatively, enable USE_SQLITE_FALLBACK=true in backend/.env for instant local operation.")
            sys.exit(1)

        # Seed initial Admin user
        admin_user = User.query.filter_by(email="admin@fakenews.ai").first()
        if not admin_user:
            admin_user = User(
                full_name="System Administrator",
                email="admin@fakenews.ai",
                username="admin",
                password_hash=generate_password_hash("Admin@12345"),
                role="admin",
                is_active=True
            )
            db.session.add(admin_user)
            db.session.flush()

            admin_record = Admin(user_id=admin_user.id)
            db.session.add(admin_record)
            print("[SEED] Created default Admin user: admin@fakenews.ai / Admin@12345")
        else:
            print("[INFO] Admin user already exists.")

        # Seed initial Demo User
        demo_user = User.query.filter_by(email="user@fakenews.ai").first()
        if not demo_user:
            demo_user = User(
                full_name="Research Student",
                email="user@fakenews.ai",
                username="demouser",
                password_hash=generate_password_hash("User@12345"),
                role="user",
                is_active=True
            )
            db.session.add(demo_user)
            print("[SEED] Created default Demo user: user@fakenews.ai / User@12345")
        else:
            print("[INFO] Demo user already exists.")

        # Seed Datasets
        if Dataset.query.count() == 0:
            datasets_to_seed = [
                Dataset(
                    dataset_name="Self-Generated Fake & Real News Dataset",
                    dataset_type="self_generated",
                    file_path="dataset/self_generated/self_generated_news.csv",
                    record_count=660,
                    dataset_version="v2.0.0",
                    status="ACTIVE"
                ),
                Dataset(
                    dataset_name="Kaggle Benchmark Fake News Dataset",
                    dataset_type="kaggle",
                    file_path="dataset/kaggle/kaggle_news.csv",
                    record_count=24,
                    dataset_version="v1.0.0",
                    status="ACTIVE"
                ),
                Dataset(
                    dataset_name="Harmonized Hybrid News Dataset",
                    dataset_type="hybrid",
                    file_path="dataset/hybrid/hybrid_dataset.csv",
                    record_count=684,
                    dataset_version="v2.0.0",
                    status="ACTIVE"
                )
            ]
            db.session.bulk_save_objects(datasets_to_seed)
            print("[SEED] Registered initial datasets.")

        # Seed Active Model Version
        metadata_file = os.path.join("trained_models", "model_metadata.json")
        metrics = {"accuracy": 0.9333, "f1_score": 0.9231, "algorithm": "Calibrated Linear Support Vector Machine"}
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, "r") as f:
                    meta = json.load(f)
                    metrics = meta.get("champion_metrics", metrics)
            except Exception:
                pass

        if ModelVersion.query.count() == 0:
            model_ver = ModelVersion(
                version_name="Calibrated-LinearSVC-v1.0.0",
                model_path="trained_models/fake_news_model.pkl",
                vectorizer_path="trained_models/tfidf_vectorizer.pkl",
                training_dataset_version="v1.0.0",
                evaluation_metrics_json=metrics,
                is_active=True
            )
            db.session.add(model_ver)
            print("[SEED] Registered active champion model version.")

        # Seed Sample News and Prediction
        if News.query.count() == 0:
            news1 = News(
                title="James Webb Space Telescope Directly Images Exoplanetary Atmosphere Containing Carbon Dioxide",
                article="Astronomers analyzing transmission spectroscopy data from the NIRSpec instrument aboard the James Webb Space Telescope have published definitive evidence of carbon dioxide molecules in the upper atmosphere of gas giant WASP-39 b.",
                category="Science",
                source="Nature Astronomy",
                content_hash="jwst_sample_hash_real_news"
            )
            db.session.add(news1)
            db.session.flush()

            pred1 = PredictionHistory(
                user_id=demo_user.id if demo_user else None,
                news_id=news1.id,
                prediction_label="REAL",
                confidence_score=0.964,
                model_version="Calibrated-LinearSVC-v1.0.0",
                analysis_type="ml_previous",
                prediction_source="web_ui",
                result_status="COMPLETED"
            )
            db.session.add(pred1)
            db.session.flush()

            saved1 = SavedNews(
                user_id=demo_user.id if demo_user else None,
                news_id=news1.id
            )
            db.session.add(saved1)

            gemini1 = GeminiVerification(
                prediction_history_id=pred1.id,
                assessment="REAL",
                confidence_score=0.95,
                evidence_summary="Peer-reviewed astrophysical data from Nature Astronomy confirms JWST atmospheric carbon dioxide detection.",
                sources_json=["https://www.nature.com/articles/s41550-023-01909-x"],
                agreement_status="AGREE"
            )
            db.session.add(gemini1)
            print("[SEED] Populated sample news, predictions, and Gemini verification.")

        db.session.commit()
        print("[SUCCESS] Database initialization completed successfully!")

if __name__ == "__main__":
    init_database()
