"""
Script: validate_datasets.py
Description: Validates datasets for column presence, missing values, label conventions,
             duplicates, and returns a structured validation summary.
"""

import os
import sys
import json
import pandas as pd

REQUIRED_COLUMNS = ["news_id", "title", "article", "category", "source", "label", "label_name"]

def validate_csv(filepath):
    print(f"\n--- Validating: {filepath} ---")
    if not os.path.exists(filepath):
        return {"status": "ERROR", "message": f"File not found: {filepath}"}

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return {"status": "ERROR", "message": f"Could not parse CSV: {str(e)}"}

    total_rows = len(df)
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    if missing_cols:
        return {
            "status": "FAILED",
            "file": filepath,
            "error": f"Missing required columns: {missing_cols}",
            "available_columns": list(df.columns)
        }

    # Missing values
    null_counts = df[REQUIRED_COLUMNS].isnull().sum().to_dict()
    has_nulls = any(v > 0 for v in null_counts.values())

    # Label validity (must be 0 or 1)
    unique_labels = sorted(df["label"].unique().tolist())
    valid_labels = set(unique_labels).issubset({0, 1})

    # Duplicates check on title + article
    dups = df.duplicated(subset=["title", "article"]).sum()

    # Class balance
    class_dist = df["label_name"].value_counts().to_dict()

    result = {
        "status": "PASSED" if not missing_cols and valid_labels and not has_nulls else "WARNING",
        "file": filepath,
        "total_rows": total_rows,
        "null_counts": null_counts,
        "unique_labels": unique_labels,
        "valid_labels": valid_labels,
        "duplicate_rows": int(dups),
        "class_distribution": class_dist
    }

    print(json.dumps(result, indent=2))
    return result

def validate_all():
    targets = [
        os.path.join("dataset", "self_generated", "self_generated_news.csv"),
        os.path.join("dataset", "kaggle", "kaggle_news.csv"),
        os.path.join("dataset", "hybrid", "hybrid_dataset.csv")
    ]
    results = {}
    for target in targets:
        if os.path.exists(target):
            results[target] = validate_csv(target)
        else:
            print(f"Skipping {target} (not generated yet).")
    return results

if __name__ == "__main__":
    validate_all()
