"""
Test Suite: test_dataset_validation.py
Description: Pytest unit tests for dataset schema verification, label consistency,
             and hybrid dataset integrity.
"""

import os
import pytest
from scripts.validate_datasets import validate_csv

def test_validate_self_generated_dataset():
    path = os.path.join("dataset", "self_generated", "self_generated_news.csv")
    assert os.path.exists(path)
    res = validate_csv(path)
    assert res["status"] == "PASSED"
    assert res["total_rows"] >= 40
    assert res["valid_labels"] is True
    assert res["duplicate_rows"] == 0

def test_validate_hybrid_dataset():
    path = os.path.join("dataset", "hybrid", "hybrid_dataset.csv")
    assert os.path.exists(path)
    res = validate_csv(path)
    assert res["status"] == "PASSED"
    assert res["total_rows"] >= 60
    assert res["valid_labels"] is True
    assert res["duplicate_rows"] == 0
