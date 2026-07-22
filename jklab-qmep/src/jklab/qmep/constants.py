# ==========================================================
# qmep_constants.py
#
# General constants, naming conventions, and file naming
# utilities used throughout qmep_analysis_lib.
#
# This module acts as the single source of truth for QMEP
# file names, directory names, and strain-amplitude
# formatting conventions.
#
# ==========================================================

from my_basic_lib import exceptions as mex

# ==========================================================
# PROGRAM CONSTANTS

PROGRAM_NAME = "cyclic_shear"

INPUT_FILE_NAME_PREFIX = "cyclic_shear_input_"

# ==========================================================
# COMMON LABELS

LABEL_EPST = "\\epsilon_t"
LABEL_HYST = "\\epsilon_{hyst}"
LABEL_IRR  = "\\epsilon_{irr}"

COLOR_HYST = "xkcd:green"
COLOR_IRR  = "xkcd:red"

# ==========================================================
# EPST CONSTANTS

EPST_DIGITS = 5

EPST_PERCENT_DIGITS = EPST_DIGITS - 2


def epst_to_int(epst, digits=EPST_DIGITS):
    """
    Convert strain amplitude to integer representation.

    Examples
    --------
    0.0100 -> 1000
    0.0530 -> 5300
    """

    return round(epst * 10**digits)


def epst_to_float_string(epst, digits=EPST_DIGITS):
    """
    Convert strain amplitude to fixed-point string.
    """

    return f"{epst:.{digits}f}"


def epst_to_percentage_string(
    epst,
    digits=EPST_PERCENT_DIGITS
):
    """
    Convert strain amplitude to percentage string.

    Examples
    --------
    0.0100 -> '1.000%'
    0.0530 -> '5.300%'
    """

    return f"{epst:.{digits}%}"


def epst_to_label(
    epst,
    digits=EPST_DIGITS
):
    """
    Convert strain amplitude to folder label.

    Examples
    --------
    0.0100 -> 'epst01000'
    0.0530 -> 'epst05300'
    """

    epst_int = epst_to_int(epst)

    return f"epst{epst_int:0{digits}d}"


# ==========================================================
# DIRECTORY CONSTANTS

DIR_PREFIX_CONFIG_DATA = "config_data_"

DIR_NAME_TRANSIENT_DATA = "transient_data"

# ==========================================================
# FILE CONSTANTS

# Summary files.
FILE_PREFIX_CYCLES = "cycles"

# Transient files.
FILE_PREFIX_SCALAR      = "scalar-permanent"
FILE_PREFIX_EVENT       = "event"
FILE_PREFIX_TRAP_PLUS   = "trap-plus"
FILE_PREFIX_TRAP_MINUS  = "trap-moinsf"
FILE_PREFIX_STRESS      = "stress"
FILE_PREFIX_PLASTIC_DEF = "def-pl"

# Branch suffix appended to filenames.
#
# ""  : standard (parallel) protocol
# "p" : ascending branch of a sequential protocol
# "m" : descending branch of a sequential protocol
VALID_BRANCHES = ("", "p", "m")

# Cycle points labels. 
#
# This labels identify the cycle point the system
# goes through during training. They're hardcoded
# in the QMEP 'cyclic_shear.f90' file.

POINT_LABEL_LIST = (
    "Y",
    "Tp",
    "X",
    "T",
)

# ==========================================================
# LABELS MANAGEMENT

def get_last_cycle_layout(
    french_cycle,
    n_dump_last,
    point_label_list=POINT_LABEL_LIST,
):
    """
    Return the mapping between logical configuration names
    and dumped files required to reconstruct the last cycle.

    Parameters
    ----------
    french_cycle : int
        Total number of completed cycles.

    n_dump_last : int
        Size of the last-cycle dump buffer.

    point_label_list : sequence of str, optional
        Ordered labels identifying the configurations within
        one cycle. The default corresponds to
        qc.POINT_LABEL_LIST.

    Returns
    -------
    dict
        Dictionary mapping logical configuration names to
        (cycle_point_label, cycle_idx) tuples.

        If only one cycle is available, the previous
        configuration is taken from the aged configuration
        'A0'. Otherwise it is taken from 'T-2'.
    """

    n_stored = min(french_cycle, n_dump_last)

    if n_stored < 1:
        mex.raise_error(
            error_type="value",
            module_name="qmep_loader",
            function_name="get_last_cycle_layout",
            message="No dumped cycles available",
            french_cycle=french_cycle,
            n_dump_last=n_dump_last,
        )

    layout = {}

    if n_stored == 1:
        layout["A"] = ("A", 0)
    else:
        layout["A"] = (point_label_list[-1], -2)

    for label in point_label_list:
        layout[label] = (label, -1)

    return layout

# ==========================================================
# FILE NAMING UTILITIES

def _validate_branch(branch):
    if branch not in VALID_BRANCHES:
        mex.raise_error(
            error_type="value",
            module_name="qmep_constants",
            function_name="_validate_branch",
            message="Invalid branch",
            branch=branch,
            valid_branches=VALID_BRANCHES,
        )


def build_cycles_filename(
    N,
    age,
    epst,
    branch=""
):
    """
    Build the cycles summary filename.

    Parameters
    ----------
    branch : {"", "p", "m"}, default=""
        Optional suffix identifying the branch of a sequential
        training protocol.

            "" : standard (parallel) protocol
            "p": ascending branch
            "m": descending branch

    Examples
    --------
    Parallel
        cycles_N32_age800_g1000.out

    Sequential (ascending)
        cycles_N32_age800_g1000p.out

    Sequential (descending)
        cycles_N32_age800_g1000m.out
    """

    _validate_branch(branch)

    epst_int = epst_to_int(epst)

    return (
        f"{FILE_PREFIX_CYCLES}_"
        f"N{N}_age{age}_g{epst_int}{branch}.out"
    )


def build_transient_filename(
    file_type,
    epst,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    branch=""
):
    """
    Build a transient configuration filename.

    Parameters
    ----------
    branch : {"", "p", "m"}, default=""
        Optional suffix identifying the branch of a sequential
        training protocol.

    Examples
    --------
    Parallel
        event_g1000_rea1_T_c-1.dat

    Sequential (ascending)
        event_g1000_rea1_T_c-1p.dat

    Sequential (descending)
        event_g1000_rea1_T_c-1m.dat
    """

    _validate_branch(branch)

    epst_int = epst_to_int(epst)

    return (
        f"{file_type}_g{epst_int}{branch}_"
        f"rea{rea_idx + 1}_"
        f"{cycle_point_label}_"
        f"c{cycle_idx}.dat"
    )