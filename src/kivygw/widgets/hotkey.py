import logging
from kivy.uix.widget import Widget
from kivy.properties import DictProperty
from kivy.core.window import Window
from kivy.app import App

from ..utils.keystrokes import generic_keystroke, parse_keystroke_expression

LOG = logging.getLogger("kivygw")


__ALL__ = [
    'MultiKeystrokeListener',
]

TAB = 9
ENTER = 13


class MultiKeystrokeListener(Widget):
    """
    An invisble widget that listens to the keyboard for complete multi-keystroke
    combinations, e.g. ctrl+shift+f1. All other noisy events are ignored.
    For example, on the way to the ctrl+shift+f1 combination, we get three
    key_down and three key_up events, but only the last key_down event is
    significant. Here, we call that a "key press".

    :param on_key_press: A callable to handle the resultant key press (the one
    significant key_down). This function needs to accept a list of one or more
    integers, one of which is the key (e.g. 97 for "a") and the rest, if any, are
    modifiers (e.g. 304 for "shift"). It then needs to return True if it
    recognizes the keystroke and handles it; otherwise, returning False tells
    the system handle it.
    """

    shortcut_index = DictProperty({})
    '''
    :attr:`shortcut_index` is a :class:`~kivy.properties.DictProperty` and defaults to an empty dictionary.
    '''

    def __init__(self, **kwargs):
        super(MultiKeystrokeListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        # if self._keyboard.widget:
        #     # If it exists, this widget is a VKeyboard object which you can use
        #     # to change the keyboard layout.
        #     pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.on_kv_post = self.further_init
        self.app: App = App.get_running_app()

    def further_init(self, base_widget):
        # Establish the shortcut index dictioanry
        self.shortcut_index = {}
        # For convenience, set a link to the dictionary at the app level.
        self.app.shortcut_index = self.shortcut_index

    def _keyboard_closed(self):
        pass
        # self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        # self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """
        This handler is called spuriously. For example, on the way to a
        ctrl+alt+f1, it gets called for each of the keydowns:
            ctrl, ctrl+shift, ctrl+shift+f1.
        Also, if there is a pause in between, then the keyboard may auto
        repeat, as in:
            ctrl, ctrl, ctrl, ctrl, ctrl, ctrl, ctrl+shift, ctrl+shift+f1
        So, we just want to remember the last call, then only act on it
        once we start to receive key_up calls.
        """
        self.latest_down = (keycode, modifiers)
        # print('--- DOWN ---')
        # print('keycode[0]:', keycode[0])
        # print('keycode[1]:', keycode[1])
        # print('text:', text)
        # print('modifiers:', modifiers)

        # Return True to accept the key. Otherwise, it will be used by the system.
        return True

    def _on_keyboard_up(self, _, __):
        # Now we can act on the last keydown we saw.
        if not self.latest_down:
            # This keypress was already handled
            return True

        keycode, modifiers = self.latest_down
        self.latest_down = None
        # Clearing latest_down ensures that we only act once, e.g. in the case
        # of ctrl+shift+f1, we'll get 3 calls to key_up (in random order).

        # `do_key_press` needs to returns true if it recognizes the keystroke
        # and handles it; otherwise, False tells the system handle it.
        return self.do_key_press(parse_keystroke_expression(modifiers, keycode[0]))

    def do_key_press(self, key_ints) -> bool:
        for ki in [tuple(key_ints), tuple(generic_keystroke(key_ints))]:
            if ki in self.shortcut_index.keys():
                return self.shortcut_index[ki].invoke()
        return False
