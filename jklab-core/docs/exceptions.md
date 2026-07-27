----------------------------------------------------------------------

# exceptions.md

----------------------------------------------------------------------

## Purpose

The `exceptions.py` module provides a standardised framework for error
and warning handling. Errors and warnings are managed through native
Python `Exception` and `Warning` classes or through JKateLab-specific
custom classes.

The custom classes provide a common basis for future development of
dedicated JKateLab errors and warnings.

---

## Design

Error and warning handling is composed of three individual steps:

1. **Selection of the appropriate error or warning.** The caller
   specifies either a native Python `Exception` (`Warning`) class or a
   custom `JKateLabError` (`JKateLabWarning`) class.

2. **Formatting of the error or warning message.** The message is
   composed of:

   * a user-provided message describing the error or warning;
   * an optional `context` dictionary containing variables relevant to
     the error or warning.

   This is done via the `format_message` function.

3. **Raising or issuing the error or warning.** Errors are raised using
   the native Python `raise` mechanism, while warnings are issued via
   the native Python `warnings` module. This is done via the
   `raise_error` and `raise_warning` functions.

For consistency between error and warning handling, the warning issuing
function is also named `raise_warning`.

---

## Dependencies

* `warnings`: for native Python warning management.

---

## Public API

**Classes**:

* `JKateLabError`   : Base class for JKateLab-specific exceptions.
* `JKateLabWarning` : Base class for JKateLab-specific warnings.

**Functions**:

* `format_message` : Compose and format error and warning messages.
* `raise_error`    : Raise an error with a custom message and context.
* `raise_warning`  : Issue a warning with a custom message and context.

---

## Usage

Usage of the module requires a direct call to the `raise_error` or
`raise_warning` function with the following arguments:

* the error or warning class;
* a custom message;
* (optional) context dictionary.

---

## Error vs warning handling

Given its scientific focus, the JKateLab ecosystem prescribes that any
ambiguous, anomalous or unexpected behaviour that may affect numerical
results should result in an appropriate error rather than being allowed
to propagate silently.

Errors shall therefore be used whenever unexpected behaviour may
compromise the correctness of the final results.

In exceptional situations where the unexpected behaviour is certain not
to alter the numerical results, a warning may instead be issued to
inform the user while allowing the computation to continue.

---

## Context formatting

In addition to the error or warning class and the custom message, an
optional `context` dictionary may be passed to the error or warning
call. The context provides information about variables relevant to the
error or warning.

For a context dictionary structured as `{name: value}`, the context is
formatted as:

```text
Context:
name1 = value1
name2 = value2
...
```

and appended to the error or warning message.

---

## Examples

**Error**: A possible use case for error raising is the validation of
data before performing computations. If the data does not satisfy a
given criterion, an error can be raised with an explanatory message and
optional context.

For example, in the case of a negative argument for a square root:

```python
from jklab.core.exceptions import raise_error


def square_root_func(x):
    """
    Compute the square root of a non-negative number.
    """

    if x < 0:
        raise_error(
            error=ValueError,
            message="x cannot be negative.",
            context={"x": x}
        )

    return x ** 0.5
```

**Warning**: A possible use case for warning issuing is when a
statistical calculation that assumes a large dataset is provided with
a small number of datapoints. In this case, the computation can still
be performed correctly, but the user should be informed that the result
may be less reliable.

```python
import numpy as np

from jklab.core.exceptions import raise_warning


def central_limit_thm_average(data_list):
    """
    Compute the estimated mean value of the average of N random values.

    Note: the result will generally better match the theoretical
    expectation as the number of entries increases.
    """

    # Check that the number of entries is sufficiently large.
    N = len(data_list)

    if N < 10:
        raise_warning(
            warning=UserWarning,
            message=("Very small number of datapoints. "
                     "The final result may be less reliable."),
            context={"N": N}
        )

    average = np.mean(data_list)

    return average
```

----------------------------------------------------------------------