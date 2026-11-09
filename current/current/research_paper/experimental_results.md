# Experimental Evaluation & Empirical Results

## 1. Experimental Setup

- **Dataset**: Harmonized Hybrid Fake News Corpus (`dataset/hybrid/hybrid_dataset.csv`)
- **Total Records**: 684 balanced records (341 FAKE, 343 REAL)
- **Train-Test Partition**: Stratified 80/20 split (`random_state=42`)
  - **Training Samples**: 547 (273 FAKE, 274 REAL)
  - **Testing Samples**: 137 (68 FAKE, 69 REAL)
- **Feature Representation**: TF-IDF Vectorizer with sublinear term frequency, unigram and bigram extraction $(1, 2)$, yielding 5,000 vocabulary features.
- **Hardware/Environment**: Windows 11 AMD64, Python 3.13.5, Scikit-learn 1.9.1.

---

## 2. Quantitative Model Comparison

| Evaluation Metric | Candidate 1: Logistic Regression | Candidate 2: Calibrated Linear SVM (Champion) |
| :--- | :--- | :--- |
| **Accuracy** | 98.54% | **98.54%** |
| **Precision (Macro Avg)** | 98.59% | **98.59%** |
| **Recall (Macro Avg)** | 98.53% | **98.53%** |
| **F1 Score (Macro Avg)** | 0.9854 | **0.9854** |
| **F1 Score (Real Class)** | 0.9857 | **0.9857** |
| **ROC-AUC Score** | 1.0000 | **1.0000** |
| **Calibration Method** | Built-in Sigmoid Log-loss | 3-Fold Platt Scaling (`CalibratedClassifierCV`) |
| **Inference Time (Single Query)** | ~1.3 ms | **~1.5 ms** |

---

## 3. Detailed Classification Report (Champion Model)

```text
              precision    recall  f1-score   support

        FAKE     1.0000    0.9706    0.9851        68
        REAL     0.9718    1.0000    0.9857        69

    accuracy                         0.9854       137
   macro avg     0.9859    0.9853    0.9854       137
weighted avg     0.9858    0.9854    0.9854       137
```

---

## 4. Confusion Matrix Breakdown

$$\begin{bmatrix} 66 & 2 \\ 0 & 69 \end{bmatrix}$$

- **True Negatives ($TN = 66$)**: 66 out of 68 deceptive news articles in the holdout test set were accurately flagged.
- **False Positives ($FP = 2$)**: Only 2 deceptive news items slipped past the linguistic decision boundary.
- **False Negatives ($FN = 0$)**: **Zero authentic articles were misclassified as fake** (100% recall on authentic news).
- **True Positives ($TP = 69$)**: All 69 authentic news articles were correctly identified.
