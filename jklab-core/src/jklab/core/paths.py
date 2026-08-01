# =============================================================================
# jklab-core/paths.py
#
# -----------------------------------------------------------------------------
# DESCRIPTION
# -----------------------------------------------------------------------------
# Utilities for filesystem and path management.
#
# The module provides:
# - utilities for validating files and directories;
# - utilities for creating a folder;
# - utilities for listing files and directories;
#
# -----------------------------------------------------------------------------
# DEPENDENCIES
# -----------------------------------------------------------------------------
# - pathlib : for the Path class.
#
# - jklab.core.exceptions : for error handling.
#
# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------
# Functions:
# - validate_file : Validate a path to a file.
# - validate_dir  : Validate a path to a directory.
# - ensure_dir    : Ensure the existence of a directory.
# - list_files    : List all files in a directory.
# - list_dirs     : List all directories contained in a directory.
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

from pathlib import Path

import jklab.core.exceptions as jkex

# =============================================================================
# Type alias
# =============================================================================

PathLike = str | Path

# =============================================================================
# Functions
# =============================================================================
# -----------------------------------------------------------------------------
# Validation functions
# -----------------------------------------------------------------------------

def validate_file(
    file_path: PathLike
) -> bool:
    """
    Validate that the given path points to a file.

    Parameters
    ----------
    file_path : PathLike
        Path to the file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.

    IsADirectoryError
        If the path points to a directory.

    ValueError
        If the path exists but does not point to a file.

    Returns
    -------
    bool
        True if file is validated.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        jkex.raise_error(
            error=FileNotFoundError,
            message="File does not exist.",
            context={"path": file_path}
        )

    if file_path.is_file():

        return True

    if file_path.is_dir():
        jkex.raise_error(
            error=IsADirectoryError,
            message="Path points to a directory, not a file.",
            context={"path": file_path}
        )

    jkex.raise_error(
        error=ValueError,
        message="Path exists but does not point to a regular file.",
        context={"path": file_path}
    )


def validate_dir(
    dir_path: PathLike
) -> bool:
    """
    Validate that the given path points to a directory.

    Parameters
    ----------
    dir_path : PathLike
        Path to the directory.

    Raises
    ------
    FileNotFoundError
        If the directory does not exist.

    NotADirectoryError
        If the path points to a file.

    ValueError
        If the path exists but does not point to a directory.

    Returns
    -------
    bool
        True if directory is validated.
    """

    dir_path = Path(dir_path)

    if not dir_path.exists():
        jkex.raise_error(
            error=FileNotFoundError,
            message="Directory does not exist.",
            context={"path": dir_path}
        )

    if dir_path.is_dir():

        return True

    if dir_path.is_file():
        jkex.raise_error(
            error=NotADirectoryError,
            message="Path points to a file, not a directory.",
            context={"path": dir_path}
        )

    jkex.raise_error(
        error=ValueError,
        message="Path exists but does not point to a directory.",
        context={"path": dir_path}
    )

# -----------------------------------------------------------------------------
# Construction functions
# -----------------------------------------------------------------------------

def ensure_dir(
    dir_path: PathLike
) -> None:
    """
    Create a directory if it does not already exist.

    Parameters
    ----------
    dir_path : PathLike
        Directory path.

    Returns
    -------
    None
    """

    dir_path = Path(dir_path)

    dir_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return None

# -----------------------------------------------------------------------------
# Listing functions
# -----------------------------------------------------------------------------

def list_files(
    dir_path: PathLike
) -> list[Path]:
    """
    Return a sorted list of files contained in a directory.

    Parameters
    ----------
    dir_path : PathLike
        Directory path.

    Returns
    -------
    list[Path]
        Sorted file list.
    """

    dir_path = Path(dir_path)

    validate_dir(dir_path)

    sorted_file_list = sorted([
        item for item in dir_path.iterdir()
        if item.is_file()
    ])

    return sorted_file_list


def list_dirs(
    dir_path: PathLike
) -> list[Path]:
    """
    Return a sorted list of directories contained in a directory.

    Parameters
    ----------
    dir_path : PathLike
        Directory path.

    Returns
    -------
    list[Path]
        Sorted directory list.
    """

    dir_path = Path(dir_path)

    validate_dir(dir_path)

    sorted_dir_list = sorted([
        item for item in dir_path.iterdir()
        if item.is_dir()
    ])

    return sorted_dir_list

# =============================================================================