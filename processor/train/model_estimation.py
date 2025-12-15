import time
from typing import Tuple

import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

from ..data.build_dataset import build_dataset, build_raw_dataset, split_dataset
from ..model.constants import K_FFT_FEATURES

configs = [
    {"X": "raw", "feature_order": 0, "fft": False},
    {"X": "features", "feature_order": 1, "fft": False},
    {"X": "features", "feature_order": 2, "fft": False},
    {"X": "features", "feature_order": 0, "fft": True},
    {"X": "features", "feature_order": 2, "fft": True},
]

models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
    "XGBoost": xgb.XGBClassifier(
        n_estimators=200, eval_metric="logloss", random_state=42
    ),
}


def evaluate_model(
    model: object,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Tuple[float, float, float, float]:
    start_train = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_train

    start_pred = time.time()
    y_pred = model.predict(X_test)
    pred_time = time.time() - start_pred

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    return acc, f1, train_time, pred_time


def evaluate_all() -> pd.DataFrame:
    results = []

    for config in configs:
        start_feat = time.time()
        if config["X"] == "raw":
            X, y = build_raw_dataset()
        else:
            X, y = build_dataset(
                feature_order=config["feature_order"],
                fft_feature=config["fft"],
                k_fft_features=K_FFT_FEATURES,
            )
        feat_time = time.time() - start_feat

        X_train, y_train, X_test, y_test = split_dataset(X, y)

        for name, model in models.items():
            print(
                f"Config: data={config['X']}, feature_order={config['feature_order']}, fft={config['fft']}, model={name}"
            )
            acc, f1, train_time, pred_time = evaluate_model(
                model, X_train, y_train, X_test, y_test
            )
            results.append(
                {
                    "data": config["X"],
                    "feature_order": config["feature_order"],
                    "fft": config["fft"],
                    "model": name,
                    "accuracy": acc,
                    "f1": f1,
                    "total_execution_time": feat_time + pred_time,
                    "feature_time": feat_time,
                    # "train_time": train_time,
                    "predict_time": pred_time,
                }
            )

    df_results = pd.DataFrame(results)
    df_results_sorted = df_results.sort_values(
        by=["f1", "accuracy", "total_execution_time"], ascending=[False, False, True]
    )

    return df_results_sorted


if __name__ == "__main__":
    df_results = evaluate_all()
    print(df_results)
    # df_results.to_csv("naive_best_model_estimation_results.csv", index=False)
