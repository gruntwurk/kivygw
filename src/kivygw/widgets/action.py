import logging
from kivy.uix.widget import Widget

from ..utils.keystrokes import parse_keystroke_expression

LOG = logging.getLogger("kivygw")


__ALL__ = [
    'CommandAction',
]


class CommandAction(Widget):
    """
    A single command can often be invoked via multiple paths through the UI (a
    menu item, a toolbar button, a keyboard shortcut, etc.) This invisible
    (logical) widget allows for such an action to be defined independently from
    the widget(s) that invoke it.
    """

    def __init__(self, **kwargs):
        self.register_event_type('on_invoke')
        super().__init__(**kwargs)
        self._text = ""
        self._enabled = True
        self._checkable = False
        self._checked = False
        self._shortcut = None
        self._callback = None
        self._associated_widgets = []

    def on_invoke(self):
        pass

    @property
    def text(self):
        """The text property."""
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        if self._text:
            for associated_widget in self._associated_widgets:
                if hasattr(associated_widget, "text"):
                    associated_widget.text = self._text

    @property
    def enabled(self):
        """The enabled property."""
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def checked(self) -> bool:
        """The checked property."""
        return self._checked

    @checked.setter
    def checked(self, value: bool):
        self._checked = value

    @property
    def checkable(self) -> bool:
        """
        Whether or not the action is checkable (i.e. has an on/off state). In a
        text editor, for example, a Bold toolbar button may be either on or off
        to indicate whether the text currently being typed is to be bold or not.
        In contrast, a non-checkable action is simply executed once.
        """
        return self._checkable

    @checkable.setter
    def checkable(self, value):
        self._checkable = value

    @property
    def shortcut(self):
        """The shortcut property."""
        return self._shortcut

    @shortcut.setter
    def shortcut(self, value):
        self._shortcut = parse_keystroke_expression(value)

    def invoke(self):
        """
        This method can be called directly to invoke/activate/deactivate the
        command, although it is usually called indirectly via some other widget.

        NOTE: If this CommandAction is disabled, then nothing happens.
        """
        if not self.enabled:
            return
        if self.checkable:
            self.checked = not self.checked
        self.dispatch('on_invoke')

    def attach_to(self, associated_widget):
        self._associated_widgets.append(associated_widget)
        associated_widget._command_action = self
        if hasattr(associated_widget, "on_release"):
            associated_widget.on_release = self.invoke
        if hasattr(associated_widget, "text"):
            associated_widget.text = self._text

    def associated_widgets(self):
        """
        Returns a list of widgets this action has been attached to.
        """
        return self._associated_widgets







