"""
Script: train_model.py
Description: Trains TF-IDF + Logistic Regression and Calibrated Linear SVM models
             on the harmonized hybrid dataset, evaluates both pipelines, selects the
             champion model, and serializes artifacts to trained_models/.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.ml.preprocessor import clean_text, combine_title_and_article

def train_and_evaluate():
    dataset_path = os.path.join("dataset", "hybrid", "hybrid_dataset.csv")
    models_dir = "trained_models"
    os.makedirs(models_dir, exist_ok=True)

    if not os.path.exists(dataset_path):
        print(f"[ERROR] Hybrid dataset not found at {dataset_path}!")
        print("Please run scripts/create_hybrid_dataset.py first.")
        sys.exit(1)

    print(f"Loading hybrid dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"Loaded {len(df)} records.")

    # Prepare features and labels
    print("Preprocessing text features...")
    df["processed_text"] = df.apply(
        lambda r: combine_title_and_article(str(r["title"]), str(r["article"])),
        axis=1
    )
    X = df["processed_text"]
    y = df["label"].astype(int)

    # Stratified Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")

    # TF-IDF Vectorization
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # 1. Candidate 1: Logistic Regression
    print("\n--- Training Candidate 1: Logistic Regression ---")
    lr = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    lr.fit(X_train_tfidf, y_train)
    y_pred_lr = lr.predict(X_test_tfidf)
    y_prob_lr = lr.predict_proba(X_test_tfidf)[:, 1]

    metrics_lr = {
        "model_name": "Logistic Regression",
        "accuracy": round(float(accuracy_score(y_test, y_pred_lr)), 4),
        "precision": round(float(precision_score(y_test, y_pred_lr, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred_lr, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred_lr, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_prob_lr)), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred_lr).tolist()
    }
    print(f"Logistic Regression F1: {metrics_lr['f1_score']} | Acc: {metrics_lr['accuracy']}")

    # 2. Candidate 2: Calibrated Linear SVM
    print("\n--- Training Candidate 2: Calibrated Linear SVM ---")
    base_svc = LinearSVC(C=1.0, random_state=42, max_iter=2000, dual="auto")
    calibrated_svc = CalibratedClassifierCV(estimator=base_svc, cv=3)
    calibrated_svc.fit(X_train_tfidf, y_train)
    y_pred_svc = calibrated_svc.predict(X_test_tfidf)
    y_prob_svc = calibrated_svc.predict_proba(X_test_tfidf)[:, 1]

    metrics_svc = {
        "model_name": "Calibrated Linear Support Vector Machine",
        "accuracy": round(float(accuracy_score(y_test, y_pred_svc)), 4),
        "precision": round(float(precision_score(y_test, y_pred_svc, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred_svc, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred_svc, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_prob_svc)), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred_svc).tolist()
    }
    print(f"Calibrated Linear SVM F1: {metrics_svc['f1_score']} | Acc: {metrics_svc['accuracy']}")

    # Champion selection based on F1 Score
    if metrics_svc["f1_score"] >= metrics_lr["f1_score"]:
        champion_model = calibrated_svc
        champion_metrics = metrics_svc
        print("\n=> Selected Champion: Calibrated Linear Support Vector Machine")
    else:
        champion_model = lr
        champion_metrics = metrics_lr
        print("\n=> Selected Champion: Logistic Regression")

    # Serialize artifacts
    model_path = os.path.join(models_dir, "fake_news_model.pkl")
    vectorizer_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    metadata_path = os.path.join(models_dir, "model_metadata.json")

    joblib.dump(champion_model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    metadata = {
        "model_version": "v2.0.0",
        "timestamp": datetime.now().isoformat(),
        "algorithm": champion_metrics["model_name"],
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "feature_count": X_train_tfidf.shape[1],
        "champion_metrics": champion_metrics,
        "comparison_metrics": {
            "logistic_regression": metrics_lr,
            "calibrated_linear_svc": metrics_svc
        },
        "classification_report": classification_report(
            y_test,
            champion_model.predict(X_test_tfidf),
            target_names=["FAKE", "REAL"],
            output_dict=True
        ),
        "artifacts": {
            "model_path": model_path,
            "vectorizer_path": vectorizer_path
        }
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print(f"\n[SUCCESS] Model successfully saved to {model_path}")
    print(f"[SUCCESS] Vectorizer saved to {vectorizer_path}")
    print(f"[SUCCESS] Metadata saved to {metadata_path}")
    return metadata

if __name__ == "__main__":
    train_and_evaluate()
