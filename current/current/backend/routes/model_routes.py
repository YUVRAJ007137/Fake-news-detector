"""
Routes: model_routes.py
Description: Administrative endpoints for candidate model retraining, versioning,
             performance metrics, and training run audit trails.
"""

import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.models import db, ModelVersion, TrainingLog, AdminLog
from backend.utils.auth_utils import admin_required, get_current_user
from scripts.train_model import train_and_evaluate

model_bp = Blueprint("model_admin", __name__, url_prefix="/api/admin/models")

@model_bp.route("", methods=["GET"])
@admin_required()
def get_models():
    models = ModelVersion.query.order_by(ModelVersion.created_at.desc()).all()
    return jsonify({
        "total": len(models),
        "models": [m.to_dict() for m in models]
    }), 200

@model_bp.route("/metrics", methods=["GET"])
@admin_required()
def get_model_metrics():
    metadata_path = os.path.join("trained_models", "model_metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data), 200

    # Fallback to DB
    active_m = ModelVersion.query.filter_by(is_active=True).first()
    if active_m:
        return jsonify({
            "model_version": active_m.version_name,
            "champion_metrics": active_m.evaluation_metrics_json
        }), 200

    return jsonify({"error": "No model metadata found."}), 404

@model_bp.route("/train", methods=["POST"])
@admin_required()
def trigger_retraining():
    admin = get_current_user()
    dataset_version = request.json.get("dataset_version", "v1.0.0") if request.json else "v1.0.0"
    candidate_version = f"Calibrated-LinearSVC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Log start
    training_run = TrainingLog(
        dataset_version=dataset_version,
        model_version=candidate_version,
        training_status="RUNNING"
    )
    db.session.add(training_run)
    db.session.commit()

    try:
        metadata = train_and_evaluate()

        # Update training run
        training_run.training_status = "COMPLETED"
        training_run.metrics_json = metadata.get("champion_metrics")
        training_run.completed_at = datetime.utcnow()

        # Check existing active model
        active_model = ModelVersion.query.filter_by(is_active=True).first()
        current_f1 = 0.0
        if active_model and active_model.evaluation_metrics_json:
            current_f1 = float(active_model.evaluation_metrics_json.get("f1_score", 0.0))

        candidate_f1 = float(metadata.get("champion_metrics", {}).get("f1_score", 0.0))

        # Register candidate
        promoted = candidate_f1 >= current_f1
        if promoted and active_model:
            active_model.is_active = False

        new_version = ModelVersion(
            version_name=candidate_version,
            model_path=metadata["artifacts"]["model_path"],
            vectorizer_path=metadata["artifacts"]["vectorizer_path"],
            training_dataset_version=dataset_version,
            evaluation_metrics_json=metadata["champion_metrics"],
            is_active=promoted
        )
        db.session.add(new_version)

        if admin:
            action_desc = f"RETRAINED_MODEL_PROMOTED_{candidate_version}" if promoted else f"RETRAINED_MODEL_CANDIDATE_{candidate_version}"
            log_entry = AdminLog(
                admin_id=admin.id,
                action=action_desc,
                target_type="MODEL",
                target_id=new_version.id
            )
            db.session.add(log_entry)

        db.session.commit()

        return jsonify({
            "message": "Retraining completed successfully.",
            "promoted": promoted,
            "candidate_version": candidate_version,
            "metrics": metadata["champion_metrics"]
        }), 200

    except Exception as e:
        training_run.training_status = "FAILED"
        training_run.error_message = str(e)
        training_run.completed_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"error": f"Retraining failed: {str(e)}"}), 500

@model_bp.route("/training-logs", methods=["GET"])
@admin_required()
def get_training_logs():
    logs = TrainingLog.query.order_by(TrainingLog.started_at.desc()).all()
    return jsonify({
        "total": len(logs),
        "logs": [l.to_dict() for l in logs]
    }), 200
