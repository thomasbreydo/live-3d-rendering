from collections import Collection
from dataclasses import dataclass
from typing import Union

from .stats_functions import StatsFunc
import numpy as np

Array2D = Union[list[list[int]], np.ndarray]


@dataclass
class Window:
    """Rectangular window of a 2D array

    Attributes:
        array: Underlying 2D array for this window
        row: row of top left corner of window
        col: column of top left corner of window
        width: width of window
        height: height of window
    """

    array: np.ndarray
    row: int
    col: int
    width: int
    height: int

    @staticmethod
    def relu(n):
        return max(n, 0)

    def access(self):
        return self.array[
            self.relu(self.row) : self.relu(self.row + self.height),
            self.relu(self.col) : self.relu(self.col + self.width),
        ]


def get_local_stats(
    array: Array2D,
    stats_functions: Collection[StatsFunc],
    pixel_row: int,
    pixel_col: int,
    rx: int,
    ry: int,
) -> list[float]:
    """Apply each function in `stats_functions` to a window of `array`

    Args:
        array: 2D array of surface data
        stats_functions: collection of functions that compute local stats
        pixel_row: row index of the center pixel
        pixel_col: column index of the center pixel
        rx: # of pixels to the left of center pixel (width == 2rx + 1)
        ry: # of pixels above the center pixel (height = 2ry + 1)

    Returns:
        A list of local stat results.

    Notes:
        Say this is the 2D `array`:

        .. code-block:: text

              0123456
            0 **...**
            1 **.x.**
            2 **...**

        The 'x' marks (pixel_row, pixel_col), which is (1, 3) in this case.
        rx is 1, ry is 1. The window is from (0, 2).

            0 == pixel_row - ry
            1 == pixel_col - rx
    """
    array = np.asarray(array)
    window = Window(array, pixel_row - ry, pixel_col - rx, 2 * rx + 1, 2 * ry + 1)
    local_array = window.access()
    return [stats_func(local_array) for stats_func in stats_functions]
