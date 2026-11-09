"""
Script: sync_self_dataset.py
Description: Maps and copies F:/Fake news detection/Self-generated.csv into
             dataset/self_generated/self_generated_news.csv matching the canonical
             system schema (news_id, title, article, category, source, label, label_name).
"""

import os
import pandas as pd

def sync():
    source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Self-generated.csv"))
    if not os.path.exists(source_path):
        source_path = "F:/Fake news detection/Self-generated.csv"

    dest_path = os.path.join("dataset", "self_generated", "self_generated_news.csv")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    print(f"Reading source CSV: {source_path}")
    df = pd.read_csv(source_path)
    print(f"Loaded {len(df)} rows.")

    # Schema mapping
    df_mapped = pd.DataFrame()
    df_mapped["news_id"] = df["news_id"]
    df_mapped["title"] = df["title"].astype(str).str.strip()
    df_mapped["article"] = df["article_text"].astype(str).str.strip()
    df_mapped["category"] = df["topic"].fillna("General").astype(str).str.strip()
    df_mapped["source"] = df["source"].fillna("Self-Generated").astype(str).str.strip()
    df_mapped["label"] = df["label"].astype(int)
    df_mapped["label_name"] = df_mapped["label"].map({0: "FAKE", 1: "REAL"})

    # Filter out empty or corrupted records
    df_mapped = df_mapped[df_mapped["article"].str.len() > 20]
    df_mapped = df_mapped[df_mapped["title"].str.len() > 5]

    df_mapped.to_csv(dest_path, index=False, encoding="utf-8")
    print(f"[SUCCESS] Wrote {len(df_mapped)} mapped records to {dest_path}")
    print("Class distribution:")
    print(df_mapped["label_name"].value_counts())

if __name__ == "__main__":
    sync()
