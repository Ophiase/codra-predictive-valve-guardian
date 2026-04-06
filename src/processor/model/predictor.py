import joblib
import numpy as np

from processor.data.build_dataset import build_X
from processor.model.classifier_protocol import ClassifierProtocol

from .constants import FEATURE_ORDER, FFT_FEATURE_ENABLED, K_FFT_FEATURES, MODEL_PATH

BinaryPrediction = bool


class Predictor:
    model: ClassifierProtocol

    def __init__(self, model: ClassifierProtocol | None = None):
        if model is None:
            model = joblib.load(MODEL_PATH)
        else:
            self.model = model

    def predict(self, ps2: np.ndarray, fs1: np.ndarray) -> list[BinaryPrediction]:
        """
        Predicts the condition based on PS2 and FS1 signals.
        :param ps2: np.ndarray, shape (n_samples, n_timesteps)
        :param fs1: np.ndarray, shape (n_samples, n_timesteps)
        :return: list of bool, predictions for each sample
        """
        X = build_X(
            ps2,
            fs1,
            feature_order=FEATURE_ORDER,
            fft_feature=FFT_FEATURE_ENABLED,
            k_fft_features=K_FFT_FEATURES,
        )
        predictions = self.model.predict(X)
        return predictions.tolist()

    def predict_single(self, ps2: np.ndarray, fs1: np.ndarray) -> BinaryPrediction:
        """
        Predicts the condition for a single sample based on PS2 and FS1 signals.
        :param ps2: np.ndarray, shape (n_timesteps,)
        :param fs1: np.ndarray, shape (n_timesteps,)
        :return: bool, prediction for the sample
        """
        ps2_reshaped = ps2.reshape(1, -1)
        fs1_reshaped = fs1.reshape(1, -1)
        X = build_X(
            ps2_reshaped,
            fs1_reshaped,
            feature_order=FEATURE_ORDER,
            fft_feature=FFT_FEATURE_ENABLED,
            k_fft_features=K_FFT_FEATURES,
        )
        prediction = self.model.predict(X)
        return bool(prediction[0])

    def predict_batch(self, X: np.ndarray) -> list[BinaryPrediction]:
        predictions = self.model.predict(X)
        return predictions.tolist()
