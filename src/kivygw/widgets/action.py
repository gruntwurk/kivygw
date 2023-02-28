import logging
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.app import App

from kivygw.utils.keystrokes import keystroke_expression, parse_keystroke_expression
from kivygw.utils.strings import normalize_name

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
        associated_widget.text = str(name)


def propogate_widget_disabled(associated_widget, is_now_disabled):
    """
    Propogates the CommandAction enabled/`disabled` status to the associated
    widget (e.g. a button or a menu item).
    """
    if hasattr(associated_widget, "disabled"):
        associated_widget.disabled = bool(is_now_disabled)


# ############################################################################
#                                                        COMMAND ACTION WIDGET
# ############################################################################

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

    shortcut_codes = ListProperty([])
    '''
    The (computed) keyboard shortcut codes (list of int), if any.
    Use the `shortcut` property to get/set tose codes via the equivalent keystroke expression
    (e.g. `cmd_action.shortcut = 'ctrl+shift+F12'`).

    :attr:`shortcut_codes` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    '''

    associated_widgets = ListProperty([])
    '''
    :attr:`associated_widgets` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_invoke')
        super().__init__(**kwargs)
        self.app: App = App.get_running_app()

    @property
    def shortcut_index(self):
        """Convienence getter for the shortcut_index dictionary, which is kept in the app."""
        if not hasattr(self.app, 'shortcut_index'):
            self.app.shortcut_index = {}
        return self.app.shortcut_index

    @property
    def shortcut(self):
        return keystroke_expression(self.shortcut_codes)

    @shortcut.setter
    def shortcut(self, value):
        self.shortcut_codes = parse_keystroke_expression(value)

    def on_text(self, instance, value):
        if value:
            for associated_widget in self.associated_widgets:
                propogate_widget_text(associated_widget, value)

    def on_disabled(self, instance, is_now_disabled):
        for associated_widget in self.associated_widgets:
            propogate_widget_disabled(associated_widget, is_now_disabled)

    def on_shortcut_codes(self, instance, value):
        # FIXME Unregister the old codes first, if any
        self.register_keyboard_shortcut()

    def on_invoke(self, *args):
        pass

    def invoke(self, *args):
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

    def register_keyboard_shortcut(self):
        # Casting the ListProperty to a tuple is necessary to make it hashable.
        if self.shortcut_codes:
            self.shortcut_index[tuple(self.shortcut_codes)] = self

    def find_and_set_handler(self, associated_widget: Widget):
        """
        Walks up the widget tree, parent by parent, until we find the handler_name
        method we're looking for, or we run out of parents.
        Once found, we bind that method to the CommandAction.

        :param handler_method_name: The name of the handler_name method.
        :return: A reference to the method, or None.
        """
        handler_method_name = associated_widget.handler_name
        widget = associated_widget
        while widget := widget.parent:
            if not hasattr(widget, handler_method_name):
                continue
            self.on_invoke = getattr(widget, handler_method_name)
            return
        # No handler found, maybe we just haven't loaded the handler_name property directly yet


    def attach_to(self, associated_widget: Widget):
        if associated_widget in self.associated_widgets:
            return  # already attached

        self.associated_widgets.append(associated_widget)
        associated_widget._command_action = self
        associated_widget.on_release = self.invoke

        self.find_and_set_handler(associated_widget)

        propogate_widget_text(associated_widget, self.text)

    def any_associated_widget_in_play(self) -> bool:
        """
        Checks if any of the associated widgets are currently visible.

        :return: True if at least one widget is visible.
        """
        # If we're not descended from a window, then we are not in play (not visible)
        return any(aw.get_parent_window() for aw in self.associated_widgets)


# ############################################################################
#                                                     COMMAND ACTIONABLE MIXIN
# ############################################################################

class CommandActionable(Widget):
    """
    A composable widget for allowing another widget to be controlled by a `CommandAction`.

    Example (in the `.kv` file)
    ~~~~
    <MyButton@Button+CommandActionable>
        ...
    ~~~~

    See also GWButton.
    """
    shortcut = StringProperty("")
    handler_name = StringProperty("")

    def __init__(self, **kwargs):
        self.register_event_type('on_invoke')
        self._command_action = None
        super().__init__(**kwargs)
        self.bind(text=self.calc_handler_name)

    @property
    def command_action(self) -> CommandAction:
        """
        Get-accessor for the command_action object associated with this widget.
        If one doesn't currently exist, it will be automatically created.
        """
        if not hasattr(self, '_command_action') or not self._command_action:
            cmd_action = CommandAction(text=self.text)
            cmd_action.attach_to(self)
        return self._command_action

    def on_invoke(self, *args):
        pass

    def on_shortcut(self, instance, keystroke_expression):
        # Setting the keyboard shortcut in the associated widget is just a
        # convenience so that we don't have to manually declare the
        # `CommandAction` in the KV file and link it to the widget. The
        # widget's `command_action` get-accessor does that for us.
        self.command_action.shortcut = keystroke_expression

    def calc_handler_name(self, instance, text):
        if not self.handler_name:
            self.handler_name = f'_{normalize_name(text).lower()}_action'

    def on_handler_name(self, instance, handler_name):
        # Setting the name of the handler_name method in the associated widget is
        # just a convenience so that we don't have to manually declare the
        # `CommandAction` in the KV file and link it to the widget. The
        # widget's `command_action` get-accessor does that for us.
        if self.command_action:
            self.command_action.find_and_set_handler(self)
