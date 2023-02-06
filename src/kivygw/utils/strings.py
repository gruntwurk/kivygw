import re

__all__ = [
    "snake_case",
]


def snake_case(identifier: str) -> str:
    """
    Converts CamelCase or javaCase to snake_case (all lower with underscores).
    """
    words = re.findall(r"([a-z]+|[A-Z][a-z]*|[^A-Za-z]+)", identifier)
    lower_words = [word.lower() for word in words if word != "_"]
    return "_".join(lower_words)




