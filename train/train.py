from data.build_dataset import build_dataset, split_dataset
from model.constants import K_FFT_FEATURES, FFT_FEATURE_ENABLED, FEATURE_ORDER, MODEL_PATH
import xgboost as xgb
import joblib


def train_and_save():
    print("Building dataset...")
    X, y = build_dataset(feature_order=FEATURE_ORDER, fft_feature=FFT_FEATURE_ENABLED,
                         k_fft_features=K_FFT_FEATURES)
    X_train, y_train, X_test, y_test = split_dataset(X, y)

    print("Training model...")
    model = xgb.XGBClassifier(n_estimators=200, eval_metric='logloss', random_state=392)
    model.fit(X_train, y_train)

    print("Saving model at ", MODEL_PATH)
    joblib.dump(model, MODEL_PATH)


if __name__ == "__main__":
    train_and_save()
