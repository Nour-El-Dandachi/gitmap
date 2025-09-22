# ml_experiments/train_model.py
import json, joblib
from pathlib import Path
import pandas as pd
from scipy.io import arff
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier

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

joblib.dump(clf, MODEL_PATH)
with open(FEATURES_PATH, "w") as f:
    json.dump(list(clf.feature_names_in_), f)


y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=clf.classes_, yticklabels=clf.classes_)
plt.title("Confusion Matrix")
plt.ylabel("True Label")
plt.xlabel("Predicted Label")
plt.savefig(ARTIFACT_DIR / "confusion_matrix.png")

from sklearn.metrics import RocCurveDisplay

y_proba = clf.predict_proba(X_test)[:, 1]
RocCurveDisplay.from_predictions(y_test, y_proba, pos_label="true")

plt.title("ROC Curve")
plt.savefig(ARTIFACT_DIR / "roc_curve.png")

metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred, average="binary", pos_label="true"),
    "recall": recall_score(y_test, y_pred, average="binary", pos_label="true"),
    "f1": f1_score(y_test, y_pred, average="binary", pos_label="true"),
}

with open(ARTIFACT_DIR / "metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\nSaved metrics:", metrics)

joblib.dump(clf, MODEL_PATH)
with open(FEATURES_PATH, "w") as f:
    json.dump(list(clf.feature_names_in_), f)
