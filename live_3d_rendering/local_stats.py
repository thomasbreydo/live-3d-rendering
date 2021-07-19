import numpy as np

DEFAULT_RX = 2
DEFAULT_RY = 2


def get_window(ar, centerx, centery, rx, ry):
    return ar[centerx - rx : centerx + rx + 1, centery - ry : centery + ry + 1]


def build_hover_data(ar, rx=None, ry=None):
    if rx is None:
        rx = DEFAULT_RX
    if ry is None:
        ry = DEFAULT_RY
    mins = np.zeros(ar.shape)
    maxs = np.zeros(ar.shape)
    means = np.zeros(ar.shape)
    variances = np.zeros(ar.shape)
    nrows, ncols = ar.shape
    for row in range(rx, nrows - rx):
        for col in range(ry, ncols - ry):
            window = get_window(ar, row, col, rx, ry)
            mins[row, col] = window.min()
            maxs[row, col] = window.max()
            means[row, col] = window.mean()
            variances[row, col] = window.var()
    return np.stack((mins, maxs, means, variances), axis=-1)


# def windows(ar, width=50, height=50):
#     """Iterate over windows in ar.
#
#     Args:
#         ar: array from which to take windows
#         width: width of window (always odd, +1 if even)
#         height: height of window (always odd, +1 if even)
#
#     Returns:
#         An iterator over windows of ar with dimensions width x height.
#     """
#
#     nrows, ncols = ar.shape
#     for cx in range(rx, ncols - rx):
#         for centery in range(ry, nrows - ry):
#             yield ar[cx - rx : cx + rx + 1, centery - ry : centery + ry + 1]
