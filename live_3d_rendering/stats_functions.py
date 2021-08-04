from collections import Callable

import numpy as np

StatsFunc = Callable[[np.ndarray], float]


def local_min(window: np.ndarray) -> float:
    return window.min()  # noqa: call args


def local_variance(window: np.ndarray) -> float:
    return window.var()


def local_max(window: np.ndarray) -> float:
    return window.max()  # noqa: call args


def local_mean(window: np.ndarray) -> float:
    return window.mean()
