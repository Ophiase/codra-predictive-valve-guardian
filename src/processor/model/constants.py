from pathlib import Path

MODULE_PATH = Path(__file__).parent
CACHE_PATH = MODULE_PATH / "cached"
MODEL_PATH = MODULE_PATH / "model.pkl"

FEATURE_ORDER = 0
FFT_FEATURE_ENABLED = True
K_FFT_FEATURES = 20
