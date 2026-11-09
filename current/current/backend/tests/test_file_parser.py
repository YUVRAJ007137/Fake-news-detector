"""
Test Suite: test_file_parser.py
Description: Pytest unit tests for multi-format document text extraction and batch CSV parsing.
"""

import os
import tempfile
import pytest
from backend.services.file_service import FileService

def test_extract_text_txt():
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("Global Climate Conference Reaches Historic Zero Emissions Accord\n\nDelegates from sixty nations ratified the international climate treaty.")
        temp_path = f.name

    try:
        title, article = FileService.extract_text_txt(temp_path)
        assert "Global Climate Conference" in title
        assert "Delegates from sixty nations" in article
    finally:
        os.remove(temp_path)

def test_process_csv_batch():
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("title,article,category\n")
        f.write("NASA Launches New Satellite,Engineers at the space center launched an earth observation probe,Science\n")
        f.write("Secret Alien Fleet Spotted Over Capital,UFO conspiracy bloggers claim military radar detected invisible ships,Conspiracy\n")
        temp_path = f.name

    try:
        results = FileService.process_csv(temp_path, analysis_mode="ml_previous")
        assert len(results) == 2
        assert "NASA Launches" in results[0]["title"]
        assert "overall_decision" in results[0]
        assert results[0]["overall_decision"] in ("REAL", "FAKE", "INCONCLUSIVE")
    finally:
        os.remove(temp_path)

def test_reject_unsupported_extensions():
    assert FileService.allowed_file("report.pdf") is True
    assert FileService.allowed_file("dataset.csv") is True
    assert FileService.allowed_file("malicious.exe") is False
    assert FileService.allowed_file("script.py") is False
