# ==========================================================
# qmep_scan.py
#
# QMEP scan-file utilities.
#
# This module provides utilities to:
#
# - list available scans
# - load scan files
# - convert scan entries into Case objects
#
# Scan files are intended to be human-readable and define
# a set of simulation cases sharing common parameters
# (typically N and age) while scanning over epst values.
#
# ==========================================================

from pathlib import Path

from .qmep_case import Case

# ==========================================================
# SCAN DISCOVERY
# ==========================================================

SCAN_PREFIX = "scan_"


def list_scans(scan_dir):
    """
    List available scan files.

    Parameters
    ----------
    scan_dir : str or pathlib.Path
        Directory containing scan files.

    Returns
    -------
    list[str]
        Sorted list of scan names (without extension).

    Notes
    -----
    Only files whose names start with SCAN_PREFIX are
    returned.
    """

    scan_dir = Path(scan_dir)

    return sorted(
        path.stem
        for path in scan_dir.iterdir()
        if (
            path.is_file()
            and path.stem.startswith(SCAN_PREFIX)
        )
    )

# ==========================================================
# SCAN LOADING
# ==========================================================


def load_scan(
    scan_dir,
    scan_name
):
    """
    Load a scan file and return its list of cases.

    Parameters
    ----------
    scan_dir : str or pathlib.Path
        Directory containing scan files.

    scan_name : str
        Scan file name without extension.

    Returns
    -------
    list[Case]
        List of Case objects defined in the scan.

    Raises
    ------
    FileNotFoundError
        If the requested scan file is not found.

    ValueError
        If the scan file is malformed.
    """

    scan_dir = Path(scan_dir)

    scan_path = scan_dir / f"{scan_name}.txt"

    if not scan_path.is_file():

        available_scans = list_scans(scan_dir)

        raise FileNotFoundError(
            "in [load_scan], scan file not found:\n"
            f"scan_name = '{scan_name}'\n\n"
            f"Available scans:\n"
            + "\n".join(available_scans)
        )

    return _parse_scan_file(scan_path)

# ==========================================================
# INTERNAL HELPERS
# ==========================================================


def _parse_scan_file(scan_path):
    """
    Parse a scan file.

    Expected structure
    ------------------

    N:
    32

    age:
    800

    epst:
    0.01000,
    0.02000,
    0.03000

    Parameters
    ----------
    scan_path : pathlib.Path

    Returns
    -------
    list[Case]
    """

    with open(scan_path, "r") as file:

        lines = file.readlines()

    N = None
    age = None

    epst_list = []

    section = None

    for line in lines:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip comments
        if line.startswith("#"):
            continue

        # Section headers
        if line == "N:":

            section = "N"
            continue

        elif line == "age:":

            section = "age"
            continue

        elif line == "epst:":

            section = "epst"
            continue

        # Section content
        if section == "N":

            N = int(line)

        elif section == "age":

            age = int(line)

        elif section == "epst":

            values = line.split(",")

            for value in values:

                value = value.strip()

                if value:

                    epst_list.append(
                        float(value)
                    )

    # Validation
    if N is None:

        raise ValueError(
            f"Missing 'N' section in:\n{scan_path}"
        )

    if age is None:

        raise ValueError(
            f"Missing 'age' section in:\n{scan_path}"
        )

    if len(epst_list) == 0:

        raise ValueError(
            f"No epst values found in:\n{scan_path}"
        )

    return [
        Case(
            N=N,
            age=age,
            epst=epst
        )
        for epst in epst_list
    ]

# ==========================================================