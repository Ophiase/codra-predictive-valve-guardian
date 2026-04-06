from dataclasses import dataclass
from enum import StrEnum

import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from processor.model.classifier_protocol import ClassifierProtocol


class RawOrFeatures(StrEnum):
    RAW = "raw"
    FEATURES = "features"


@dataclass
class ModelConfig:
    X: RawOrFeatures
    feature_order: int
    fft: bool


MODEL_CANDIDATES: dict[str, ClassifierProtocol] = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
    "XGBoost": xgb.XGBClassifier(
        n_estimators=200, eval_metric="logloss", random_state=42
    ),
}

CANDIDATES = [
    ModelConfig(X=RawOrFeatures.RAW, feature_order=0, fft=False),
    ModelConfig(X=RawOrFeatures.FEATURES, feature_order=1, fft=False),
    ModelConfig(X=RawOrFeatures.FEATURES, feature_order=2, fft=False),
    ModelConfig(X=RawOrFeatures.FEATURES, feature_order=0, fft=True),
    ModelConfig(X=RawOrFeatures.FEATURES, feature_order=2, fft=True),
]
