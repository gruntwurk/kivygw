__all__ = [
    'float_color',
    'float_tuple',
    'int_color',
    'int_tuple',
    'is_color',
    'is_float_tuple',
    'color_brightness',
    'color_outline',
]


def is_color(possible_color_tuple) -> bool:
    """
    Analyzes `possible_color_tuple` to see if the value could properly represent
    a color. Namely it is a 3-tuple or a 4-tuple (or list), and all of those 3-4
    elements are either ints (0-255) ir all floats (0.0 to 1.0).

    :param possible_color_tuple: the candidate value.
    :return: True if it looks like a color tuple.
    """
    if not (isinstance(possible_color_tuple, (tuple, list))):
        return False
    count = len(possible_color_tuple)
    if count < 3 or count > 4:
        return False
    float_count = 0
    above_1_count = 0

    for v in possible_color_tuple:
        if v < 0 or v > 255:
            return False
        if isinstance(v, float):
            float_count += 1
        if v > 1:
            above_1_count += 1
    return above_1_count == 0 or float_count == 0


def is_float_tuple(color_tuple) -> bool:
    """
    Analyzes a color tuple to see if it is a Kivy style with
    floats (0.0 to 1.0), or a traditional style with ints (0-255).
    NOTE: For a few edge cases (where all elements are exactly 0 or exactly 1)
    tie goes to True (is floats). For all 0's, it's the same either way.
    All 0's and 1's is rare for an int tuple but quite common for a float tuple
    (WHITE, RED, GREEN, BLUE, CYAN, ...).

    :param color_tuple: Either a 3- or 4-tuple.
    :return: True if it is Kivy style.
    """
    return not any(value > 1.0 or value < 0.0 for value in color_tuple)


def float_color(int_color):
    '''
    Converts an RGB value from integer (0-255) to float (0.0 to 1.0).
    '''
    return min(int_color / 255, 1.0) if int_color is not None else None


def float_tuple(color_tuple, alpha=None) -> tuple:
    '''
    Converts an RGB tuple from integers (0-255) to floats (0.0 to 1.0).

    :param int_tuple: Either a 3-tuple or a 4-tuple of integers (0-255)
    :param alpha: The alpha value to use (between 0.0 and 1.0).
        Defaults to `None`. In the case of a 4-tuple, `None` means the alpha
        value will be converted to float along with the RGB. In the case
        of a 3-tuple, `None` means it will remain a 3-tuple.

    :return: A corresponding tuple of floats.
    '''
    if not color_tuple:
        return None
    if is_float_tuple(color_tuple):
        return (*color_tuple[:3], alpha) if alpha else color_tuple
    if len(color_tuple) == 3:
        red, green, blue = color_tuple
        old_alpha = None
    elif len(color_tuple) == 4:
        red, green, blue, old_alpha = color_tuple
    else:
        raise ValueError(f"float_tuple() requires a 3-tuple or a 4-tuple, but a {len(color_tuple)}-tuple was given.")
    if not alpha:
        alpha = float_color(old_alpha)

    if alpha is not None:
        return (float_color(red), float_color(green), float_color(blue), alpha)
    return (float_color(red), float_color(green), float_color(blue))


def int_color(float_color):
    '''
    Converts an RGB value from float (0.0 to 1.0) to integer (0 to 255).
    '''
    return min(int(float_color * 255), 255) if float_color is not None else None


def int_tuple(float_tuple, alpha=None) -> tuple:
    '''
    Converts an RGB tuple from floats (0.0 to 1.0) to integers (0 to 255).

    :param int_tuple: Either a 3-tuple or a 4-tuple of floats (0.0 to 0.1)
    :param alpha: The alpha value to use (between 0 and 255).
        Defaults to `None`. In the case of a 4-tuple, `None` means the alpha
        value will be converted to int along with the RGB. In the case
        of a 3-tuple, `None` means it will remain a 3-tuple.

    :return: A corresponding tuple of ints.
    '''
    if not float_tuple:
        return None
    if len(float_tuple) == 3:
        red, green, blue = float_tuple
        old_alpha = None
    elif len(float_tuple) == 4:
        red, green, blue, old_alpha = float_tuple
    else:
        raise ValueError(f"int_tuple() requires a 3-tuple or a 4-tuple, but a {len(int_tuple)}-tuple was given.")
    if not alpha:
        alpha = int_color(old_alpha)

    if alpha is not None:
        return (int_color(red), int_color(green), int_color(blue), int_color(alpha))
    return (int_color(red), int_color(green), int_color(blue))


def color_brightness(int_tuple) -> int:
    """
    :param int_tuple: Either a 3- or 4-tuple of integers (0-255).
    (The alpha channel is ignored.)

    :return: The average of the RGB values.
    """
    return int((sum(int_tuple[:3])) / 3)


def color_outline(color_tuple) -> tuple:
    """
    Returns either black or white, depending on if this color is light or dark
    (e.g. to outline it in case the original color is hard to see).

    :param color_tuple: Can be either Kivy style with floats (0.0 to 1.0),
    or a traditional style with ints (0-255), with optional alpha channel,
    i.e. 3 or 4 elements.

    :return: A 3-tuple of the corresponding type (floats or ints)
    """
    if was_float := is_float_tuple(color_tuple):
        color_tuple = int_tuple(color_tuple)
    is_dark = color_brightness(color_tuple) < 128
    result = (255, 255, 255) if is_dark else (0, 0, 0)
    return float_tuple(result) if was_float else result


