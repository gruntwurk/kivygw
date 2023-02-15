__all__ = [
    "widget_by_id",
]


def widget_by_id(parent, value) -> object:
    """
    Searches the widget tree starting at the specified parent node, looking
    for the given ID.

    :param parent: The head iof the tree within which to search.
    :param value: The ID to find.
    :return: The found object, or None.
    """
    for widget in parent.walk():
        if widget.id == value:
            return widget
    return None
