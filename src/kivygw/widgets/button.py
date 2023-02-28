import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

from kivygw.widgets.label import GWLabel

from ..widgets.action import CommandActionable

LOG = logging.getLogger("main")


__all__ = [
    "GWButton",
    "GWButtonBar",
]


class GWButtonBar(BoxLayout):
    """
    A container for the action buttons.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = 30


class GWButton(CommandActionable, ButtonBehavior, GWLabel):
    """
    An alternative to the kivy Button widget that also inherits from
    `CommandActionable` and `BackgroundColor` (via `GWLabel`).
    """

    # FYI, Inherited properties:

    # BackgroundColor.background_color = ColorProperty()
    # BackgroundColor.border_color
    # BackgroundColor.border_width
    # BackgroundColor.corner_radius
    # CommandActionable.shortcut
    # CommandActionable.handler_name
    # GWLabel.text_padding

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_color = 'gray'
        self.color = 'black'
