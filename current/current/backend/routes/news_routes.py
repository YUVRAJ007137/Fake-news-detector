"""
Routes: news_routes.py
Description: Endpoints for previous news prediction, latest news analysis with Gemini,
             prediction history browsing, and saved news bookmarks.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, News, PredictionHistory, SavedNews, GeminiVerification
from backend.services.prediction_service import PredictionService
from backend.services.gemini_service import GeminiService
from backend.utils.auth_utils import get_current_user

news_bp = Blueprint("news", __name__, url_prefix="/api/news")

@news_bp.route("/predict", methods=["POST"])
def predict_news():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    article = data.get("article", "").strip()
    category = data.get("category", "General").strip()
    source = data.get("source", "User Input").strip()

    if not title or not article:
        return jsonify({"error": "Both news title and news article body are required."}), 400

    if len(article) < 20:
        return jsonify({"error": "The news article body is too brief to analyze (minimum 20 characters)."}), 400

    current_user = get_current_user()
    user_id = current_user.id if current_user else None

    try:
        # Run inference
        result = PredictionService.predict(title, article, check_cache=True)

        if result.get("is_cached"):
            return jsonify({
                "message": "Found identical previous news prediction in database cache.",
                "result": result
            }), 200

        content_hash = result["content_hash"]

        # Persist News
        news_entry = News.query.filter_by(content_hash=content_hash).first()
        if not news_entry:
            news_entry = News(
                title=title,
                article=article,
                category=category,
                source=source,
                content_hash=content_hash
            )
            db.session.add(news_entry)
            db.session.flush()

        # Persist PredictionHistory
        pred_entry = PredictionHistory(
            user_id=user_id,
            news_id=news_entry.id,
            prediction_label=result["prediction_label"],
            confidence_score=result["confidence_score"],
            model_version=result["model_version"],
            analysis_type="ml_previous",
            prediction_source="web_ui",
            result_status="COMPLETED"
        )
        db.session.add(pred_entry)
        db.session.commit()

        result["prediction_id"] = pred_entry.id
        result["news_id"] = news_entry.id
        result["created_at"] = pred_entry.created_at.isoformat()

        return jsonify({
            "message": "Prediction generated and saved successfully.",
            "result": result
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Inference pipeline error: {str(e)}"}), 500

@news_bp.route("/latest-analysis", methods=["POST"])
def latest_news_analysis():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    article = data.get("article", "").strip()
    category = data.get("category", "General").strip()
    source = data.get("source", "Latest News").strip()

    if not title or not article:
        return jsonify({"error": "Both news title and news article body are required."}), 400

    current_user = get_current_user()
    user_id = current_user.id if current_user else None

    try:
        # 1. Local ML Model Prediction
        ml_result = PredictionService.predict(title, article, check_cache=False)
        ml_label = ml_result["prediction_label"]

        # 2. Gemini Claim Analysis
        gemini_result = GeminiService.analyze_claim(title, article, ml_label=ml_label)

        # Content hash
        content_hash = PredictionService.compute_content_hash(title, article)

        # Persist News
        news_entry = News.query.filter_by(content_hash=content_hash).first()
        if not news_entry:
            news_entry = News(
                title=title,
                article=article,
                category=category,
                source=source,
                content_hash=content_hash
            )
            db.session.add(news_entry)
            db.session.flush()

        # Persist Prediction
        overall_label = gemini_result.get("final_decision", ml_label)
        pred_entry = PredictionHistory(
            user_id=user_id,
            news_id=news_entry.id,
            prediction_label=overall_label,
            confidence_score=ml_result["confidence_score"],
            model_version=ml_result["model_version"],
            analysis_type="gemini_latest",
            prediction_source="web_ui",
            result_status="COMPLETED"
        )
        db.session.add(pred_entry)
        db.session.flush()

        # Persist GeminiVerification
        gemini_entry = GeminiVerification(
            prediction_history_id=pred_entry.id,
            assessment=gemini_result.get("assessment", "UNVERIFIED"),
            confidence_score=gemini_result.get("confidence_score"),
            evidence_summary=gemini_result.get("evidence_summary"),
            sources_json=gemini_result.get("sources", []),
            agreement_status=gemini_result.get("agreement_status", "INCONCLUSIVE")
        )
        db.session.add(gemini_entry)
        db.session.commit()

        return jsonify({
            "message": "Dual-engine analysis completed successfully.",
            "ml_prediction": ml_result,
            "gemini_analysis": gemini_result,
            "overall_decision": overall_label,
            "prediction_id": pred_entry.id,
            "news_id": news_entry.id,
            "created_at": pred_entry.created_at.isoformat()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Dual-engine analysis failed: {str(e)}"}), 500

@news_bp.route("/history", methods=["GET"])
@jwt_required()
def get_user_history():
    user_id = int(get_jwt_identity())
    label_filter = request.args.get("label", "").strip().upper()
    query_text = request.args.get("query", "").strip()

    query = PredictionHistory.query.filter_by(user_id=user_id)

    if label_filter in ("FAKE", "REAL", "INCONCLUSIVE"):
        query = query.filter_by(prediction_label=label_filter)

    records = query.order_by(PredictionHistory.created_at.desc()).all()

    results = []
    for r in records:
        item = r.to_dict()
        if query_text:
            if query_text.lower() not in item["news_title"].lower() and query_text.lower() not in item["news_article"].lower():
                continue
        results.append(item)

    return jsonify({
        "total": len(results),
        "history": results
    }), 200

@news_bp.route("/history/<int:history_id>", methods=["GET"])
@jwt_required()
def get_history_detail(history_id):
    user_id = int(get_jwt_identity())
    record = PredictionHistory.query.filter_by(id=history_id, user_id=user_id).first()
    if not record:
        return jsonify({"error": "Prediction record not found or unauthorized."}), 404
    return jsonify({"record": record.to_dict()}), 200

@news_bp.route("/save", methods=["POST"])
@jwt_required()
def save_news():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    news_id = data.get("news_id")

    if not news_id:
        return jsonify({"error": "news_id is required."}), 400

    existing = SavedNews.query.filter_by(user_id=user_id, news_id=news_id).first()
    if existing:
        return jsonify({"message": "News article is already saved in bookmarks."}), 200

    saved = SavedNews(user_id=user_id, news_id=news_id)
    db.session.add(saved)
    db.session.commit()

    return jsonify({"message": "News article bookmarked successfully.", "saved_id": saved.id}), 201

@news_bp.route("/save/<int:news_id>", methods=["DELETE"])
@jwt_required()
def remove_saved_news(news_id):
    user_id = int(get_jwt_identity())
    saved = SavedNews.query.filter_by(user_id=user_id, news_id=news_id).first()
    if not saved:
        return jsonify({"error": "Saved bookmark not found."}), 404

    db.session.delete(saved)
    db.session.commit()
    return jsonify({"message": "Bookmark removed successfully."}), 200

@news_bp.route("/saved", methods=["GET"])
@jwt_required()
def get_saved_news():
    user_id = int(get_jwt_identity())
    saved_items = SavedNews.query.filter_by(user_id=user_id).order_by(SavedNews.created_at.desc()).all()
    return jsonify({
        "total": len(saved_items),
        "saved_news": [item.to_dict() for item in saved_items]
    }), 200
