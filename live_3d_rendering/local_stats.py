import numpy as np


def get_window(ar, centerx, centery, rx, ry):
    return ar[centerx - rx : centerx + rx + 1, centery - ry : centery + ry + 1]


def build_hover_data(ar, rx=25, ry=25):
    mins = np.zeros(ar.shape)
    maxs = np.zeros(ar.shape)
    means = np.zeros(ar.shape)
    variances = np.zeros(ar.shape)
    nrows, ncols = ar.shape
    for centerx in range(rx, ncols - rx):
        for centery in range(ry, nrows - ry):
            window = get_window(ar, centerx, centery, rx, ry)
            mins[centerx, centery] = window.min()
            maxs[centerx, centery] = window.max()
            means[centerx, centery] = window.mean()
            variances[centerx, centery] = window.var()
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
