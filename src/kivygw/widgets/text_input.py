from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import FocusBehavior

__all__ = [
    'GWTextInput',
]


class GWTextInput(TextInput, FocusBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write_tab = False
        self.text = ""
        self.multiline = False
