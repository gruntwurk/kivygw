__all__ = [
    "next_in_range",
    "round_base",
]


def next_in_range(index, max_value, min_value=0, increment=1) -> int:
    """
    Increments an index while keeping it in range.
    """

    index += increment
    if index > max_value:
        index = min_value
    if index < min_value:
        index = max_value
    return index


def round_base(x, base=5):
    """
    Rounds a number to the nearest base number. E.g. 22.9 gets rounded up to
    25 if base=5, or down to 20 if base=10.

    :param x: the raw number to be rounded
    :param base: the base (increment), defaults to 5
    """
    return base * round(x/base)