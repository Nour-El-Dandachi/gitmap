# ml_experiments/inference.py
import json, joblib
from pathlib import Path
import pandas as pd
from metrics.models import FileMetrics

ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "model.pkl"
FEATURES_PATH = ARTIFACT_DIR / "features.json"

_MODEL = None
_FEATURES = None
_TRUE_INDEX = None

DB_TO_MODEL = {
    "loc": "loc",
    "vg": "v(g)",
    "evg": "ev(g)",
    "ivg": "iv(g)",
    "n": "n",
    "v": "v",
    "l": "l",
    "d": "d",
    "i": "i",
    "e": "e",
    "b": "b",
    "t": "t",
    "iocode": "lOCode",
    "iocomment": "lOComment",
    "ioblank": "lOBlank",
    "iocode_and_comment": "lOCodeAndComment",
    "uniq_op": "uniq_Op",
    "uniq_opnd": "uniq_Opnd",
    "total_op": "total_Op",
    "total_opnd": "total_Opnd",
    "branch_count": "branchCount",
}

def _load_artifacts():
    global _MODEL, _FEATURES, _TRUE_INDEX
    if _MODEL is None:
        _MODEL = joblib.load(MODEL_PATH)
        with open(FEATURES_PATH, "r") as f:
            _FEATURES = json.load(f)

        classes = list(_MODEL.classes_)
        _TRUE_INDEX = classes.index("true")
    return _MODEL, _FEATURES, _TRUE_INDEX

def _prepare_features(df: pd.DataFrame, feature_names):

    df = df.drop(
        columns=["id", "repo_file_id", "created_at", "updated_at", "defects"],
        errors="ignore",
    )
    
    df = df.rename(columns=DB_TO_MODEL)

    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    
    return df[feature_names].fillna(0)

def predict_repo(repo_id: int):
    clf, feature_names, true_idx = _load_artifacts()

    
    qs = FileMetrics.objects.filter(repo_file__repository_id=repo_id).values()
    rows = list(qs)
    if not rows:
        return []

    df = pd.DataFrame(rows)
    X = _prepare_features(df, feature_names)

    
    y_pred = clf.predict(X)
    y_proba = clf.predict_proba(X)

    results = []
    for row, pred, proba in zip(rows, y_pred, y_proba):
        p_true = float(proba[true_idx])
        p_false = float(1.0 - p_true)
        
        FileMetrics.objects.filter(id=row["id"]).update(defects=(pred == "true"))
        results.append({
            "filemetrics_id": row["id"],
            "repo_file_id": row["repo_file_id"],
            "pred": pred,
            "p_true": round(p_true, 2),
            "p_false": round(p_false, 2),
        })
    return results
