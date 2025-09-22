# ml_experiments/train_model.py
import json, joblib
from pathlib import Path
import pandas as pd
from scipy.io import arff
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.colors as mcolors
import numpy as np

ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = ARTIFACT_DIR / "model.pkl"
FEATURES_PATH = ARTIFACT_DIR / "features.json"

def load_arff(path):
    data, _ = arff.loadarff(path)
    df = pd.DataFrame(data)
    df["defects"] = df["defects"].apply(lambda x: x.decode("utf-8"))
    return df

df_jm1 = load_arff("ml_experiments/jm1.arff.txt")
df_cm1 = load_arff("ml_experiments/cm1.arff.txt")
df = pd.concat([df_jm1, df_cm1], ignore_index=True)

X = df.drop(columns=["defects"])
y = df["defects"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model + features
joblib.dump(clf, MODEL_PATH)
with open(FEATURES_PATH, "w") as f:
    json.dump(list(clf.feature_names_in_), f)

# Metrics and visualizations
from sklearn.metrics import (
    classification_report, confusion_matrix,
    precision_score, recall_score, f1_score, RocCurveDisplay
)
import matplotlib.pyplot as plt
import seaborn as sns

print(classification_report(y_test, y_pred))

PRIMARY = "#948BFC"
LIGHT = "#D6D3F3"
DARK = "#131325"

custom_cmap = mcolors.LinearSegmentedColormap.from_list(
    "brand_cmap", [LIGHT, PRIMARY, DARK], N=256
)

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap=custom_cmap,
    norm=mcolors.Normalize(vmin=0, vmax=np.max(cm)),
    cbar_kws={"shrink": 0.8, "label": "Count"},
    xticklabels=clf.classes_,
    yticklabels=clf.classes_
)
plt.title("Confusion Matrix", color=DARK, fontsize=14, weight="bold")
plt.ylabel("True Label", color=DARK, fontsize=12)
plt.xlabel("Predicted Label", color=DARK, fontsize=12)
plt.xticks(color=DARK)
plt.yticks(color=DARK, rotation=0)
plt.savefig(ARTIFACT_DIR / "confusion_matrix.png", facecolor="white")
plt.close()

y_proba = clf.predict_proba(X_test)[:, 1]
roc_disp = RocCurveDisplay.from_predictions(
    y_test,
    y_proba,
    pos_label="true",
    color=PRIMARY,
    name="ROC Curve"
)
plt.plot([0, 1], [0, 1], "--", color=LIGHT)
plt.title("ROC Curve", color=DARK, fontsize=14, weight="bold")
plt.xlabel("False Positive Rate", color=DARK, fontsize=12)
plt.ylabel("True Positive Rate", color=DARK, fontsize=12)
plt.xticks(color=DARK)
plt.yticks(color=DARK)
plt.savefig(ARTIFACT_DIR / "roc_curve.png", facecolor="white")
plt.close()

metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred, average="binary", pos_label="true"),
    "recall": recall_score(y_test, y_pred, average="binary", pos_label="true"),
    "f1": f1_score(y_test, y_pred, average="binary", pos_label="true"),
}

with open(ARTIFACT_DIR / "metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\nSaved metrics:", metrics)
