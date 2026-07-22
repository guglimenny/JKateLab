# ==========================================================
# io.py
#
# Input-output (IO) utilities used by my_basic_lib.
#
# This module provides a centralized interface for loading
# and saving data files. Functions defined here should be
# generic and independent of any project-specific naming
# conventions or data structures.
#
# ==========================================================

import numpy as np

# ==========================================================
# TEXT FILES

def load_txt(
    path,
    dtype=float,
    skiprows=0,
    skipdata=0,
    usecols=None
) -> np.ndarray:
    """
    Load data from a text file.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the file.

    dtype : data-type, optional
        Desired data type of the returned array.

    skiprows : int, optional
        Number of lines to skip at the beginning of the file.

    skipdata : int, optional
        Number of lines to skip when returning the loaded data.

    Returns
    -------
    ndarray
        Loaded data array.
    """

    return np.loadtxt(
        fname=path,
        dtype=dtype,
        skiprows=skiprows,
        usecols=usecols
    )[skipdata:]


def save_txt(
    path,
    data,
    dfmt="%.18e",
    header="",
    columns=False
) -> None:
    """
    Save data to a text file.

    Parameters
    ----------
    path : str or pathlib.Path
        Output file path.

    data : array-like
        Data to save.

    dfmt : str, optional
        Format string used for writing numerical values.

    header : str, optional
        Header written at the beginning of the file.

    columns : bool, optional
        If True and data is two-dimensional, the first axis
        is interpreted as columns and the array is transposed
        before saving.

        Example
        -------
        data = [x, y]

        is written as

            x[0]  y[0]
            x[1]  y[1]
            ...
            
        when columns=True.

    Returns
    -------
    None
    """

    data = np.asarray(data)

    if (
        columns
        and data.ndim == 2
    ):
        data = data.T

    np.savetxt(
        fname=path,
        X=data,
        fmt=dfmt,
        header=header
    )

    return None

# ==========================================================