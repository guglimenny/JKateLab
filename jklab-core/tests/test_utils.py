# =============================================================================
# test_utils.py
#
# -----------------------------------------------------------------------------
# DESCRIPTION
# -----------------------------------------------------------------------------
# Utilities for testing modules.
#
# The module provides:
# - utilities for testing error raising;
# - utilities for recording test results;
# - utilities for printing test summaries;
#
# -----------------------------------------------------------------------------
# DEPENDENCIES
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------
# Functions:
# - test_raises        : Test whether a function raises an expected error.
# - record_test        : Record and display a test result.
# - print_test_summary : Print a summary of test results.
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
# Functions
# =============================================================================
# -----------------------------------------------------------------------------
# Test-error functions
# -----------------------------------------------------------------------------

def test_raises(
    func,
    expected_error,
    expected_message=None,
) -> bool:
    """
    Test whether a function raises an expected error.

    Parameters
    ----------
    func
        Function expected to raise an error.

    expected_error
        Expected error class.

    expected_message : optional
        Expected text contained in the raised error message.

    Returns
    -------
    bool
        True if func raises expected_error and, if provided,
        expected_message is contained in the error message.
    """

    try:
        func()

    except expected_error as error:

        if expected_message is None:
            return True

        return expected_message in str(error)

    except Exception:
        return False

    return False

# -----------------------------------------------------------------------------
# Test-recording functions
# -----------------------------------------------------------------------------

def record_test(
    test_results: dict[str, bool],
    test_name: str,
    condition: bool,
) -> None:
    """
    Record and display the result of a test.

    Parameters
    ----------
    test_results : dict[str, bool]
        Dictionary storing test names and results.

    test_name : str
        Name assigned to the test.

    condition : bool
        Boolean condition determining the test result.

    Returns
    -------
    None
    """

    passed_flag = bool(condition)

    test_results[test_name] = passed_flag

    if passed_flag:
        print(f"✅ PASSED: {test_name}.")
    else:
        print(f"❌ FAILED: {test_name}.")


def print_test_summary(
    test_results: dict[str, bool]
) -> None:
    """
    Print a summary of test results.

    Parameters
    ----------
    test_results : dict[str, bool]
        Dictionary storing test names and results.

    Returns
    -------
    None
    """

    # Used for visual separation
    separator_len = 40

    total = len(test_results)
    # bool values are treated as 1 (True) and 0 (False) when summed.
    passed = sum(test_results.values())
    failed = total - passed

    print()
    print("=" * separator_len)
    print("TEST SUMMARY")
    print("=" * separator_len)

    print(f"Passed: {passed}/{total}")
    print(f"Failed: {failed}/{total}")

    if total:
        ratio = passed / total * 100
        print(f"Success rate: {ratio:.1f}%")

    print()

    for name, result in test_results.items():

        status = "PASSED" if result else "FAILED"

        print(f"{status}: {name}")

    print("=" * separator_len)

# =============================================================================