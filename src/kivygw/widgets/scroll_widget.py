from typing import Union
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ColorProperty

from kivygw.utils.colors import color_outline, color_parse, float_tuple

from .label import GWLabel

import logging

LOG = logging.getLogger("main")
DEFAULT_NAME_COLOR = 'salmon'
DEFAULT_INFO_COLOR = 'khaki'
MIN_HEIGHT = 24

__all__ = [
    "GWScrollView",
    "GWScrollingResultsLog",
    "GWResultsLogPair",
    "GWResultsLogSingle",
]


class GWScrollView(ScrollView):
    """
    A ScrollView that defaults to vertical scrolling using a scroll bar (or the wheel).

    NOTE: If the content widget (box layout, grid layout, etc.) is specified in code
    (as opposed to in the KV file), then be sure to call `ensure_content_scrolls()`
    after adding it.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # A common mistake is to forget to set the scroll_type
        self.scroll_type = ['bars', 'content']
        self.do_scroll_x = False
        self.do_scroll_y = True

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.ensure_content_scrolls()

    def ensure_content_scrolls(self):
        """
        Make sure that the contents of the scroll window (usually a box layout
        or a grid layout) actually grows beyond the height of the scroll window
        (as opposed to squeezing it all in).
        """
        for content_pane in self.children:
            content_pane.size_hint_y = None
            content_pane.bind(minimum_height=content_pane.setter('height'))


class GWResultsLogPair(BoxLayout):
    """
    This is how a name/value pair is rendered within a GWScrollingResultsLog.
    i.e. a horizontal BoxLayout with two labels: "name" and "info".
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.size_hint_min_y: MIN_HEIGHT
        self.entry_name = GWLabel(size_hint=(.15, 1.0), halign='right')
        self.entry_info = GWLabel(size_hint=(.85, 1.0))
        self.add_widget(self.entry_name)
        self.add_widget(self.entry_info)
        self.entry_info.bind(size=self.update_size)

    def update_size(self, instance, size):
        self.height = size[1]


class GWResultsLogSingle(GWLabel):
    """
    This is how a simple entry is rendered within a GWScrollingResultsLog.
    i.e. a single GWLabel.
    """
    def __init__(self, **kwargs):
        self.size_hint_min_y = MIN_HEIGHT
        self.size_hint_y = None
        self.bind(background_color=self.update_entry_color)
        super().__init__(**kwargs)

    def update_entry_color(self, instance, color):
        self.color = color_outline(color)
        self.border_color = color_outline(color)


class GWScrollingResultsLog(GWScrollView):
    default_name_color = ColorProperty(DEFAULT_NAME_COLOR)
    default_info_color = ColorProperty(DEFAULT_INFO_COLOR)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entry_pairs = {}

    def on_kv_post(self, base_widget):
        self.initialize_actual_results_log_layout()
        super().on_kv_post(base_widget)

    def initialize_actual_results_log_layout(self):
        self.results_log_actual = BoxLayout(orientation='vertical', padding=4, spacing=4)
        self.add_widget(self.results_log_actual)
        self.ensure_content_scrolls()

    def log_result(self, info: Union[str, list], name=None, info_color=None, name_color=None):
        """
        Adds an entry to the scrolling log.

        :param info: The information to present. Can be a single string or a
            list of strings. NOTE: If this parameter is empty, then nothing
            happens.
        :param entry_name: (Optional) A name for the entry, which will appear
            in its own label to the left of the info label. Defaults to None.
        :param info_color: (Optional) A unique background color for the info
            label of this particular entry; otherwise, the `default_info_color`
            is used.
        :param name_color: (Optional) A unique background color for the name
            label (if there is one) of this particular entry; otherwise, the
            `default_name_color` is used.
        """
        if not info:
            return

        if isinstance(info, list):
            info = '\n'.join(info)

        info_color = float_tuple(color_parse(info_color, default=self.default_info_color), alpha=1.0)
        name_color = float_tuple(color_parse(name_color, default=self.default_name_color), alpha=1.0)

        if not name:
            self.results_log_actual.add_widget(GWResultsLogSingle(text=info, background_color=info_color))
            return

        entry = GWResultsLogPair()
        entry.entry_name.background_color = name_color
        entry.entry_info.background_color = info_color
        entry.entry_name.text = name
        entry.entry_info.text = info
        self.results_log_actual.add_widget(entry)

