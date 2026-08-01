# ==========================================================
# statistics.py
#
# Basic statistical utilities.
#
# This module provides simple statistical functions that are
# independent of any specific application or data format.
#
# Condition convention
# --------------------
# Conditions always define VALID entries.
#
# Entries not satisfying the condition are ignored when
# computing statistics.
#
# ==========================================================

import numpy as np

# ==========================================================
# INTERNAL UTILITIES
# ==========================================================

def _apply_condition(
    data,
    condition=None
) -> np.ndarray:
    """
    Apply a validity condition to data.

    Entries not satisfying the condition are replaced
    by NaN so that NumPy nan-aware statistics can ignore
    them while preserving the array shape.

    Parameters
    ----------
    data : array-like
        Input data.

    condition : callable, optional
        Function returning a boolean mask.

    Returns
    -------
    numpy.ndarray
        Conditioned array.
    """

    data = np.asarray(
        data,
        dtype=float
    )

    if condition is None:
        return data

    mask = condition(data)

    return np.where(
        mask,
        data,
        np.nan
    )

# ==========================================================
# STATISTICS
# ==========================================================

def mean(
    data,
    axis=None,
    condition=None
) -> np.ndarray:
    """
    Compute mean.

    Parameters
    ----------
    data : array-like
        Input data.

    axis : int, tuple, or None, optional
        Axis along which the statistic is computed.

    condition : callable, optional
        Valid-data condition.

    Returns
    -------
    numpy.ndarray
        Mean values.
    """

    data = _apply_condition(
        data,
        condition=condition
    )

    return np.nanmean(
        data,
        axis=axis
    )


def var(
    data,
    axis=None,
    condition=None,
    ddof=0
) -> np.ndarray:
    """
    Compute variance.

    Parameters
    ----------
    data : array-like
        Input data.

    axis : int, tuple, or None, optional
        Axis along which the statistic is computed.

    condition : callable, optional
        Valid-data condition.

    ddof : int, optional
        Delta degrees of freedom.

    Returns
    -------
    numpy.ndarray
        Variance values.
    """

    data = _apply_condition(
        data,
        condition=condition
    )

    return np.nanvar(
        data,
        axis=axis,
        ddof=ddof
    )


def std(
    data,
    axis=None,
    condition=None,
    ddof=0
) -> np.ndarray:
    """
    Compute standard deviation.

    Parameters
    ----------
    data : array-like
        Input data.

    axis : int, tuple, or None, optional
        Axis along which the statistic is computed.

    condition : callable, optional
        Valid-data condition.

    ddof : int, optional
        Delta degrees of freedom.

    Returns
    -------
    numpy.ndarray
        Standard-deviation values.
    """

    data = _apply_condition(
        data,
        condition=condition
    )

    return np.nanstd(
        data,
        axis=axis,
        ddof=ddof
    )


def sem(
    data,
    axis=None,
    condition=None
) -> np.ndarray:
    """
    Compute standard error of the mean (SEM).

    Notes
    -----
    Uses the unbiased sample standard deviation
    (ddof=1).

    Parameters
    ----------
    data : array-like
        Input data.

    axis : int, tuple, or None, optional
        Axis along which the statistic is computed.

    condition : callable, optional
        Valid-data condition.

    Returns
    -------
    numpy.ndarray
        SEM values.
    """

    data = _apply_condition(
        data,
        condition=condition
    )

    n_valid = np.sum(
        ~np.isnan(data),
        axis=axis
    )

    std_val = np.nanstd(
        data,
        axis=axis,
        ddof=1
    )

    return std_val / np.sqrt(
        n_valid
    )

# ==========================================================