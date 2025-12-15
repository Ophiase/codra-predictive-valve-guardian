from pathlib import Path

import numpy as np

from .constants import FS1_PATH, PROFILE_PATH, PS2_PATH, TRAINING_LIMIT


def load_signal(path: Path) -> np.ndarray:
    return np.loadtxt(path)


def load_profile(path: Path) -> np.ndarray:
    return np.loadtxt(path)


def simple_features(signal: np.ndarray) -> np.ndarray:
    mean = signal.mean(axis=1)
    std = signal.std(axis=1)
    minimum = signal.min(axis=1)
    maximum = signal.max(axis=1)
    q10 = np.quantile(signal, 0.1, axis=1)
    q90 = np.quantile(signal, 0.9, axis=1)
    energy = np.sum(signal**2, axis=1)
    features = np.stack(
        [mean, std, minimum, maximum, q10, q90, energy], axis=1)
    return features


def extract_features(signal: np.ndarray, order: int, fft_feature: bool) -> np.ndarray:
    if order > 2 or order < 0:
        raise ValueError("Order must be 0, 1, or 2")

    result = [simple_features(signal)]

    signal_order_k = signal
    for _ in range(1, order + 1):
        signal_order_k = np.diff(signal_order_k, axis=1)
        features_order_k = simple_features(signal_order_k)
        result.append(features_order_k)

    if fft_feature:
        k_fft_features = 20  # TODO: expose it as a parameter
        fft_coeffs = np.fft.rfft(signal, axis=1)
        fft_magnitudes = np.abs(fft_coeffs[:, :k_fft_features])
        result.append(fft_magnitudes)

    return np.hstack(result)


def build_y(profile: np.ndarray) -> np.ndarray:
    y = (profile[:, 1] == 100).astype(int)
    return y


def build_raw_dataset():
    """
    Build raw dataset for training and testing.
    Outputs:
        X: Features
        y: Labels
   """
    ps2 = load_signal(PS2_PATH)
    fs1 = load_signal(FS1_PATH)
    profile = load_profile(PROFILE_PATH)

    X = np.hstack([ps2, fs1])
    y = build_y(profile)

    return X, y


def build_dataset(feature_order: int = 2, fft_feature: bool = False):
    """
    Build dataset for training and testing.
    Outputs:
        X: Features
        y: Labels
    """
    ps2 = load_signal(PS2_PATH)
    fs1 = load_signal(FS1_PATH)
    profile = load_profile(PROFILE_PATH)

    X_ps2 = extract_features(ps2, feature_order, fft_feature)
    X_fs1 = extract_features(fs1, feature_order, fft_feature)

    X = np.hstack([X_ps2, X_fs1])
    y = build_y(profile)

    return X, y


def split_dataset(X: np.ndarray, y: np.ndarray, training_limit: int = TRAINING_LIMIT):
    """
    Split dataset into training and testing sets.
    """

    X_train, y_train = X[:training_limit], y[:training_limit]
    X_test, y_test = X[training_limit:], y[training_limit:]
    return X_train, y_train, X_test, y_test
