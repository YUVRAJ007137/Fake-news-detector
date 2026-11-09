"""
Script: evaluate_model.py
Description: Evaluates the production model against test sets or new inputs,
             outputting precision, recall, F1, and a confusion matrix breakdown.
"""

import os
import sys
import json
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.ml.preprocessor import clean_text, combine_title_and_article

def evaluate():
    model_path = os.path.join("trained_models", "fake_news_model.pkl")
    vectorizer_path = os.path.join("trained_models", "tfidf_vectorizer.pkl")
    dataset_path = os.path.join("dataset", "hybrid", "hybrid_dataset.csv")

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("[ERROR] Model artifacts not found. Run scripts/train_model.py first.")
        sys.exit(1)

    print("Loading model and vectorizer...")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    df = pd.read_csv(dataset_path)
    df["processed_text"] = df.apply(
        lambda r: combine_title_and_article(str(r["title"]), str(r["article"])),
        axis=1
    )

    X_tfidf = vectorizer.transform(df["processed_text"])
    y_true = df["label"].astype(int)
    y_pred = model.predict(X_tfidf)
    y_prob = model.predict_proba(X_tfidf)[:, 1]

    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred).tolist()
    cr = classification_report(y_true, y_pred, target_names=["FAKE", "REAL"], output_dict=True)

    summary = {
        "accuracy": round(acc, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm,
        "classification_report": cr
    }

    print("\n--- Model Evaluation Summary ---")
    print(f"Overall Accuracy: {acc * 100:.2f}%")
    print(f"Overall F1 Score: {f1 * 100:.2f}%")
    print(f"Confusion Matrix [TN, FP / FN, TP]: {cm}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=["FAKE", "REAL"]))

    return summary

if __name__ == "__main__":
    evaluate()
