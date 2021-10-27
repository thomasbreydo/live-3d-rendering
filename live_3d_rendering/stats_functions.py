from collections import Callable

import numpy as np

StatsFunc = Callable[[np.ndarray], float]


def fmt(s: str):
    def wrapper(func):
        func.fmt = s
        return func

    return wrapper


@fmt("Min: %d")
def local_min(window: np.ndarray) -> float:
    return window.min()  # noqa: call args


@fmt("Variance: %.2f")
def local_variance(window: np.ndarray) -> float:
    return window.var()


@fmt("Max: %d")
def local_max(window: np.ndarray) -> float:
    return window.max()  # noqa: call args


@fmt("Mean: %.2f")
def local_mean(window: np.ndarray) -> float:
    return window.mean()
