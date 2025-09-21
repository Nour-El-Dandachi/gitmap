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

clf = DecisionTreeClassifier(
    max_depth=None,          
    class_weight="balanced",
    random_state=42
)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

joblib.dump(clf, MODEL_PATH)
with open(FEATURES_PATH, "w") as f:
    json.dump(list(clf.feature_names_in_), f)
