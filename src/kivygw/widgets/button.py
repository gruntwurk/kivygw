import logging

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ColorProperty

from ..widgets.action import CommandActionable
from ..utils.colors import NamedColor, color_outline, color_subdued
from .background import BackgroundColor

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


class GWButton(Button, BackgroundColor, CommandActionable):
    """
    A variation of the kivy Button widget that also inherits from
    `BackgroundColor` and `CommandActionable`. It defaults to
    having no background image so that the background color
    is not muddled.
    """

    def __init__(self, **kwargs):
        # LOG.trace("GWButton initiated.")
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_disabled_normal = ''
        self.background_disabled_down = ''
        self.background_color = 'gray'
        self.color = 'black'

    # def on_background_color(self, instance, color):
    #     self.color = color_outline(color)
    #     self.border_color = color_outline(color)  # color_subdued(color)
    #     LOG.debug(f"GWButton.border_color = {self.border_color}")
    #     LOG.debug(f"GWButton.border_width = {self.border_width}")

