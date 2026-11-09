"""
Routes: health_routes.py
Description: Public health check and service readiness endpoint.
"""

import os
from flask import Blueprint, jsonify
from backend.config import Config
from backend.services.gemini_service import GeminiService
from backend.models import db

health_bp = Blueprint("health", __name__, url_prefix="/api/health")

@health_bp.route("", methods=["GET"])
def health_check():
    # Check DB
    db_ok = True
    db_err = None
    try:
        db.session.execute(db.text("SELECT 1"))
    except Exception as e:
        db_ok = False
        db_err = str(e)

    # Check Model Artifacts
    model_ok = os.path.exists(Config.ACTIVE_MODEL_PATH)
    vec_ok = os.path.exists(Config.ACTIVE_VECTORIZER_PATH)

    # Check Gemini
    gemini_configured = GeminiService.is_configured()

    status = "healthy" if db_ok and model_ok and vec_ok else "degraded"

    return jsonify({
        "status": status,
        "database": {
            "status": "connected" if db_ok else "error",
            "type": "sqlite_dev" if Config.USE_SQLITE_FALLBACK else "mysql",
            "error": db_err
        },
        "ml_model": {
            "model_loaded": model_ok,
            "vectorizer_loaded": vec_ok,
            "model_path": Config.ACTIVE_MODEL_PATH
        },
        "gemini_api": {
            "configured": gemini_configured,
            "model": Config.GEMINI_MODEL
        }
    }), 200 if status == "healthy" else 503
