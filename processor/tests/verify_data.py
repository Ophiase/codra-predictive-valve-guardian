from processor.data.constants import TRAINING_LIMIT

from ..data.build_dataset import build_dataset, build_raw_dataset, split_dataset


def test_build_raw_dataset() -> None:
    """
    Ensure that the raw dataset can be built and split correctly.
    """
    X, y = build_raw_dataset()
    assert X.shape[0] == y.shape[0], "Number of samples in X and y should be equal"
    print(f"Raw dataset built successfully with {X.shape[0]} samples.")
    X_train, y_train, X_test, y_test = split_dataset(X, y)
    assert (
        X_train.shape[0] == TRAINING_LIMIT
    ), f"Training set should by default have {TRAINING_LIMIT} samples"
    assert (
        y_train.shape[0] == TRAINING_LIMIT
    ), f"Training set should by default have {TRAINING_LIMIT} samples"
    assert (
        X_train.shape[0] + X_test.shape[0] == X.shape[0]
    ), "Train and test split should sum to total samples"
    assert (
        y_train.shape[0] + y_test.shape[0] == y.shape[0]
    ), "Train and test split should sum to total samples"


def test_build_dataset() -> None:
    """
    Ensure that the featured-based dataset can be built and split correctly.
    """
    X, y = build_dataset()
    assert X.shape[0] == y.shape[0], "Number of samples in X and y should be equal"
    print(f"Processed dataset built successfully with {X.shape[0]} samples.")
    X_train, y_train, X_test, y_test = split_dataset(X, y)
    assert (
        X_train.shape[0] == TRAINING_LIMIT
    ), f"Training set should by default have {TRAINING_LIMIT} samples"
    assert (
        y_train.shape[0] == TRAINING_LIMIT
    ), f"Training set should by default have {TRAINING_LIMIT} samples"
    assert (
        X_train.shape[0] + X_test.shape[0] == X.shape[0]
    ), "Train and test split should sum to total samples"
    assert (
        y_train.shape[0] + y_test.shape[0] == y.shape[0]
    ), "Train and test split should sum to total samples"


if __name__ == "__main__":
    test_build_raw_dataset()
    test_build_dataset()
