import logging

from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty
from .background import BackgroundColor

LOG = logging.getLogger("main")

__all__ = [
    "GWLabel",
    "GWStatusBar",
]


class GWLabel(BackgroundColor, Label):
    """
    A variation of the kivy Label widget that defaults to using the whole space
    alloted to the label (rather than always centering the text).
    It also inherits from BackgroundColor. Thus, all of these properties can be combined:

    * text_padding (new) defaults to [6, 2] (i.e. left/right = x = 6, top/bottom = y = 2)
    * background_color (from BackgroundColor) is required.
    * halign now defaults to 'left'.
    * valign now defaults to 'top'.

    For example, if the label is 200px x 100px, and the text_padding is 8, then
    the text rectangle will be 184 x 84 (centered), and the text will placed in
    the upper left of that.
    """
    text_padding_x = NumericProperty(6)
    text_padding_y = NumericProperty(2)
    text_padding = ReferenceListProperty(text_padding_x, text_padding_y)

    def __init__(self, **kwargs):
        # LOG.trace("GWLabel initiated.")
        super().__init__(**kwargs)
        self.halign = 'left'
        self.valign = 'top'
        self.markup = True
        self.bind(pos=self.recalc_text_size)
        self.bind(size=self.recalc_text_size)
        self.bind(texture=self.adjust_entry_height)

    def adjust_entry_height(self, instance, texture):
        if not texture:
            return
        # LOG.trace("Reacting to texture size change")
        new_height = texture.height + (2 * self.text_padding_y)
        # This if-statement guards against an infinate loop (changing the height calls on_size)
        # LOG.debug("new_height = {}".format(new_height))
        # LOG.debug("self.height = {}".format(self.height))
        if new_height != self.height:
            # LOG.debug("setting new height")
            self.height = new_height

    def recalc_text_size(self, *args):
        text_width_available = self.size[0] - (2 * self.text_padding_x)
        if self.text_size[0] != text_width_available:
            # LOG.trace("Recalculating text dimensions.")
            self.text_size = (text_width_available, None)
            self.texture_update()


class GWStatusBar(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 30
        self.background_color = 'lightgray'


