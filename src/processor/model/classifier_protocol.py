from typing import Protocol

import numpy as np
from numpy.typing import ArrayLike


class ClassifierProtocol(Protocol):
    def fit(self, X: ArrayLike, y: ArrayLike) -> "ClassifierProtocol": ...
    def predict(self, X: ArrayLike) -> np.ndarray: ...
