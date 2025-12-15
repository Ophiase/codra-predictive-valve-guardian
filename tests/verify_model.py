import joblib
import numpy as np

from data.build_dataset import build_dataset
from model.constants import FEATURE_ORDER, FFT_FEATURE_ENABLED, K_FFT_FEATURES
from model.predictor import Predictor


def test_predictor() -> None:
    X, y = build_dataset(
        feature_order=FEATURE_ORDER,
        fft_feature=FFT_FEATURE_ENABLED,
        k_fft_features=K_FFT_FEATURES,
    )
    predictor = Predictor()

    y_pred = predictor.predict_batch(X)
    loss = np.mean((y - y_pred) ** 2)
    print(f"Mean Squared Error: {loss}")


if __name__ == "__main__":
    test_predictor()
