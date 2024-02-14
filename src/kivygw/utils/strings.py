import re

__all__ = [
    "snake_case",
    "normalize_name",
]


def snake_case(identifier: str) -> str:
    """
    Converts CamelCase or javaCase to snake_case (all lower with underscores).
    """
    words = re.findall(r"([a-z0-9]+|[A-Z][a-z0-9]*|[^A-Za-z0-9]+)", identifier)
    lower_words = [word.lower() for word in words if word != "_"]
    return "_".join(lower_words)


def normalize_name(name, separator="_") -> str:
    """
    Normalizes a name by replacing all non-alphanumeric characters with
    underscores (or whatever separator you specify).

    See also: `snake_case(), camel_case()`.
    """
    return re.sub("[^A-Za-z0-9_]+", separator, name)

