# ==========================================================
# qmep_paths.py
#
# QMEP filesystem and directory structure utilities.
#
# This module centralizes all QMEP-specific path and
# directory naming conventions.
#
# Paths are composed of:
#
# - simulation root directory
# - case directory (N, age, epst)
# - batch directory
# - optional filename modifiers:
#     * epst_file   (sequential protocol)
#     * branch (sequential protocol)
# ==========================================================

from pathlib import Path

from qmep_analysis_lib import qmep_constants as qc

# ==========================================================

def build_case_path(
    simulation_data_dir,
    case
):
    """
    Build path to a QMEP case directory.

    Directory structure:

    simulation_data/
        N<case.N>/
            age<case.age>/
                epst<case.epst>

    Parameters
    ----------
    simulation_data_dir : str or pathlib.Path
        Root simulation-data directory.

    case : qph.Case
        QMEP simulation case.

    Returns
    -------
    pathlib.Path
        Case directory path.
    """

    return (
        Path(simulation_data_dir)
        / case.case_label
    )


def build_batch_path(
    simulation_data_dir,
    case,
    batch
):
    """
    Build path to a QMEP batch directory.

    Parameters
    ----------
    simulation_data_dir : str or pathlib.Path
        Root simulation-data directory.

    case : qph.Case
        QMEP simulation case.

    batch : str
        Batch name.

    Returns
    -------
    pathlib.Path
        Batch directory path.
    """

    return (
        build_case_path(
            simulation_data_dir,
            case
        )
        / batch
    )


def build_cycles_path(
    simulation_data_dir,
    case,
    batch,
    epst_file=None,
    branch=""
):
    """
    Build the path to a cycles summary file.

    By default, the filename is built using 'case.epst',
    which corresponds to the standard (parallel) protocol.

    For sequential protocols, 'epst_file' may specify a different
    training amplitude while the directory remains determined
    by 'case'.

    Parameters
    ----------
    simulation_data_dir : str or pathlib.Path
        Root simulation-data directory.

    case : qmep_case.Case
        Simulation case identifying the directory.

    batch : str
        Batch name.

    epst_file : float, optional
        Strain amplitude encoded in the filename.
        If None, uses 'case.epst'.

    branch : {"", "p", "m"}, default=""
        Sequential protocol branch.

    Returns
    -------
    pathlib.Path
        Path to the cycles summary file.
    """

    if epst_file is None:
        epst_file = case.epst

    return (
        build_batch_path(
            simulation_data_dir,
            case,
            batch
        )
        / qc.build_cycles_filename(
            case.N,
            case.age,
            epst=epst_file,
            branch=branch
        )
    )


# NOTE: to be done
def build_config_dir_path(
    simulation_data_dir,
    case,
    batch,
    protocol
):
    """
    Build path to configuration-data directory.
    """

    return (
        build_batch_path(
            simulation_data_dir,
            case,
            batch
        )
        / (
            f"{qc.DIR_PREFIX_CONFIG_DATA}"
            f"{protocol}_"
            f"{case.epst_label}"
        )
    )


def build_transient_dir_path(
    simulation_data_dir,
    case,
    batch
):
    """
    Build path to transient-data directory.
    """

    return (
        build_batch_path(
            simulation_data_dir,
            case,
            batch
        )
        / qc.DIR_NAME_TRANSIENT_DATA
    )