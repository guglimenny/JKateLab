# ==========================================================
# qmep_statistics.py
#
# QMEP-specific statistical utilities.
#
# This module provides wrappers around the generic
# statistical functions from my_basic_lib.statistics.
#
# ==========================================================

import numpy as np

from my_basic_lib import exceptions as mex
from my_basic_lib import statistics as mst

# ==========================================================
# PERIOD STATISTICS
# ==========================================================

def compute_period_mean(
    period_mat,
    axis
):
    """
    Compute mean period over successful realizations.

    Success is defined as:

        period > 0
    """

    return mst.mean(
        period_mat,
        axis=axis,
        condition=lambda x: x > 0
    )


def compute_period_var(
    period_mat,
    axis
):
    """
    Compute period variance over successful realizations.
    """

    return mst.var(
        period_mat,
        axis=axis,
        condition=lambda x: x > 0
    )


def compute_period_std(
    period_mat,
    axis
):
    """
    Compute period standard deviation over successful
    realizations.
    """

    return mst.std(
        period_mat,
        axis=axis,
        condition=lambda x: x > 0
    )


def compute_period_sem(
    period_mat,
    axis
):
    """
    Compute period standard error of the mean over
    successful realizations.
    """

    return mst.sem(
        period_mat,
        axis=axis,
        condition=lambda x: x > 0
    )

# ==========================================================
# TRANSIENT STATISTICS
# ==========================================================

def compute_transient_mean(
    transient_mat,
    cycle_number,
    axis
):
    """
    Compute mean transient duration over successful
    realizations.

    Success is defined as:

        transient < cycle_number
    """

    return mst.mean(
        transient_mat,
        axis=axis,
        condition=lambda x: x < cycle_number
    )


def compute_transient_var(
    transient_mat,
    cycle_number,
    axis
):
    """
    Compute transient variance over successful
    realizations.
    """

    return mst.var(
        transient_mat,
        axis=axis,
        condition=lambda x: x < cycle_number
    )


def compute_transient_std(
    transient_mat,
    cycle_number,
    axis
):
    """
    Compute transient standard deviation over successful
    realizations.
    """

    return mst.std(
        transient_mat,
        axis=axis,
        condition=lambda x: x < cycle_number
    )


def compute_transient_sem(
    transient_mat,
    cycle_number,
    axis
):
    """
    Compute transient standard error of the mean over
    successful realizations.
    """

    return mst.sem(
        transient_mat,
        axis=axis,
        condition=lambda x: x < cycle_number
    )

# ==========================================================
# SUCCESS PROBABILITY
# ==========================================================

def compute_success_probability(
    period_mat,
    axis
):
    """
    Compute success probability.

    Notes
    -----
    This function should be applied to period data.

    Success is defined as:

        period > 0

    Using period data is preferred because the success
    criterion is encoded directly in the output and no
    additional simulation parameters are required.
    """

    return np.mean(
        period_mat > 0,
        axis=axis
    )

# ==========================================================
# ACTIVITY RATE
# ==========================================================

def compute_activity_rate(
    field_mat,
    axis
):
    """
    Compute fraction of active sites.

    Active sites are defined as:

        event_field != 0
    """

    return np.mean(
        field_mat != 0,
        axis=axis
    )


def compute_cycle_activity_rate(
    field_cycle_mat,
    cycle_point_axis,
    site_axis
):
    """
    Compute accumulated activity over an entire cycle.

    A site is considered active if it is active at least
    once during the cycle.

    Parameters
    ----------
    event_field_cycle_mat : numpy.ndarray
        Event-field data containing a cycle-point axis.

    cycle_point_axis : int
        Axis corresponding to cycle points.

    site_axis : int
        Axis corresponding to lattice sites.

    Returns
    -------
    numpy.ndarray
        Fraction of sites active at least once during
        the cycle.
    """

    accumulated_event_mat = np.any(
        field_cycle_mat != 0,
        axis=cycle_point_axis
    )

    return np.mean(
        accumulated_event_mat,
        axis=site_axis
    )

# ==========================================================
# VARIATIONAL FIELDS
# ==========================================================

def build_variational_field(config1, config2):

    if config1.shape != config2.shape:
        mex.raise_error(
            error_type="value",
            module_name="qmep_statistics",
            function_name="build_variational_field",
            message=("config1 and config2 must have "
                     "the same shape"),
            config1_shape=config1.shape,
            config2_shape=config2.shape,
        )

    return config2 - config1


def build_variational_field_list(
    config_list,
    axis
) -> np.array:

    nconfig = config_list.shape[axis]

    if nconfig < 2:
        mex.raise_error(
            error_type="value",
            module_name="qmep_statistics",
            function_name="build_variational_field_array",
            message=(
                "configuration axis must contain at least two "
                "configurations"
            ),
            axis=axis,
            nconfig=nconfig,
            array_shape=config_list.shape,
        )

    return np.diff(config_list, axis=axis)

# ==========================================================
# OVERLAP
# ==========================================================

def compute_overlap(
    config1,
    config2
):
    """
    Compute the overlap between two configurations.

    The overlap is defined as the fraction of sites having
    identical values in the two configurations.

        q = (1 / L) * Σ_i δ(config1_i, config2_i)

    where L is the total number of sites and δ is the
    Kronecker delta.

    The input configurations may have any shape, provided
    they are identical. Internally, both arrays are flattened
    before computing the overlap.

    Parameters
    ----------
    config1 : numpy.ndarray
        First configuration.

    config2 : numpy.ndarray
        Second configuration.

    Returns
    -------
    float
        Overlap in the interval [0, 1].

            1.0 : identical configurations.
            0.0 : no matching sites.
    """
    
    if config1.shape != config2.shape:
        mex.raise_error(
            error_type="value",
            module_name="qmep_statistics",
            function_name="compute_overlap",
            message=("config1 and config2 have "
                     "different shapes"),
            config1_shape=config1.shape,
            config2_shape=config2.shape
        )

    config1 = config1.flatten()
    config2 = config2.flatten()

    return np.mean(config1 == config2)


def compute_overlap_matrix(config_list) -> np.ndarray:
    """
    Compute the pairwise overlap matrix for a list of configurations.

    Parameters
    ----------
    config_list : ndarray
        Array of configurations with shape

            (nconfig, ...)
        
        where the trailing dimensions represent a single
        configuration (e.g. (N,N) or (N**2,)).

    Returns
    -------
    ndarray
        Symmetric overlap matrix of shape (nconfig, nconfig).
    """

    config_list = np.asarray(config_list)

    nconfig = config_list.shape[0]

    overlap_mat = np.empty(
        (nconfig, nconfig),
        dtype=float,
    )

    for i in range(nconfig):

        overlap_mat[i, i] = 1.0

        for j in range(i + 1, nconfig):

            overlap = compute_overlap(
                config_list[i],
                config_list[j],
            )

            overlap_mat[i, j] = overlap
            overlap_mat[j, i] = overlap

    return overlap_mat