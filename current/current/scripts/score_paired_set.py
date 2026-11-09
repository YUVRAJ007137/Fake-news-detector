"""Score paired_test_set.csv against the project's trained model.
Run from the project root:  python score_paired_set.py [--threshold 0.6]
"""
import argparse, os, sys
import joblib, pandas as pd

sys.path.insert(0, os.getcwd())
from backend.ml.preprocessor import combine_title_and_article

ap = argparse.ArgumentParser()
ap.add_argument("--csv", default="paired_test_set.csv")
ap.add_argument("--model", default="trained_models/fake_news_model.pkl")
ap.add_argument("--vectorizer", default="trained_models/tfidf_vectorizer.pkl")
ap.add_argument("--threshold", type=float, default=0.5,
                help="min confidence, else INCONCLUSIVE (use your Config.CONFIDENCE_THRESHOLD)")
a = ap.parse_args()

model, vec = joblib.load(a.model), joblib.load(a.vectorizer)
df = pd.read_csv(a.csv)
X = vec.transform([combine_title_and_article(t, b) for t, b in zip(df.title, df.article)])
p = model.predict_proba(X)          # column 0 = FAKE, 1 = REAL (matches prediction_service.py)
df["p_fake"] = p[:, 0].round(3)

def label(pf):
    pr = 1 - pf
    if max(pf, pr) < a.threshold: return "INCONCLUSIVE"
    return "REAL" if pr >= 0.5 else "FAKE"

df["predicted"] = df.p_fake.apply(label)
df["correct"] = df.predicted == df.label
df.to_csv("paired_results.csv", index=False)

print("\n== By variant (accuracy | mean P(FAKE) | inconclusive) ==")
g = df.groupby(["variant"]).agg(n=("id", "count"), accuracy=("correct", "mean"),
        mean_p_fake=("p_fake", "mean"),
        inconclusive=("predicted", lambda s: (s == "INCONCLUSIVE").sum())).round(2)
print(g.to_string())

print("\n== Fake pairs: sensational vs neutral P(FAKE) ==")
piv = df[df.label == "FAKE"].pivot(index="group", columns="variant", values="p_fake")
piv["style_gap"] = (piv.sensational - piv.neutral).round(3)
print(piv.to_string())
print("\nStyle-bias signal: mean gap =", round(piv.style_gap.mean(), 3),
      "(large positive = detector keys on tone, not content)")
print("Wrote paired_results.csv")
