"""
Service: prediction_service.py
Description: ML inference service for fake news classification using the trained
             champion model and TF-IDF vectorizer, supporting exact caching, calibrated
             probabilities, and signal feature extraction.
"""

import os
import hashlib
import joblib
import numpy as np
from backend.config import Config
from backend.ml.preprocessor import clean_text, combine_title_and_article
from backend.models import db, News, PredictionHistory

class PredictionService:
    _model = None
    _vectorizer = None
    _model_version = "Calibrated-LinearSVC-v2.0.0"

    @classmethod
    def load_artifacts(cls):
        """Loads serialized model and TF-IDF vectorizer if not already loaded."""
        if cls._model is None or cls._vectorizer is None:
            if not os.path.exists(Config.ACTIVE_MODEL_PATH):
                raise FileNotFoundError(
                    f"Trained model not found at '{Config.ACTIVE_MODEL_PATH}'. "
                    "Run 'python scripts/train_model.py' to generate artifacts."
                )
            if not os.path.exists(Config.ACTIVE_VECTORIZER_PATH):
                raise FileNotFoundError(
                    f"Vectorizer not found at '{Config.ACTIVE_VECTORIZER_PATH}'. "
                    "Run 'python scripts/train_model.py' to generate artifacts."
                )

            cls._model = joblib.load(Config.ACTIVE_MODEL_PATH)
            cls._vectorizer = joblib.load(Config.ACTIVE_VECTORIZER_PATH)

    @classmethod
    def compute_content_hash(cls, title: str, article: str) -> str:
        """Computes deterministic SHA-256 hash of normalized text."""
        normalized = (title.strip().lower() + " " + article.strip().lower())
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @classmethod
    def check_cached_prediction(cls, content_hash: str):
        """Looks up an exact existing prediction record for the same content."""
        from flask import has_app_context
        if not has_app_context():
            return None
        try:
            existing_news = News.query.filter_by(content_hash=content_hash).first()
            if existing_news and existing_news.predictions:
                latest_pred = existing_news.predictions[-1]
                return {
                    "news_id": existing_news.id,
                    "title": existing_news.title,
                    "article": existing_news.article,
                    "category": existing_news.category,
                    "source": existing_news.source,
                    "prediction_label": latest_pred.prediction_label,
                    "confidence_score": latest_pred.confidence_score,
                    "model_version": latest_pred.model_version,
                    "analysis_type": latest_pred.analysis_type,
                    "is_cached": True,
                    "created_at": latest_pred.created_at.isoformat() if latest_pred.created_at else None
                }
        except Exception:
            pass
        return None

    @classmethod
    def predict(cls, title: str, article: str, check_cache: bool = True):
        """Performs ML inference on title and article."""
        cls.load_artifacts()

        content_hash = cls.compute_content_hash(title, article)
        if check_cache:
            cached = cls.check_cached_prediction(content_hash)
            if cached:
                return cached

        # Preprocess
        processed_text = combine_title_and_article(title, article)
        if not processed_text.strip():
            return {
                "prediction_label": "INCONCLUSIVE",
                "confidence_score": 0.50,
                "probabilities": {"FAKE": 0.50, "REAL": 0.50},
                "model_version": cls._model_version,
                "is_cached": False,
                "signals": [],
                "explanation": "Insufficient textual content to perform meaningful linguistic analysis."
            }

        # Vectorize
        tfidf_features = cls._vectorizer.transform([processed_text])

        # Inference
        probs = cls._model.predict_proba(tfidf_features)[0]
        p_fake = float(probs[0])
        p_real = float(probs[1])

        threshold = Config.CONFIDENCE_THRESHOLD

        if max(p_fake, p_real) < threshold:
            label = "INCONCLUSIVE"
            confidence = max(p_fake, p_real)
        elif p_real >= 0.50:
            label = "REAL"
            confidence = p_real
        else:
            label = "FAKE"
            confidence = p_fake

        # Extract top signal words
        feature_names = cls._vectorizer.get_feature_names_out()
        non_zero_indices = tfidf_features.nonzero()[1]
        word_scores = [
            (feature_names[idx], tfidf_features[0, idx])
            for idx in non_zero_indices
        ]
        word_scores.sort(key=lambda x: x[1], reverse=True)
        top_signals = [w for w, _ in word_scores[:6]]

        if label == "REAL":
            explanation = (
                f"The text exhibits linguistic patterns consistent with credible journalism. "
                f"Key semantic indicators include: {', '.join(top_signals) if top_signals else 'formal syntax and objective attribution'}."
            )
        elif label == "FAKE":
            explanation = (
                f"The text exhibits sensationalist vocabulary or speculative phrasing typical of unverified reports. "
                f"Significant terms detected: {', '.join(top_signals) if top_signals else 'hyperbolic phrasing'}."
            )
        else:
            explanation = (
                "The classification model generated low discriminant confidence. "
                "The content contains mixed signals that require human or secondary verification."
            )

        return {
            "prediction_label": label,
            "confidence_score": round(confidence, 4),
            "probabilities": {
                "FAKE": round(p_fake, 4),
                "REAL": round(p_real, 4)
            },
            "model_version": cls._model_version,
            "is_cached": False,
            "signals": top_signals,
            "explanation": explanation,
            "content_hash": content_hash
        }
