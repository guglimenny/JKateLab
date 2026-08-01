# =============================================================================
# jklab-core/statistics.py
#
# -----------------------------------------------------------------------------
# DESCRIPTION
# -----------------------------------------------------------------------------
# Utilities for computing statistics over multidimensional arrays with
# optional masking.
#
# The module provides:
# - a private helper for applying boolean masks to data;
# - utilities for computing mean, variance, standard deviation, and standard
#   error of the mean over selected axes.
#
# -----------------------------------------------------------------------------
# DEPENDENCIES
# -----------------------------------------------------------------------------
# - numpy : for array conversion, masking, and NaN-aware statistical
#   functions.
#
# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------
# Functions:
# - compute_mean : Compute the mean of numerical data with optional axis
#   selection and masking.
# - compute_var  : Compute the variance of numerical data with optional axis
#   selection, masking, and choice of degrees of freedom.
# - compute_std  : Compute the standard deviation of numerical data with
#   optional axis selection, masking, and choice of degrees of freedom.
# - compute_sem  : Compute the standard error of the mean of numerical data
#   with optional axis selection and masking.
#
# -----------------------------------------------------------------------------
# IMPLEMENTATION NOTES
# -----------------------------------------------------------------------------
# - _apply_mask() preserves the shape of the original data array by replacing
#   entries that do not satisfy the mask with np.nan. Consequently:
#   1. Integer array-like inputs are promoted to floating-point arrays when
#      a mask is applied.
#   2. Pre-existing NaN values are ignored by the NaN-aware statistical
#      functions and should therefore be handled explicitly by the caller
#      when their presence indicates invalid or unexpected data.
#
# - compute_var() and compute_std() allow the choice of delta degrees of
#   freedom (ddof).
#
# - compute_sem() uses the unbiased sample standard deviation (ddof=1).
#
# -----------------------------------------------------------------------------
# MAINTAINER
# -----------------------------------------------------------------------------
# Guglielmo Mennella.
# =============================================================================

# =============================================================================
# Imports
# =============================================================================

import numpy as np

# =============================================================================
# Functions
# =============================================================================

def _apply_mask(
    data,
    mask = None
) -> np.ndarray:
    """
    Apply a boolean mask to data.

    Entries corresponding to False mask values are replaced
    by NaN, preserving the shape of the input array.

    Parameters
    ----------
    data : array-like
        Input data.

    mask : array-like of bool, optional
        Boolean mask used to identify valid data entries.

    Returns
    -------
    numpy.ndarray
        Array with masked entries replaced by NaN.
    """

    data = np.asarray(data)

    if mask is None:
        return data

    filtered_data = np.where(
        mask,
        data,
        np.nan
    )

    return filtered_data


def compute_mean(
    data,
    axis = None,
    mask = None
) -> np.ndarray:
    """
    Compute mean.

    The mask parameter optionally selects the data
    entries included in the computation.

    Parameters
    ----------
    data : array-like
        Input data.

    axis : int, tuple, or None, optional
        Axis along which the statistic is computed.

    mask : array-like of bool, optional
        Valid-data mask.

    Returns
    -------
    numpy.ndarray
        Mean values.
    """

    data = _apply_mask(
        data,
        mask=mask
    )

    mean_value = np.nanmean(
        data,
        axis=axis
    )

    return mean_value


def compute_var(
    data,
    axis = None,
    mask = None,
    ddof = 0
) -> np.ndarray:
    """
    Compute variance.

    Parameters
    ----------
    data : array-like
        Input data.

    axis : int, tuple, or None, optional
        Axis along which the statistic is computed.

    mask : array-like of bool, optional
        Valid-data mask.

    ddof : int, optional
        Delta degrees of freedom.

    Returns
    -------
    numpy.ndarray
        Variance values.
    """

    data = _apply_mask(
        data,
        mask=mask
    )

    var_value = np.nanvar(
        data,
        axis=axis,
        ddof=ddof
    )

    return var_value


def compute_std(
    data,
    axis = None,
    mask = None,
    ddof = 0
) -> np.ndarray:
    """
    Compute standard deviation.

    Notes
    -----
    If the number of valid observations is insufficient for the
    specified ddof, the result is NaN and a RuntimeWarning is issued.

    Parameters
    ----------
    data : array-like
        Input data.

    axis : int, tuple, or None, optional
        Axis along which the statistic is computed.

    mask : array-like of bool, optional
        Valid-data mask.

    ddof : int, optional
        Delta degrees of freedom.

    Returns
    -------
    numpy.ndarray
        Standard-deviation values.
    """

    data = _apply_mask(
        data,
        mask=mask
    )

    std_value = np.nanstd(
        data,
        axis=axis,
        ddof=ddof
    )

    return std_value


def compute_sem(
    data,
    axis = None,
    mask = None
) -> np.ndarray:
    """
    Compute standard error of the mean (SEM).

    Notes
    -----
    Uses the unbiased sample standard deviation (ddof=1).

    Only valid, non-NaN entries contribute to the calculation.
    If fewer than two valid entries are available along a
    reduction axis, the result is NaN.

    Parameters
    ----------
    data : array-like
        Input data.

    axis : int, tuple, or None, optional
        Axis along which the statistic is computed.

    mask : array-like of bool, optional
        Valid-data mask.

    Returns
    -------
    numpy.ndarray
        SEM values.
    """

    data = _apply_mask(
        data,
        mask=mask
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

    sem_value = std_val / np.sqrt(n_valid)

    return sem_value

# =============================================================================