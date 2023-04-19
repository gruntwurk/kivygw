import logging

from kivy.properties import StringProperty, ListProperty, BooleanProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior, FocusBehavior
from kivygw.widgets.background import BackgroundColor

from kivygw.widgets.label import GWLabel

from ..widgets.action import CommandActionable

LOG = logging.getLogger("main")


__all__ = [
    "GWButton",
    "GWCheckBox",
    "GWButtonBar",
]


class GWButtonBar(BoxLayout):
    """
    A container for the action buttons.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = 30


class GWCheckBox(CommandActionable, BackgroundColor, BoxLayout):

    color = ColorProperty()
    active = BooleanProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._checkbox = CheckBox(
            # background_checkbox_normal=None,
            # background_checkbox_down=None,
            # background_checkbox_disabled_normal=None,
            # background_checkbox_disabled_down=None,
            )
        self._checkbox.bind(active=self.setter('active'))
        self._label = Label(text=self.text)
        self.add_widget(self._checkbox)
        self.add_widget(self._label)
        self.bind(color=self.update_color)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self._checkbox.active = self.active

    def update_color(self, *args):
        self._checkbox.color = self.color
        self._label.color = self.color


class GWButton(CommandActionable, ButtonBehavior, FocusBehavior, GWLabel):
    """
    An alternative to the kivy Button widget that also inherits from
    `CommandActionable` and `BackgroundColor` (via `GWLabel`).
    """

    # FYI, Inherited properties:

    # BackgroundColor.background_color
    # BackgroundColor.border_color
    # BackgroundColor.border_width
    # BackgroundColor.corner_radius
    # BackgroundColor.rounded
    # CommandActionable.shortcut
    # CommandActionable.handler_name
    # GWLabel.text_padding

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = 'center'
        self.valign = 'middle'
