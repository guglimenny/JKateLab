# ==========================================================
# exceptions.py
#
# Exception and error-handling utilities.
#
# This module provides helpers for raising formatted
# exceptions with consistent diagnostic information.
#
# Convention
# ----------
# Error messages follow the format:
#
#     [module.function]
#
#     message
#
#     variable_1 = value_1
#     variable_2 = value_2
#     ...
#
#
# ==========================================================

# ==========================================================
# ERROR TYPES
# ==========================================================

_ERROR_DICT = {
    "value"   : ValueError,
    "type"    : TypeError,
    "index"   : IndexError,
    "key"     : KeyError,
    "runtime" : RuntimeError,
    "file"    : FileNotFoundError
}

# ==========================================================
# ERROR UTILITIES
# ==========================================================

def raise_error(
    error_type,
    module_name,
    function_name,
    message,
    **kwargs
):
    """
    Raise a formatted exception.

    Parameters
    ----------
    error_type : str
        Error category.

        Supported values:

        - "value"
        - "type"
        - "index"
        - "key"
        - "runtime"

    module_name : str
        Module name.

    function_name : str
        Function name.

    message : str
        Main error message.

    **kwargs
        Additional variables printed for debugging.

    Examples
    --------
    >>> raise_error(
    ...     error_type="value",
    ...     module_name="plotting",
    ...     function_name="plot_imshow_grid",
    ...     message=(
    ...         "image_data_list and "
    ...         "subplot_label_list must contain "
    ...         "the same number of elements."
    ...     ),
    ...     nplots=8,
    ...     nlabels=4
    ... )
    """

    if error_type not in _ERROR_DICT:

        raise ValueError(
            "[exceptions.raise_error]\n"
            "Unknow error type:\n"
            f"error_type = '{error_type}'.\n"
        )

    text = (
        f"[{module_name}.{function_name}]\n"
        f"{message}:"
    )

    if kwargs:

        text += "\n"

        for name, value in kwargs.items():

            text += (
                f"{name} = {value!r}\n"
            )

    raise _ERROR_DICT[error_type](text)

# ==========================================================