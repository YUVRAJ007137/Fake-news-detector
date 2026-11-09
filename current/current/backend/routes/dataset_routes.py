"""
Routes: dataset_routes.py
Description: Administrative endpoints for dataset upload, validation, and hybrid generation.
"""

import os
import uuid
import pandas as pd
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from backend.models import db, Dataset, AdminLog
from backend.utils.auth_utils import admin_required, get_current_user
from scripts.validate_datasets import validate_csv
from scripts.create_hybrid_dataset import create_hybrid_dataset

dataset_bp = Blueprint("dataset_admin", __name__, url_prefix="/api/admin/datasets")

@dataset_bp.route("", methods=["GET"])
@admin_required()
def get_datasets():
    datasets = Dataset.query.order_by(Dataset.created_at.desc()).all()
    return jsonify({
        "total": len(datasets),
        "datasets": [d.to_dict() for d in datasets]
    }), 200

@dataset_bp.route("/validate", methods=["POST"])
@admin_required()
def validate_dataset():
    data = request.get_json() or {}
    file_path = data.get("file_path")

    if not file_path:
        return jsonify({"error": "file_path is required."}), 400

    report = validate_csv(file_path)
    return jsonify({"report": report}), 200

@dataset_bp.route("/create-hybrid", methods=["POST"])
@admin_required()
def trigger_create_hybrid():
    admin = get_current_user()
    try:
        create_hybrid_dataset()
        hybrid_path = os.path.join("dataset", "hybrid", "hybrid_dataset.csv")
        count = 0
        if os.path.exists(hybrid_path):
            df = pd.read_csv(hybrid_path)
            count = len(df)

        # Update or register dataset entry
        hybrid_rec = Dataset.query.filter_by(dataset_type="hybrid").first()
        if not hybrid_rec:
            hybrid_rec = Dataset(
                dataset_name="Harmonized Hybrid News Dataset",
                dataset_type="hybrid",
                file_path=hybrid_path,
                record_count=count,
                dataset_version="v1.0.0",
                status="ACTIVE"
            )
            db.session.add(hybrid_rec)
        else:
            hybrid_rec.record_count = count

        if admin:
            log_entry = AdminLog(
                admin_id=admin.id,
                action="GENERATED_HYBRID_DATASET",
                target_type="DATASET",
                target_id=hybrid_rec.id if hybrid_rec.id else None
            )
            db.session.add(log_entry)

        db.session.commit()
        return jsonify({
            "message": "Hybrid dataset constructed and validated successfully.",
            "record_count": count,
            "file_path": hybrid_path
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to generate hybrid dataset: {str(e)}"}), 500
