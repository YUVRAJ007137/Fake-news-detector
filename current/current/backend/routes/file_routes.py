"""
Routes: file_routes.py
Description: Endpoints for uploading and analyzing news documents (PDF, DOCX, TXT, CSV).
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, UploadedFile, PredictionHistory, News
from backend.services.file_service import FileService
from backend.utils.auth_utils import get_current_user

file_bp = Blueprint("files", __name__, url_prefix="/api/files")

@file_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file payload found in the request."}), 400

    file_obj = request.files["file"]
    if file_obj.filename == "":
        return jsonify({"error": "Empty filename submitted."}), 400

    analysis_mode = request.form.get("analysis_mode", "ml_previous").strip()
    if analysis_mode not in ("ml_previous", "gemini_latest"):
        analysis_mode = "ml_previous"

    current_user = get_current_user()
    user_id = current_user.id if current_user else None

    try:
        # Save file securely
        original_name, stored_filename, full_path = FileService.save_upload(file_obj)
        file_ext = FileService.get_extension(original_name)

        # Process document
        process_res = FileService.process_document(
            file_path=full_path,
            file_type=file_ext,
            analysis_mode=analysis_mode
        )

        records_count = process_res.get("records_count", 1)

        # Record in uploaded_files
        upload_entry = UploadedFile(
            user_id=user_id,
            original_filename=original_name,
            stored_filename=stored_filename,
            file_type=file_ext,
            analysis_mode=analysis_mode,
            processing_status="COMPLETED" if "error" not in process_res else "ERROR",
            records_count=records_count
        )
        db.session.add(upload_entry)
        db.session.flush()

        # If single article document, persist to News & PredictionHistory
        if not process_res.get("is_batch") and "title" in process_res:
            content_hash = PredictionService.compute_content_hash(process_res["title"], process_res["article"])
            news_entry = News.query.filter_by(content_hash=content_hash).first()
            if not news_entry:
                news_entry = News(
                    title=process_res["title"],
                    article=process_res["article"],
                    category="Document Upload",
                    source=f"File: {original_name}",
                    content_hash=content_hash
                )
                db.session.add(news_entry)
                db.session.flush()

            pred_entry = PredictionHistory(
                user_id=user_id,
                news_id=news_entry.id,
                prediction_label=process_res.get("overall_decision", "INCONCLUSIVE"),
                confidence_score=process_res.get("confidence_score", 0.50),
                model_version=process_res.get("model_version", "v1.0.0"),
                analysis_type=f"file_{file_ext}",
                prediction_source=f"upload:{original_name}",
                result_status="COMPLETED"
            )
            db.session.add(pred_entry)

        db.session.commit()

        return jsonify({
            "message": f"Successfully processed '{original_name}'.",
            "file_id": upload_entry.id,
            "filename": original_name,
            "file_type": file_ext,
            "analysis_mode": analysis_mode,
            "result": process_res
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Document processing failed: {str(e)}"}), 500

@file_bp.route("/history", methods=["GET"])
@jwt_required()
def get_upload_history():
    user_id = int(get_jwt_identity())
    uploads = UploadedFile.query.filter_by(user_id=user_id).order_by(UploadedFile.uploaded_at.desc()).all()
    return jsonify({
        "total": len(uploads),
        "uploads": [u.to_dict() for u in uploads]
    }), 200
