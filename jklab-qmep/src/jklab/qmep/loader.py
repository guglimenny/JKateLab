# ==========================================================
# qmep_loader.py
#
# High-level QMEP data loading interface.
#
# This module connects QMEP path conventions with low-level
# IO utilities.
#
# ==========================================================

# ==========================================================
# IMPORTS
# ==========================================================

import math

from my_basic_lib import io

from qmep_analysis_lib import qmep_constants as qc
from qmep_analysis_lib import qmep_paths as qph

# ==========================================================
# FIELD RESHAPE
# ==========================================================

def reshape_square_grid(data):
    """
    Reshape a 1D field into a square grid.

    Parameters
    ----------
    data : numpy.ndarray
        One-dimensional field data.

    Returns
    -------
    numpy.ndarray
        Square grid with shape (N, N).

    Raises
    ------
    ValueError
        If data size is not a perfect square.
    """

    size = data.size

    N = math.isqrt(size)

    if N * N != size:

        raise ValueError(
            f"Cannot reshape array of size "
            f"{size} into a square grid."
        )

    return data.reshape(N, N)

# ==========================================================
# CYCLES
# ==========================================================

def load_cycles(
    simulation_data_path,
    case,
    batch,
    epst_file=None,
    branch="",
    rea_num=None,
):
    """
    Load cycles summary file.

    Notes
    -----
    Columns are hardcoded and assumed fixed by the QMEP
    output format.

    Parameters
    ----------
    simulation_data_path : str or pathlib.Path
        Root simulation-data directory.

    case : Case
        QMEP simulation case.

    batch : str
        Batch name.

    epst_file : float or None, optional
        Strain amplitude encoded in the cycles filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.
        The default ("") corresponds to the standard
        parallel protocol.

    rea_num : int or None, optional
        Number of realizations to load. If None, all
        available realizations are loaded.

    Returns
    -------
    numpy.ndarray
        Array containing cycle indices and cycle-point
        indices extracted from the cycles summary file.
    """

    path = qph.build_cycles_path(
        simulation_data_path,
        case,
        batch,
        epst_file=epst_file,
        branch=branch,
    )

    data = io.load_txt(
        path,
        dtype=int,
        usecols=(1, 2)
    )

    if rea_num is not None:
        data = data[:rea_num]

    return data

# ==========================================================
# TRANSIENT DATA
# ==========================================================

def get_transient_file_path(
    simulation_data_path,
    case,
    batch,
    file_type,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    epst_file=None,
    branch="",
    set_idx=0
):
    """
    Return full path to a transient-data file.

    Parameters
    ----------
    simulation_data_path : str or pathlib.Path
        Root simulation-data directory.

    case : Case
        QMEP simulation case.

    batch : str
        Batch name.

    file_type : str
        Transient file type.

    rea_idx : int
        Realization index (0-based).

    cycle_point_label : str
        Cycle-point label.

    cycle_idx : int
        Cycle index.

    epst_file : float or None, optional
        Strain amplitude encoded in the cycles filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.
        The default ("") corresponds to the standard
        parallel protocol.

    set_idx : int, optional
        Set index. Default is 0.

    Returns
    -------
    pathlib.Path
        Full path to transient-data file.
    """

    if epst_file is None:
        epst_file = case.epst

    return (
        qph.build_transient_dir_path(
            simulation_data_dir=simulation_data_path,
            case=case,
            batch=batch
        )
        / f"run_{rea_idx + 1}"
        / f"set_{set_idx}"
        / qc.build_transient_filename(
            file_type=file_type,
            epst=epst_file,
            rea_idx=rea_idx,
            cycle_point_label=cycle_point_label,
            cycle_idx=cycle_idx,
            branch=branch
        )
    )


def load_transient_file(
    simulation_data_path,
    case,
    batch,
    file_type,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    epst_file=None,
    branch="",
    set_idx=0,
    dtype=float,
    usecols=None
):
    """
    Load a transient-data file.

    Parameters
    ----------
    simulation_data_path : str or pathlib.Path
        Root simulation-data directory.

    case : Case
        QMEP simulation case.

    batch : str
        Batch name.

    file_type : str
        Transient file type.

    rea_idx : int
        Realization index (0-based).

    cycle_point_label : str
        Cycle-point label.

    cycle_idx : int
        Cycle index.

    epst_file : float or None, optional
        Strain amplitude encoded in the cycles filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.
        The default ("") corresponds to the standard
        parallel protocol.

    set_idx : int, optional
        Set index. Default is 0.

    dtype : type, optional
        Data type passed to numpy.loadtxt.

    usecols : tuple or None, optional
        Columns passed to numpy.loadtxt.

    Returns
    -------
    numpy.ndarray
        Loaded transient-data array.
    """

    path = get_transient_file_path(
        simulation_data_path=simulation_data_path,
        case=case,
        batch=batch,
        file_type=file_type,
        rea_idx=rea_idx,
        cycle_point_label=cycle_point_label,
        cycle_idx=cycle_idx,
        set_idx=set_idx,
        epst_file=epst_file,
        branch=branch
    )

    return io.load_txt(
        path,
        dtype=dtype,
        usecols=usecols
    )

# ==========================================================
# TRANSIENT WRAPPERS
# ==========================================================

def load_transient_scalar(
    simulation_data_path,
    case,
    batch,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    epst_file=None,
    branch="",
    set_idx=0
):
    """
    Load transient scalar data.

    Parameters
    ----------
    epst_file : float or None, optional
        Strain amplitude encoded in the cycles filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.
        The default ("") corresponds to the standard
        parallel protocol.

    Notes
    -----
    The first two entries contain metadata and are
    discarded.
    """

    return load_transient_file(
        simulation_data_path=simulation_data_path,
        case=case,
        batch=batch,
        file_type=qc.FILE_PREFIX_SCALAR,
        rea_idx=rea_idx,
        cycle_point_label=cycle_point_label,
        cycle_idx=cycle_idx,
        set_idx=set_idx,
        dtype=float,
        epst_file=epst_file,
        branch=branch
    )[2:]


def load_transient_event(
    simulation_data_path,
    case,
    batch,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    epst_file=None,
    branch="",
    set_idx=0,
    grid_reshape=False,
):
    """
    Load transient event data.

Parameters
    ----------
    epst_file : float or None, optional
        Strain amplitude encoded in the loaded filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.

    set_idx : int, optional
        Set index. Default is 0.

    grid_reshape : bool, optional
        If True, reshape the loaded one-dimensional field into a square (N, N) grid.
    """

    data = load_transient_file(
        simulation_data_path=simulation_data_path,
        case=case,
        batch=batch,
        file_type=qc.FILE_PREFIX_EVENT,
        rea_idx=rea_idx,
        cycle_point_label=cycle_point_label,
        cycle_idx=cycle_idx,
        set_idx=set_idx,
        dtype=int,
        epst_file=epst_file,
        branch=branch
    )

    if grid_reshape:
        data = reshape_square_grid(data)

    return data


def load_transient_trap_plus(
    simulation_data_path,
    case,
    batch,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    epst_file=None,
    branch="",
    set_idx=0
):
    """
    Load transient trap-plus field.

Parameters
    ----------
    epst_file : float or None, optional
        Strain amplitude encoded in the loaded filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.

    set_idx : int, optional
        Set index. Default is 0.
    """

    return load_transient_file(
        simulation_data_path=simulation_data_path,
        case=case,
        batch=batch,
        file_type=qc.FILE_PREFIX_TRAP_PLUS,
        rea_idx=rea_idx,
        cycle_point_label=cycle_point_label,
        cycle_idx=cycle_idx,
        set_idx=set_idx,
        dtype=float,
        epst_file=epst_file,
        branch=branch
    )


def load_transient_trap_minus(
    simulation_data_path,
    case,
    batch,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    epst_file=None,
    branch="",
    set_idx=0
):
    """
    Load transient trap-minus field.

Parameters
    ----------
    epst_file : float or None, optional
        Strain amplitude encoded in the loaded filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.

    set_idx : int, optional
        Set index. Default is 0.
    """

    return load_transient_file(
        simulation_data_path=simulation_data_path,
        case=case,
        batch=batch,
        file_type=qc.FILE_PREFIX_TRAP_MINUS,
        rea_idx=rea_idx,
        cycle_point_label=cycle_point_label,
        cycle_idx=cycle_idx,
        set_idx=set_idx,
        dtype=float,
        epst_file=epst_file,
        branch=branch
    )


def load_transient_stress(
    simulation_data_path,
    case,
    batch,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    epst_file=None,
    branch="",
    set_idx=0
):
    """
    Load transient stress field.

Parameters
    ----------
    epst_file : float or None, optional
        Strain amplitude encoded in the loaded filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.

    set_idx : int, optional
        Set index. Default is 0.
    """

    return load_transient_file(
        simulation_data_path=simulation_data_path,
        case=case,
        batch=batch,
        file_type=qc.FILE_PREFIX_STRESS,
        rea_idx=rea_idx,
        cycle_point_label=cycle_point_label,
        cycle_idx=cycle_idx,
        set_idx=set_idx,
        dtype=float,
        epst_file=epst_file,
        branch=branch
    )


def load_transient_plastic_def(
    simulation_data_path,
    case,
    batch,
    rea_idx,
    cycle_point_label,
    cycle_idx,
    epst_file=None,
    branch="",
    set_idx=0
):
    """
    Load transient plastic-deformation field.

Parameters
    ----------
    epst_file : float or None, optional
        Strain amplitude encoded in the loaded filename.
        If None, uses case.epst.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.

    set_idx : int, optional
        Set index. Default is 0.
    """

    return load_transient_file(
        simulation_data_path=simulation_data_path,
        case=case,
        batch=batch,
        file_type=qc.FILE_PREFIX_PLASTIC_DEF,
        rea_idx=rea_idx,
        cycle_point_label=cycle_point_label,
        cycle_idx=cycle_idx,
        set_idx=set_idx,
        dtype=float,
        epst_file=epst_file,
        branch=branch
    )

# ==========================================================
# CONFIGURATION DATA
# ==========================================================

# TODO:
#
# def load_config_data(
#     simulation_data_path,
#     case,
#     batch,
#     ...
# ):
#     ...
#
# Configuration-data loading will be implemented once the
# desired interface is finalized.

# ==========================================================