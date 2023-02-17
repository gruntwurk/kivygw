import logging
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.app import App

LOG = logging.getLogger("kivygw")


__ALL__ = [
    'CommandAction',
    'propogate_widget_text',
]


def propogate_widget_text(associated_widget, name):
    """
    Propogates the CommandAction `name` to the associated widget (e.g. a button
    or menu item).
    """
    if hasattr(associated_widget, "text"):
        associated_widget.text = name


class CommandAction(Widget):
    """
    A single command can often be invoked via multiple paths through the UI (a
    menu item, a toolbar button, a keyboard shortcut, etc.) This invisible
    (logical) widget allows for such an action to be defined independently from
    the widget(s) that invoke it.
    """

    text = StringProperty("")
    '''
    Name for the action as it is to appear on an associated button and/or menu item.

    :attr:`name` is a :class:`~kivy.properties.StringProperty` and defaults to "".
    '''

    enabled = BooleanProperty(True)
    '''
    Whether or not the action is currently enabled.

    :attr:`enabled` is a :class:`~kivy.properties.BooleanProperty` and defaults to True.
    '''

    checkable = BooleanProperty(False)
    '''
    Whether or not the action has a checked state. If so, then invoking the
    action causes the checked property to be toggled.

    In a text editor, for example, a Bold toolbar button may be either on or off
    to indicate whether the text currently being typed is to be bold or not.
    In contrast, a non-checkable action is simply executed once.

    :attr:`checkable` is a :class:`~kivy.properties.BooleanProperty` and defaults to False.
    '''

    checked = BooleanProperty(False)
    '''
    The current check state.

    :attr:`checked` is a :class:`~kivy.properties.BooleanProperty` and defaults to False.
    '''

    shortcut = ListProperty([])
    '''
    The (computed) keyboard shortcut codes, if any. Use `parse_keystroke_expression`
    to compute the codes from an expression (e.g.
    `shortcut = parse_keystroke_expression('ctrl+shift+F12')`.

    :attr:`shortcut` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    '''

    associated_widgets = ListProperty([])
    '''
    :attr:`associated_widgets` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_invoke')
        super().__init__(**kwargs)
        self.app: App = App.get_running_app()

    def on_invoke(self):
        pass

    def on_text(self, instance, value):
        if value:
            for associated_widget in self.associated_widgets:
                propogate_widget_text(associated_widget, value)

    def invoke(self):
        """
        This method can be called directly to invoke/activate/deactivate the
        command, although it is usually called indirectly via some other widget.

        NOTE: If this CommandAction is disabled, then nothing happens.
        """
        if self.disabled:
            return
        if not self.any_associated_widget_in_play():
            return
        if self.checkable:
            self.checked = not self.checked
        self.dispatch('on_invoke')

    def attach_to(self, associated_widget):
        if self.shortcut:
            self.app.shortcut_index[tuple(self.shortcut)] = self
        self.associated_widgets.append(associated_widget)
        # self.associated_widgets.get(self).append(associated_widget)
        associated_widget._command_action = self
        if hasattr(associated_widget, "on_release"):
            associated_widget.on_release = self.invoke
        propogate_widget_text(associated_widget, self.text)

    def any_associated_widget_in_play(self) -> bool:
        # If we're not descended from a window, then we are not in play (not visible)
        return any(aw.get_parent_window() for aw in self.associated_widgets)

