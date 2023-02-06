import logging
from typing import Optional
from kivy.base import ExceptionHandler, ExceptionManager


__all__ = [
    "manage_uncaught_exceptions_within_kivy",
    "log_uncaught",
    "ConfigError",
    "ValueInterpretationWarning",
    "ConfigSettingWarning",
]

UNCAUGHT_MESSAGE = "Uncaught error detected. There is no good reason why the following error wasn't handled earlier."
EX_OK = 0
EX_WARNING = 1
EX_ERROR = 2


# ############################################################################
#                                                           EXCEPTION HANDLING
# ############################################################################

class GWKivyExceptionHandler(ExceptionHandler):
    EX_OK = 0  # keep runnning
    EX_WARNING = 1  # keep runnning
    EX_ERROR = 2  # (or higher) quit the app
    """
    This handler is added to the bottom of the kivy exception handler stack,
    and thus called if none of kivy's internal handlers were applicable. That
    means we're looking at a non-Kivy Exception that should have been caught
    somewhere within our application code but wasn't. So, we use GruntWurk's
    log_uncaught() function to sort it out.
    """
    def handle_exception(self, inst):
        exitcode = log_uncaught(inst)
        if exitcode < self.EX_ERROR:
            return ExceptionManager.PASS
        return ExceptionManager.RAISE


def manage_uncaught_exceptions_within_kivy():
    ExceptionManager.add_handler(GWKivyExceptionHandler())


def log_uncaught(exception: Optional[Exception] = None, log: logging.Logger = None) -> int:
    """
    It's always a good idea to wrap the entire application in a `try/except`
    block in order to catch any exceptions that trickle all the way up to
    that point. Then, just call this function in the `except` clause, passing in
    the offending Exception.

    TIP: For a `Kivy` app, just call `gwpycore.manage_uncaught_exceptions_within_kivy()`
    from within the `__init__` method of your app's main class (the class that
    inherits from `APP` or `MDApp`). That will register a special exception
    handler that does the work of sorting out any uncaught exceptions -- exactly
    how this function does -- including  telling kivy to carry on running if
    the exception specifies an exit code of `EX_OK` (0) or `EX_WARNING` (1).

    :param exception: The otherwise uncaught exception.

    :param log: The Logger to use. If not specified, then the root logger
    will be used.

    :return: A suggested exit code. If the exception has an `exitcode`
    attribute (see `GruntWurkException`), then that code is returned;
    otherwise, `EX_ERROR` (2) is returned -- or in the case that `exception`
    is None (somehow), then `EX_OK` (0) is returned.

    IMPORTANT: It's possible that an exception has an associated exit code of
    `EX_WARNING` (1), or even `EX_OK` (0). Thus, if the returned code is <= 1,
    then the application should probably actually continue, relying on the
    fact that exception has (just now) been logged.
    """
    if not log:
        log = logging.getLogger()
    exitcode = EX_OK
    if exception:
        exitcode = EX_ERROR
        if hasattr(exception, "exitcode"):
            exitcode = exception.exitcode
        log.error(UNCAUGHT_MESSAGE)
        log.exception(exception)
    return exitcode

# ############################################################################
#                                                            CUSTOM EXCEPTIONS
# ############################################################################

class ConfigError(Exception):
    """
    Exception raised because of a problem processing configuration data.

    :param args: A payload for the exception, as usual (typically a str
    with an explanation of the error).
    """

    def __init__(self, *args) -> None:
        super().__init__(*args)



class ValueInterpretationWarning(Warning):
    """
    Warning raised because of a value that could not be converted to an
    expected type.

    :param key: The name of the field.

    :param attempted_value: The value that is in error.

    :param args: Any additional payload for the exception, e.g. another
    instance of `Exception`).

    :param context: (optional) a description of the context (the data source, row number, etc.).

    :param possible_values: (optional) a list of valid choices.

    :param loglevel: (optional) How this error should appear in the log (if no
    outer code catches it and handles it, that is). The default is `logging.WARNING`.
    """

    def __init__(self, key, attempted_value, *args, context=None, possible_values=None, loglevel=logging.WARNING):
        msg = ""
        if context:
            msg += f"In {context}, "
        msg += f"{key} = {attempted_value} is invalid."
        if possible_values:
            msg += f" Possible values are: {possible_values}"
        super(ValueInterpretationWarning, self).__init__(msg, *args, loglevel=loglevel)

class ConfigSettingWarning(ValueInterpretationWarning):
    """
    Warning raised because of a bad setting in a config file.

    :param key: The name of the setting.

    :param attempted_value: The value that is in error.

    :param args: Any additional payload for the exception, e.g. another
    instance of `Exception`).

    :param context: (optional) a description of the context (the data source, row number, etc.).
    Defaults to "a configuration setting".

    :param possible_values: (optional) a list of valid choices.

    :param loglevel: (optional) How this error should appear in the log (if no
    outer code catches it and handles it, that is). The default is `logging.WARNING`.
    """
    def __init__(self, key, attempted_value, *args, context="a configuration setting", possible_values=None, loglevel=logging.WARNING):
        super(ConfigSettingWarning, self).__init__(
            key, attempted_value, *args, context="a configuration setting", possible_values=possible_values, loglevel=loglevel
        )


