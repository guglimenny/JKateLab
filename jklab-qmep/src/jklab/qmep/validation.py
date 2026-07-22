# ==========================================================
# qmep_validation.py
#
# QMEP data validation utilities.
#
# This module provides lightweight validation routines used
# before loading and analyzing simulation data.
#
# Validation is intentionally strict:
#
# - success -> return True
# - failure -> raise immediately
#
# No files are silently skipped.
#
# ==========================================================

from . import qmep_paths as qph
from . import qmep_loader as qld

# ==========================================================
# SIMULATION COMPLETENESS
# ==========================================================

def validate_realizations(
    simulation_data_dir,
    case_list,
    batch,
    rea_num,
    verbose=True
):
    """
    Check that all transient-data directories contain the
    expected number of realization folders.

    This function is intended as a lightweight simulation
    completeness check before running analysis.

    Parameters
    ----------
    simulation_data_dir : str or pathlib.Path
        Root simulation-data directory.

    case_list : list[Case]
        Cases to validate.

    batch : str
        Batch name.

    rea_num : int
        Expected number of realization folders.

    verbose : bool, optional
        Print validation summary.

    Returns
    -------
    missing_case_list : list[Case]
        Cases whose transient-data directory is missing or
        contains fewer realization folders than expected.
    """

    missing_case_list = []

    for case in case_list:

        transient_dir = qph.build_transient_dir_path(
            simulation_data_dir,
            case,
            batch
        )

        # Missing transient_data directory
        if not transient_dir.is_dir():

            missing_case_list.append(case)

            if verbose:

                print(
                    f"✗ {case.epst_label}: "
                    "missing transient_data directory"
                )

            continue

        run_dir_list = [
            path
            for path in transient_dir.iterdir()
            if (
                path.is_dir()
                and path.name.startswith("run_")
            )
        ]

        run_num = len(run_dir_list)

        if run_num != rea_num:

            missing_case_list.append(case)

            if verbose:

                print(
                    f"✗ {case.epst_label}: "
                    f"{run_num}/{rea_num} realizations found"
                )

    if verbose:

        valid_num = (
            len(case_list)
            - len(missing_case_list)
        )

        print()

        print(
            f"Validated {len(case_list)} case(s)"
        )

        print(
            f"Complete case(s) : {valid_num}"
        )

        print(
            f"Incomplete case(s) : "
            f"{len(missing_case_list)}"
        )

        if len(missing_case_list) == 0:

            print(
                "✓ All realization folders found."
            )

    return missing_case_list

# ==========================================================
# CYCLES
# ==========================================================

def validate_cycles(
    simulation_data_dir,
    case_list,
    batch,
    epst_file=None,
    branch=""
):
    """
    Validate cycles files for all cases.

    Parameters
    ----------
    simulation_data_dir : str or pathlib.Path
        Root simulation-data directory.

    case_list : list[Case]
        Cases to validate.

    batch : str
        Batch name.

    epst_file : float, optional
        Strain amplitude encoded in the filename.
        If None, uses 'case.epst'.

    branch : {"", "p", "m"}, optional
        Sequential-training branch encoded in the filename.
        The default ("") corresponds to the standard
        parallel protocol.

    Returns
    -------
    bool
        True if validation succeeds.

    Raises
    ------
    FileNotFoundError
        If a cycles file is missing.
    """

    for case in case_list:

        path = qph.build_cycles_path(
            simulation_data_dir,
            case,
            batch,
            epst_file=epst_file,
            branch=branch
        )

        if not path.is_file():

            raise FileNotFoundError(
                "in [qmep_validation.validate_cycles],\n"
                "missing cycles file:\n"
                f"case = {case}\n"
                f"path = '{path}'"
            )

    return True


# ==========================================================
# TRANSIENT DATA
# ==========================================================

def validate_transient(
    simulation_data_dir,
    case_list,
    batch,
    file_type,
    rea_idx_list,
    cycle_point_label_list,
    cycle_idx_list,
    epst_file=None,
    branch="",
    set_idx=0
):
    """
    Validate transient-data files.

    Parameters
    ----------
    simulation_data_dir : str or pathlib.Path
        Root simulation-data directory.

    case_list : list[Case]
        Cases to validate.

    batch : str
        Batch name.

    file_type : str
        Transient file type.

    rea_idx_list : iterable[int]
        Realization indices.

    cycle_point_label_list : iterable[str]
        Cycle-point labels.

    cycle_idx_list : iterable[int]
        Cycle indices.

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
    bool
        True if validation succeeds.

    Raises
    ------
    FileNotFoundError
        If a required file is missing.
    """

    for case in case_list:

        for rea_idx in rea_idx_list:

            for cycle_point_label in cycle_point_label_list:

                for cycle_idx in cycle_idx_list:

                    path = qld.get_transient_file_path(
                        simulation_data_path=simulation_data_dir,
                        case=case,
                        batch=batch,
                        file_type=file_type,
                        rea_idx=rea_idx,
                        cycle_point_label=cycle_point_label,
                        cycle_idx=cycle_idx,
                        epst_file=epst_file,
                        branch=branch,
                        set_idx=set_idx
                    )

                    if not path.is_file():

                        raise FileNotFoundError(
                            "in [qmep_validation.validate_transient], "
                            "missing transient file:\n"
                            f"case              = {case}\n"
                            f"file_type         = {file_type}\n"
                            f"rea_idx           = {rea_idx}\n"
                            f"cycle_point_label = "
                            f"'{cycle_point_label}'\n"
                            f"cycle_idx         = {cycle_idx}\n"
                            f"path              = '{path}'"
                        )

    return True

# ==========================================================