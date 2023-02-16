import logging

from kivy.uix.button import Button
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

    def __init__(self, **kwargs):
        self.background_normal = ''
        self.background_color = NamedColor.GRAY80.float_tuple()
        self._command_action = None
        super().__init__(**kwargs)

    @property
    def command_action(self):
        """The command_action property."""
        return self._command_action

    @command_action.setter
    def command_action(self, value):
        if not isinstance(value, CommandAction):
            raise ConfigError("command_action value must be an instace of CommandAction")
        value.attach_to(self)

