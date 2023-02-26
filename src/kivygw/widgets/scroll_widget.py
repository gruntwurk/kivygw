from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ColorProperty

from kivygw.utils.colors import color_outline, int_tuple

from .label import GWLabel


__all__ = [
    "GWScrollView",
    "GWScrollingResultsLog",
]

GREEN_TRANSLUCENT = [0, 1, 0, 0.25]


class GWScrollView(ScrollView):
    """
    A ScrollView that defaults to vertical scrolling using a scroll bar (or the wheel).

    NOTE: Make sure the contents of the scrollview have `size_hint_y: None`;
    otherwise Kivy will compress the contents to fill the view, defeating the
    point of scrolling.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # A common mistake is to forget to set the scroll_type
        self.scroll_type = ['bars']
        self.do_scroll_x = False
        self.bar_width = 6


class GWScrollingResultsLog(GWScrollView):

    default_entry_color = ColorProperty(GREEN_TRANSLUCENT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_kv_post = self.further_init

    def further_init(self, base_widget):
        self.initialize_actual_results_log_layout()

    def initialize_actual_results_log_layout(self):
        self.results_log_actual = BoxLayout(orientation='vertical', size_hint_y=None, padding=4, spacing=4)
        self.results_log_actual.id = "_results_log_actual"
        self.add_widget(self.results_log_actual)

        filler = Label(size_hint=(1, 1))
        filler.id = "_results_log_filler"
        # filler.pos = self.parent.pos
        self.results_log_actual.add_widget(filler)

    def log_result(self, message: str, entry_color=None):
        if not entry_color:
            entry_color = self.default_entry_color
        color_outline(int_tuple(entry_color))
        msg_label = GWLabel(text=message, background_color=entry_color, size_hint=(1, .02), size_hint_min_y=20)
        self.results_log_actual.add_widget(msg_label, index=1)  # index=1 means at the bottom except just above the filler

