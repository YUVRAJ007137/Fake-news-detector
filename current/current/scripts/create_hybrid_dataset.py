"""
Script: create_hybrid_dataset.py
Description: Ingests self-generated and Kaggle benchmark datasets, performs cleaning,
             deduplication, provenance tracking, and constructs the unified hybrid dataset
             with balanced class distributions and an audit report.
"""

import os
import sys
import json
import hashlib
import pandas as pd

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    return " ".join(text.split())

def compute_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def create_hybrid_dataset():
    self_path = os.path.join("dataset", "self_generated", "self_generated_news.csv")
    kaggle_path = os.path.join("dataset", "kaggle", "kaggle_news.csv")
    hybrid_dir = os.path.join("dataset", "hybrid")
    reports_dir = os.path.join("dataset", "reports")
    os.makedirs(hybrid_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    hybrid_csv = os.path.join(hybrid_dir, "hybrid_dataset.csv")
    report_json = os.path.join(reports_dir, "hybrid_dataset_report.json")

    # Check existence
    if not os.path.exists(self_path):
        print(f"[ERROR] Self-generated dataset missing at {self_path}. Run scripts/generate_self_dataset.py first.")
        sys.exit(1)
    if not os.path.exists(kaggle_path):
        print(f"[ERROR] Kaggle dataset missing at {kaggle_path}. Run scripts/prepare_kaggle_dataset.py first.")
        sys.exit(1)

    print(f"Loading self-generated data from {self_path}...")
    df_self = pd.read_csv(self_path)
    df_self["dataset_source"] = "self_generated"

    print(f"Loading Kaggle benchmark data from {kaggle_path}...")
    df_kaggle = pd.read_csv(kaggle_path)
    df_kaggle["dataset_source"] = "kaggle"

    # Merge
    merged_df = pd.concat([df_self, df_kaggle], ignore_index=True)
    initial_count = len(merged_df)
    print(f"Total raw merged records: {initial_count}")

    # Standardize & clean
    merged_df["title"] = merged_df["title"].apply(normalize_text)
    merged_df["article"] = merged_df["article"].apply(normalize_text)
    merged_df["label"] = merged_df["label"].astype(int)
    merged_df["label_name"] = merged_df["label"].map({0: "FAKE", 1: "REAL"})

    # Filter out empty or too short text
    merged_df = merged_df[merged_df["article"].str.len() > 30]
    merged_df = merged_df[merged_df["title"].str.len() > 5]

    # Deduplicate based on combined title and article hash
    merged_df["content_hash"] = (merged_df["title"].str.lower() + " " + merged_df["article"].str.lower()).apply(compute_hash)
    merged_df = merged_df.drop_duplicates(subset=["content_hash"]).reset_index(drop=True)

    # Re-index hybrid news_id
    merged_df["news_id"] = [f"HYB-{i+1:04d}" for i in range(len(merged_df))]

    # Order columns
    final_cols = ["news_id", "title", "article", "category", "source", "label", "label_name", "dataset_source", "content_hash"]
    final_df = merged_df[final_cols]

    # Compute statistics
    class_dist = final_df["label_name"].value_counts().to_dict()
    source_dist = final_df["dataset_source"].value_counts().to_dict()
    category_dist = final_df["category"].value_counts().to_dict()

    report = {
        "dataset_name": "Harmonized Hybrid Fake News Dataset",
        "version": "v1.0.0",
        "total_records": len(final_df),
        "deduplicated_count": initial_count - len(final_df),
        "class_distribution": class_dist,
        "source_distribution": source_dist,
        "category_distribution": category_dist,
        "features": final_cols,
        "status": "VALIDATED"
    }

    final_df.to_csv(hybrid_csv, index=False, encoding="utf-8")
    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"[SUCCESS] Hybrid dataset created: {hybrid_csv} ({len(final_df)} records)")
    print(f"Class breakdown: {class_dist}")
    print(f"Source breakdown: {source_dist}")
    print(f"Report saved to: {report_json}")

if __name__ == "__main__":
    create_hybrid_dataset()
