import numpy as np

from processor.config.model_config import K_FFT_FEATURES


def simple_features(signal: np.ndarray) -> np.ndarray:
    mean = signal.mean(axis=1)
    std = signal.std(axis=1)
    minimum = signal.min(axis=1)
    maximum = signal.max(axis=1)
    q10 = np.quantile(signal, 0.1, axis=1)
    q90 = np.quantile(signal, 0.9, axis=1)
    energy = np.sum(signal**2, axis=1)
    features = np.stack([mean, std, minimum, maximum, q10, q90, energy], axis=1)
    return features


def extract_features(
    signal: np.ndarray,
    order: int,
    fft_feature: bool,
    k_fft_features: int = K_FFT_FEATURES,
) -> np.ndarray:
    if order > 2 or order < 0:
        raise ValueError("Order must be 0, 1, or 2")

    result = [simple_features(signal)]

    signal_order_k = signal
    for _ in range(1, order + 1):
        signal_order_k = np.diff(signal_order_k, axis=1)
        features_order_k = simple_features(signal_order_k)
        result.append(features_order_k)

    if fft_feature:
        fft_coeffs = np.fft.rfft(signal, axis=1)
        fft_magnitudes = np.abs(fft_coeffs[:, :k_fft_features])
        result.append(fft_magnitudes)

    return np.hstack(result)


def build_X(
    ps2: np.ndarray,
    fs1: np.ndarray,
    feature_order: int,
    fft_feature: bool,
    k_fft_features: int = K_FFT_FEATURES,
) -> np.ndarray:
    X_ps2 = extract_features(ps2, feature_order, fft_feature, k_fft_features)
    X_fs1 = extract_features(fs1, feature_order, fft_feature, k_fft_features)
    X = np.hstack([X_ps2, X_fs1])
    return X


def build_y(profile: np.ndarray) -> np.ndarray:
    y = (profile[:, 1] == 100).astype(int)
    return y
