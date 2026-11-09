"""
Test Suite: test_gemini_service.py
Description: Pytest unit tests for Gemini claim analysis service, offline graceful degradation,
             and consensus logic.
"""

import pytest
from backend.services.gemini_service import GeminiService

def test_gemini_unconfigured_offline_degradation():
    # When GEMINI_API_KEY is not configured or empty
    res = GeminiService.analyze_claim(
        title="Breaking Tech News",
        article="A new quantum chip has been unveiled by university physicists.",
        ml_label="REAL"
    )
    assert "available" in res
    assert "assessment" in res
    assert res["final_decision"] == "REAL" # Falls back safely to local ML label
    assert "offline" in res.get("limitations", "").lower() or "offline" in res.get("evidence_summary", "").lower()
