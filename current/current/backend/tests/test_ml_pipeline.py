"""
Test Suite: test_ml_pipeline.py
Description: Pytest unit tests for NLP preprocessing, TF-IDF vectorization,
             calibrated model prediction, and hash caching.
"""

import pytest
from backend.ml.preprocessor import clean_text, combine_title_and_article
from backend.services.prediction_service import PredictionService

def test_clean_text_removes_stopwords_and_urls():
    raw = "BREAKING: Check this amazing website http://example.com/fake and see the results!"
    cleaned = clean_text(raw)
    assert "http" not in cleaned
    assert "breaking" in cleaned
    assert "amazing" in cleaned
    assert "the" not in cleaned # Stopword removed

def test_combine_title_and_article_weighting():
    title = "NASA Discovers Exoplanet"
    article = "Astronomers identified a rocky planet orbiting a distant star."
    combined = combine_title_and_article(title, article)
    assert "nasa discovers exoplanet" in combined
    # Title appears twice for proportional salience
    assert combined.count("nasa") == 2

def test_prediction_service_inference_bounds():
    title = "James Webb Space Telescope Directly Images Exoplanetary Atmosphere"
    article = "Astronomers analyzing transmission spectroscopy data confirmed atmospheric carbon dioxide molecules."
    res = PredictionService.predict(title, article, check_cache=False)

    assert "prediction_label" in res
    assert res["prediction_label"] in ("REAL", "FAKE", "INCONCLUSIVE")
    assert 0.0 <= res["confidence_score"] <= 1.0
    assert "probabilities" in res
    assert 0.0 <= res["probabilities"]["REAL"] <= 1.0
    assert 0.0 <= res["probabilities"]["FAKE"] <= 1.0
    assert len(res["signals"]) > 0

def test_prediction_hash_determinism():
    h1 = PredictionService.compute_content_hash("Title Here", "Article body text here.")
    h2 = PredictionService.compute_content_hash("title here", "article body text here.")
    assert h1 == h2
