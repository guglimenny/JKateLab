# ==========================================================
# paths.py
#
# Filesystem and path utilities used by my_basic_lib.
#
# This module provides generic utilities for validating,
# creating, and listing files and directories.
#
# ==========================================================

import pathlib as pl

from . import exceptions as mex

# ==========================================================
# VALIDATION

def validate_file(path):
    """
    Check that a file exists.

    Parameters
    ----------
    path : str or pathlib.Path
        File path.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """

    path = pl.Path(path)

    if not path.is_file():
        mex.raise_error(
            error_type="value",
            module_name="paths",
            function_name="validate_file",
            message="File not found",
            path=path
        )

    return None


def validate_dir(path):
    """
    Check that a directory exists.

    Parameters
    ----------
    path : str or pathlib.Path
        Directory path.

    Raises
    ------
    FileNotFoundError
        If the directory does not exist.
    """

    path = pl.Path(path)

    if not path.is_dir():
        mex.raise_error(
            error_type="file",
            module_name="paths",
            function_name="validate_dir",
            message="Directory not found",
            path=path
        )

    return None

# ==========================================================
# CONSTRUCTION

def ensure_dir(path):
    """
    Create a directory if it does not already exist.

    Parameters
    ----------
    path : str or pathlib.Path
        Directory path.
    """

    path = pl.Path(path)

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return None


# ==========================================================
# LISTING

def list_files(path):
    """
    Return a sorted list of files contained in a directory.

    Parameters
    ----------
    path : str or pathlib.Path
        Directory path.

    Returns
    -------
    list[pathlib.Path]
        Sorted file list.
    """

    path = pl.Path(path)

    validate_dir(path)

    return sorted(
        [
            item
            for item in path.iterdir()
            if item.is_file()
        ]
    )


def list_subdirs(path):
    """
    Return a sorted list of subdirectories contained in a
    directory.

    Parameters
    ----------
    path : str or pathlib.Path
        Directory path.

    Returns
    -------
    list[pathlib.Path]
        Sorted subdirectory list.
    """

    path = pl.Path(path)

    validate_dir(path)

    return sorted(
        [
            item
            for item in path.iterdir()
            if item.is_dir()
        ]
    )

# ==========================================================