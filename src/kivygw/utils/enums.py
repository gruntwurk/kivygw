import contextlib
from enum import Enum
from typing import List

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
        `default_member`

    TIP: Usually, an `@unique` decorator is appropriate for enums used with
        DropdownEnum.
    """

    def display_name(self) -> str:
        """
        :return: The primary value, if it's a string; otherwise, the member name.
        """
        primary = self.primary_value()

        return primary if isinstance(primary, str) else self.name

    def primary_value(self):
        return self.value[0] if self.is_tuple() else self.value

    def is_tuple(self):
        return isinstance(self.value, tuple)

    def secondary_values(self):
        """
        If the value is a tuple, then the first elemnent of the tuple is
        considered to be the primary value while all other elements of the
        tuple are considered to be secondary.

        :return: `None`, `value[1]` (if value is a 2-tuple), or `value[1:]`
        (if value is a 3-or-more-tuple).
        """
        if not self.is_tuple():
            return None
        return self.value[1] if len(self.value) == 2 else self.value[1:]

    @classmethod
    def possible_values(cls) -> List[str]:
        """
        A list describing the elements, in the order defined. The primary
        value is used if it is a string; otherise, the element's name is used.
        """
        return [e.display_name() for e in cls]

    @classmethod
    def by_value(cls, value):
        if not value:
            return cls.default_member()
        if isinstance(value, str):
            value = value.strip().casefold()
        for e in cls:
            operand = e.primary_value()
            if isinstance(operand, str):
                operand = operand.strip().casefold()
            if operand == value:
                return e
        raise GWValueError(f"No such {cls.__name__} with a primary value of {value}")

    @classmethod
    def by_name(cls, name: str):
        """
        Returns the element that matches the given `name`. You could simply refer
        to `TheEnum[name]`, but that raises an exception if not found, while this
        method return `None`. But first, it'll try again looking for the name in
        all lower-case.
        """
        name = name.strip()
        with contextlib.suppress(KeyError):
            return cls[name]
        with contextlib.suppress(KeyError):
            return cls[name.casefold()]
        return None

    @classmethod
    def default_member(cls):
        """
        Returns the first member defined.

        NOTE: Override this method for anything more complicated.
        """
        # We can't just index it as `cls[0]` because __getitem__ looks for the
        # member name, not the position.
        for e in cls:
            return e

