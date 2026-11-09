"""
Routes: admin_routes.py
Description: Main administrative system management endpoints for user governance,
             system audits, KPI aggregation, and global prediction telemetry.
"""

from flask import Blueprint, request, jsonify
from backend.models import (
    db, User, Admin, News, PredictionHistory, UploadedFile,
    Dataset, GeminiVerification, ModelVersion, AdminLog
)
from backend.utils.auth_utils import admin_required, get_current_user

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/dashboard", methods=["GET"])
@admin_required()
def get_dashboard_kpis():
    total_users = User.query.filter_by(role="user").count()
    total_admins = User.query.filter_by(role="admin").count()
    total_predictions = PredictionHistory.query.count()
    fake_predictions = PredictionHistory.query.filter_by(prediction_label="FAKE").count()
    real_predictions = PredictionHistory.query.filter_by(prediction_label="REAL").count()
    inconclusive_predictions = PredictionHistory.query.filter(
        ~PredictionHistory.prediction_label.in_(["FAKE", "REAL"])
    ).count()

    total_files = UploadedFile.query.count()
    total_datasets = Dataset.query.count()
    gemini_verifications = GeminiVerification.query.count()

    active_model = ModelVersion.query.filter_by(is_active=True).first()
    active_model_name = active_model.version_name if active_model else "Calibrated-LinearSVC-v1.0.0"
    active_accuracy = 0.9333
    if active_model and active_model.evaluation_metrics_json:
        active_accuracy = active_model.evaluation_metrics_json.get("accuracy", 0.9333)

    recent_preds = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).limit(6).all()

    return jsonify({
        "kpis": {
            "total_users": total_users,
            "total_admins": total_admins,
            "total_predictions": total_predictions,
            "fake_predictions": fake_predictions,
            "real_predictions": real_predictions,
            "inconclusive_predictions": inconclusive_predictions,
            "total_files": total_files,
            "total_datasets": total_datasets,
            "gemini_verifications": gemini_verifications,
            "active_model_name": active_model_name,
            "active_accuracy": round(float(active_accuracy), 4)
        },
        "recent_predictions": [p.to_dict() for p in recent_preds]
    }), 200

@admin_bp.route("/users", methods=["GET"])
@admin_required()
def get_all_users():
    role_filter = request.args.get("role", "").strip()
    query_text = request.args.get("query", "").strip()

    q = User.query
    if role_filter in ("user", "admin"):
        q = q.filter_by(role=role_filter)

    users = q.order_by(User.created_at.desc()).all()
    results = []
    for u in users:
        item = u.to_dict()
        if query_text:
            if query_text.lower() not in item["full_name"].lower() and query_text.lower() not in item["email"].lower():
                continue
        results.append(item)

    return jsonify({
        "total": len(results),
        "users": results
    }), 200

@admin_bp.route("/users/<int:user_id>/status", methods=["PATCH"])
@admin_required()
def toggle_user_status(user_id):
    admin = get_current_user()
    if admin and admin.id == user_id:
        return jsonify({"error": "Administrators cannot deactivate their own active account."}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json() or {}
    new_status = data.get("is_active", not user.is_active)
    user.is_active = bool(new_status)

    log_entry = AdminLog(
        admin_id=admin.id if admin else user_id,
        action=f"TOGGLED_USER_STATUS_ID_{user_id}_TO_{user.is_active}",
        target_type="USER",
        target_id=user_id
    )
    db.session.add(log_entry)
    db.session.commit()

    return jsonify({
        "message": f"User '{user.email}' status updated to {'Active' if user.is_active else 'Deactivated'}.",
        "user": user.to_dict()
    }), 200

@admin_bp.route("/predictions", methods=["GET"])
@admin_required()
def get_all_predictions():
    label_filter = request.args.get("label", "").strip().upper()
    query = PredictionHistory.query
    if label_filter in ("FAKE", "REAL", "INCONCLUSIVE"):
        query = query.filter_by(prediction_label=label_filter)

    records = query.order_by(PredictionHistory.created_at.desc()).all()
    return jsonify({
        "total": len(records),
        "predictions": [r.to_dict() for r in records]
    }), 200

@admin_bp.route("/files", methods=["GET"])
@admin_required()
def get_all_uploaded_files():
    files = UploadedFile.query.order_by(UploadedFile.uploaded_at.desc()).all()
    return jsonify({
        "total": len(files),
        "files": [f.to_dict() for f in files]
    }), 200

@admin_bp.route("/gemini-records", methods=["GET"])
@admin_required()
def get_gemini_records():
    records = GeminiVerification.query.order_by(GeminiVerification.created_at.desc()).all()
    return jsonify({
        "total": len(records),
        "records": [r.to_dict() for r in records]
    }), 200

@admin_bp.route("/logs", methods=["GET"])
@admin_required()
def get_admin_logs():
    logs = AdminLog.query.order_by(AdminLog.created_at.desc()).all()
    return jsonify({
        "total": len(logs),
        "logs": [l.to_dict() for l in logs]
    }), 200
