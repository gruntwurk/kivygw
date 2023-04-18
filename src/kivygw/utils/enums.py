import contextlib
import re

__all__ = [
    'enum_by_value',
    'enum_by_name',
]


def enum_by_value(enum_class, value: str):
    """
    Returns the element of `enum_class` that best matches the given `value`.
    In order for this to work, the element's value either needs to be a
    simple string, or else the class must have at least one of the following
    methods defined:

    `by_value()` -- (class method) that knows how to find the right element.
    `description()` -- extracts the description str from the complex enum value.
    `primary_value()` -- extracts the main value from the complex enum value
        which either needs to be a str, or can be converted to one via `str()`.

    Failing all of that, we punt over to `enum_by_name()` in case they
    actually passed in the name rather than the value.

    :param enum_class: The enum type (class). Any subclass of Enum.

    :param name: The name of the enum to fetch.

    :return: The identified enum element, or None.
    """
    if not value or not isinstance(value, str):
        return None

    # sourcery skip: assign-if-exp, reintroduce-else
    if hasattr(enum_class, 'by_value'):
        if e := enum_class.by_value(value):
            return e

    if hasattr(enum_class, 'description'):
        for e in enum_class:
            if e.description() == value:
                return e

    if hasattr(enum_class, 'primary_value'):
        for e in enum_class:
            if str(e.primary_value()) == value:
                return e

    for e in enum_class:
        if e.value == value:
            return e

    # Last resort, maybe the given value is actually the element name
    return enum_by_name(enum_class, value)


def enum_by_name(enum_class, name: str):
    """
    Returns the element of `enum_class` that best matches the given `name`.
    First, the name is normalized to exclude anything other than alphanumerics
    and underscores, since all Enum element names conform to Python identifier
    rules. Then, it tries to find any variation of the name from as-is, to
    lower case, to upper case.
    NOTE: `GWEnum.by_name` calls this function, not the other way around.

    :param enum_class: The enum type (class). Any subclass of Enum.

    :param name: The name of the enum to fetch.

    :return: The identified enum element, or None.
    """
    if name is None or not isinstance(name, str):
        return None

    name = normalize_name(name.strip(), '')
    if not name:
        return None
    with contextlib.suppress(KeyError):
        return enum_class[name]
    with contextlib.suppress(KeyError):
        return enum_class[name.casefold()]
    with contextlib.suppress(KeyError):
        return enum_class[name.upper()]
    return None


def normalize_name(name, separator="_") -> str:
    """
    Normalizes a name by replacing all non-alphanumeric characters with
    underscores (or whatever separator you specify).
    """
    return re.sub("[^A-Za-z0-9_]+", separator, name)
