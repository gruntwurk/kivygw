import contextlib
from enum import Enum

from kivygw.utils.exceptions import GWValueError

__all__ = [
    "GWEnum",
]


class GWEnum(Enum):
    """
    Base class for an `Enum` that, among other things, provides all the
    neccesary suuport for being used with the `DropdownEnum` Kivy widget.

    Element methods provided are: `display_name`

    Class methods provided are: `possible_values`, `by_name`, `by_value`,
        `default_enum`

    TIP: Usually, an `@unique` decorator is appropriate for enums used with
        DropdownEnum.
    """

    def display_name(self) -> str:
        """
        Returns the value as a string -- or, if the value is a tuple, then
        returns just the first element of the tuple as a string. This allows
        for the value to contain additional information such as a corresponding
        color.

        :return: _description_
        """
        return str(self.value[0]) if isinstance(self.value, tuple) else str(self.value)

    @classmethod
    def possible_values(cls):
        """
        Returns a list of the element values, in the order defined.
        """
        return [e.display_name() for e in cls]

    @classmethod
    def by_value(cls, value):
        if not value:
            return cls.default_enum()
        for e in cls:
            if e.value == value or e.display_name().casefold() == value.strip().casefold():
                return e
        raise GWValueError(f"No such {cls.__name__} as {value}")

    @classmethod
    def by_name(cls, name: str):
        """
        Returns the element that matches the given `name`. You could simply refer
        to `TheEnum[name]`, but that raises an exception if not found, while this
        method return `None`. But first, it'll try again looking for the name in
        all lower-case.

        :param name: _description_
        :return: _description_
        """
        name = name.strip()
        with contextlib.suppress(KeyError):
            return cls[name]
        with contextlib.suppress(KeyError):
            return cls[name.casefold()]
        return None

    @classmethod
    def default_enum(cls):
        """
        Returns the first element defined. Override this for anything else.
        """
        # We can't just index it as `cls[0]` because __getitem__ looks for the
        # member name, not the position.
        for e in cls:
            return e

