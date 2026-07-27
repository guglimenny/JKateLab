# =============================================================================
# jklab-core/exceptions.py
#
# -----------------------------------------------------------------------------
# DESCRIPTION
# -----------------------------------------------------------------------------
# Utilities for standardized error and warning handling across the JKateLab
# ecosystem.
#
# The module provides:
# - a base class for JKateLab-specific exceptions;
# - a base class for JKateLab-specific warnings;
# - utilities for formatting error and warning messages;
# - a unified interface for raising errors and issuing warnings.
#
# -----------------------------------------------------------------------------
# DEPENDENCIES
# -----------------------------------------------------------------------------
# - warnings : for native warning management.
#
# -----------------------------------------------------------------------------
# PUBLIC API
# -----------------------------------------------------------------------------
# Classes:
# - JKateLabError   : Base class for JKateLab-specific exceptions.
# - JKateLabWarning : Base class for JKateLab-specific warnings.
#
# Functions:
# - format_message : Compose and format error and warning messages.
# - raise_error    : Raise an error with a custom message and context.
# - raise_warning  : Issue a warning with a custom message and context.
#
# -----------------------------------------------------------------------------
# IMPLEMENTATION NOTES
# -----------------------------------------------------------------------------
# - [format_message]: Uses "\n".join() to separate message lines.
# - [raise_warning]: Uses stacklevel=2 to report the warning at the
#   caller's location rather than inside this module.
#
# -----------------------------------------------------------------------------
# MAINTAINER
# -----------------------------------------------------------------------------
# Guglielmo Mennella.
# =============================================================================

# =============================================================================
# Imports
# =============================================================================

import warnings

# =============================================================================
# Classes
# =============================================================================

class JKateLabError(Exception):
    """Base class for JKateLab-specific exceptions."""
    pass


class JKateLabWarning(UserWarning):
    """Base class for JKateLab-specific warnings."""
    pass

# =============================================================================
# Functions
# =============================================================================

def format_message(
    message: str,
    context: dict = None,
) -> str:
    """
    Format a message by composing a custom message with optional context data.
    The context allows to pass any kind of variables relevant
    to the error call.

    Parameters
    ----------
    message : str
        User-provided custom message to describe the error in detail.
    
    context : dict or None, optional
        Dictionary containing relevant quantities to include in the message.
        Keys represent variable names and values represent their
        corresponding values. Each entry is formatted as
        'name = value'.

    Returns
    -------
    str
        Formatted message.
    """

    message_lines = [message]

    if context:

        message_lines.append("")
        message_lines.append("Context:")

        for name, value in context.items():

            message_lines.append(
                f"{name} = {value!r}"
            )

    formatted_msg = "\n".join(message_lines)

    return formatted_msg


def raise_error(
    error: type[Exception],
    message: str,
    context: dict = None,
) -> None:
    """
    Raise an error with a custom message and optional context.

    Parameters
    ----------
    error : type[Exception]
        Exception class to raise.

    message : str
        User-provided custom message to describe the error in detail.
    
    context : dict or None, optional
        Dictionary containing relevant quantities to include in the error
        message. Keys represent variable names and values represent their
        corresponding values.

    Returns
    -------
    None
    """

    err_msg = format_message(
        message=message,
        context=context
    )

    raise error(err_msg)


def raise_warning(
    warning: type[Warning],
    message: str,
    context: dict = None,
) -> None:
    """
    Issue a warning with a custom message and optional context.

    Parameters
    ----------
    warning : type[Warning]
        Warning class to issue.

    message : str
        User-provided custom message to describe the warning in detail.
    
    context : dict or None, optional
        Dictionary containing relevant quantities to include in the warning
        message. Keys represent variable names and values represent their
        corresponding values.

    Returns
    -------
    None
    """

    warn_msg = format_message(
        message=message,
        context=context
    )

    warnings.warn(
        category=warning,
        message=warn_msg,
        stacklevel=2
    )

# =============================================================================