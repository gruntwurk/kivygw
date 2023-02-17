import logging

from kivy.uix.button import Button
from kivy.properties import ObjectProperty

from ..utils.exceptions import ConfigError
from ..widgets.action import CommandAction
from ..utils.colors import NamedColor
from .background import BackgroundColor

LOG = logging.getLogger("kivygw")


__all__ = [
    "GWButton",
]


class GWButton(Button, BackgroundColor):
    """
    A variation of the kivy Button widget that also inherits from BackgroundColor.
    It defaluts to having no background image so that the background color
    is not muddled. The default background color is 20% gray.
    """

    command_action = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.background_normal = ''
        self.background_color = NamedColor.GRAY80.float_tuple()
        self._command_action = None
        super().__init__(**kwargs)

    def on_command_action(self, instance, value):
        if not isinstance(value, CommandAction):
            raise ConfigError("command_action value must be an instance of CommandAction")
        value.attach_to(self)

