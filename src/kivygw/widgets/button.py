import logging

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from ..widgets.action import CommandActionable
from ..utils.colors import NamedColor
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
    is not muddled. The default background color is 20% gray.
    """

    button_color = StringProperty("GRAY80")

    def __init__(self, **kwargs):
        # LOG.trace("GWButton initiated.")
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_disabled_normal = ''
        self.background_disabled_down = ''
        self.background_color = NamedColor.GRAY80.float_tuple()
        self.color = NamedColor.BLACK.float_tuple()

    def on_button_color(self, instance, color_name):
        named_color = NamedColor.by_name(color_name)
        # LOG.debug(f"on_button_color named_color = {named_color}")
        if named_color:
            self.background_color = named_color.float_tuple()
            self.color = named_color.outline().float_tuple()
            self.border_color = named_color.outline().float_tuple(alpha=0.5)
            # LOG.debug(f"self.border_color = {self.border_color}")
            # LOG.debug(f"self.border_width = {self.border_width}")

