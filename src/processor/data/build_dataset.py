from pathlib import Path

import numpy as np

from processor.config.model_config import K_FFT_FEATURES
from processor.data.retrieve_data import auto_retrieve_data
from processor.model.pipeline import build_X, build_y

from .constants import (
    FS1_PATH,
    PROFILE_PATH,
    PS2_PATH,
    TRAINING_LIMIT,
)


def load_signal(path: Path) -> np.ndarray:
    return np.loadtxt(path)


def load_profile(path: Path) -> np.ndarray:
    return np.loadtxt(path)


def build_raw_dataset():
    """
    Build raw dataset for training and testing.
    Outputs:
        X: Features
        y: Labels
    """
    auto_retrieve_data()
    ps2 = load_signal(PS2_PATH)
    fs1 = load_signal(FS1_PATH)
    profile = load_profile(PROFILE_PATH)

    X = np.hstack([ps2, fs1])
    y = build_y(profile)

    return X, y


def build_dataset(
    feature_order: int = 2,
    fft_feature: bool = False,
    k_fft_features: int = K_FFT_FEATURES,
):
    """
    Build dataset for training and testing.
    Outputs:
        X: Features
        y: Labels
    """
    auto_retrieve_data()

    ps2 = load_signal(PS2_PATH)
    fs1 = load_signal(FS1_PATH)
    profile = load_profile(PROFILE_PATH)

    X = build_X(ps2, fs1, feature_order, fft_feature, k_fft_features)
    y = build_y(profile)

    return X, y


def split_dataset(X: np.ndarray, y: np.ndarray, training_limit: int = TRAINING_LIMIT):
    """
    Split dataset into training and testing sets.
    Outputs:
        X_train, y_train: Training features and labels
        X_test, y_test: Testing features and labels
    """

    X_train, y_train = X[:training_limit], y[:training_limit]
    X_test, y_test = X[training_limit:], y[training_limit:]
    return X_train, y_train, X_test, y_test
