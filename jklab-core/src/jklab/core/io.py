# =============================================================================
# jklab-core/io.py
#
# -----------------------------------------------------------------------------
# DESCRIPTION
# -----------------------------------------------------------------------------
# Utilities for standardized data input-output (IO).
#
# The module provides:
# - utilities for data loading;
# - utilities for data saving;
#
# -----------------------------------------------------------------------------
# DEPENDENCIES
# -----------------------------------------------------------------------------
# - collections.abc : for the Sequence data type.
# - numpy           : for the array class.
#
# - jklab.core.exceptions : for error handling.
# - jklab.core.paths      : for the PathLike type.
#
# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------
# Functions:
# - load_txt : Load numerical data from a text file.
# - save_txt : Save numerical data to a text file.
#
# -----------------------------------------------------------------------------
# IMPLEMENTATION NOTES
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# MAINTAINER
# -----------------------------------------------------------------------------
# Guglielmo Mennella.
# =============================================================================

# =============================================================================
# Imports
# =============================================================================

from collections.abc import Sequence
import numpy as np

import jklab.core.exceptions as jkex
from jklab.core.paths import PathLike

# =============================================================================
# Functions
# =============================================================================
# -----------------------------------------------------------------------------
# Loading functions
# -----------------------------------------------------------------------------

def load_txt(
    path: PathLike,
    dtype = float,
    skiprows: int = 0,
    usecols: int | Sequence[int] | None = None,
    start: int | None = None,
    stop: int | None = None,
) -> np.ndarray:
    """
    Load data from a text file.

    Parameters
    ----------
    path : PathLike
        Path to the file.

    dtype : optional
        Desired data type of the returned array.

    skiprows : int, optional
        Number of lines to skip at the beginning of the file.

    usecols : int or sequence of int, optional
        Columns to read from the input file.

    start : int, optional
        Starting index of the returned data slice.

    stop : int, optional
        Stopping index of the returned data slice (exclusive).

    Returns
    -------
    ndarray
        Loaded data array.
    """

    loaded_data = np.loadtxt(
        fname=path,
        dtype=dtype,
        skiprows=skiprows,
        usecols=usecols
    )

    return loaded_data[start:stop]

# -----------------------------------------------------------------------------
# Saving functions
# -----------------------------------------------------------------------------

def _format_may_lose_data(
    data: np.ndarray,
    dfmt: str,
) -> bool:
    """
    Check whether the format may cause loss of numerical information.

    Parameters
    ----------
    data : np.ndarray
        Data to process.

    dfmt : str
        Format.

    Returns
    -------
    bool
        True if dfmt causes information loss; False otherwise.
    """

    is_float_data = np.issubdtype(
        data.dtype,
        np.floating
    )

    is_integer_format = (
        "d" in dfmt
    )

    return (
        is_float_data
        and is_integer_format
    )


def save_txt(
    path: PathLike,
    data,
    dfmt: str = "%.18e",
    header: str = "",
    transpose: bool = False,
) -> None:
    """
    Save data to a text file.

    Parameters
    ----------
    path : PathLike
        Output file path.

    data : array-like
        Data to save.

    dfmt : str, optional
        Format string used for writing numerical values.

    header : str, optional
        Header written at the beginning of the file.

    transpose : bool, optional
        If True, the two-dimensional data array is transposed before saving.

        Example
        -------
        data = [x, y]

        is written as

            x[0]  y[0]
            x[1]  y[1]
            ...
            
        when transpose=True.

    Returns
    -------
    None
    """

    data = np.asarray(data)

    if _format_may_lose_data(data, dfmt):

        jkex.raise_warning(
            warning=UserWarning,
            message=(
                "Integer formatting may cause loss of "
                "numerical information."
            ),
            context={
                "data.dtype": data.dtype,
                "dfmt": dfmt,
            }
        )

    if transpose:

        if data.ndim == 2:
            data = data.T

        else:
            jkex.raise_error(
                error=ValueError,
                message="transpose=True requires two-dimensional data.",
                context={"data.ndim": data.ndim}
            )

    np.savetxt(
        fname=path,
        X=data,
        fmt=dfmt,
        header=header
    )

    return None

# =============================================================================