from typing import Union
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ColorProperty

from kivygw.utils.colors import color_outline

from .label import GWLabel

import logging

LOG = logging.getLogger("main")


__all__ = [
    "GWScrollView",
    "GWScrollingResultsLog",
    "GWResultsLogSection",
    "GWResultsLogEntry",
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
        self.scroll_type = ['bars', 'content']
        self.do_scroll_x = False
        self.bar_width = 6


DEFAULT_NAME_BG_COLOR = (0.8, 0.8, 0.8, 0.25)
DEFAULT_NAME_FG_COLOR = (0.8, 0.8, 0, 1)
DEFAULT_INFO_BG_COLOR = (0, 1, 0, 0.25)
DEFAULT_INFO_FG_COLOR = (1, 1, 1, 1)


class GWResultsLogSection(BoxLayout):
    name_color = ColorProperty()
    info_color = ColorProperty()

    def __init__(self, **kwargs):
        self.size_hint_y = None
        self.size_hint_min_y: 20
        super().__init__(**kwargs)
        self.section_name = GWLabel(
            size_hint=(.15, 1.0), size_hint_min_y=20,
            color=DEFAULT_NAME_FG_COLOR, background_color=DEFAULT_NAME_BG_COLOR,
            halign='right'
            )
        self.section_info = GWLabel(
            size_hint=(.85, 1.0), size_hint_min_y=20,
            color=DEFAULT_INFO_FG_COLOR, background_color=DEFAULT_INFO_BG_COLOR
            )
        self.section_info.bind(texture=self.adjust_entry_height)
        self.add_widget(self.section_name)
        self.add_widget(self.section_info)

    def on_name_color(self, new_color):
        self.section_name.background_color = new_color
        self.section_name.color = color_outline(new_color)

    def on_info_color(self, new_color):
        self.section_info.background_color = new_color
        self.section_info.color = color_outline(new_color)

    def adjust_entry_height(self, instance, texture):
        if texture:
            self.height = texture.height


class GWResultsLogEntry(GWLabel):

    def __init__(self, **kwargs):
        self.color = DEFAULT_INFO_FG_COLOR
        self.background_color = DEFAULT_INFO_BG_COLOR
        self.size_hint_min_y = 20
        self.size_hint_y = None
        self.bind(texture=self.adjust_entry_height)
        super().__init__(**kwargs)

    def adjust_entry_height(self, instance, texture):
        if texture:
            self.height = texture.height


class GWScrollingResultsLog(GWScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_kv_post = self.further_init
        self.sections = {}

    def further_init(self, base_widget):
        self.initialize_actual_results_log_layout()

    def initialize_actual_results_log_layout(self):
        self.results_log_actual = BoxLayout(orientation='vertical', size_hint_y=None, padding=4, spacing=4)
        self.results_log_actual.bind(minimum_height=self.results_log_actual.setter('height'))
        self.add_widget(self.results_log_actual)

    def log_result(self, message: str, entry_color=None):
        if not entry_color:
            entry_color = DEFAULT_INFO_BG_COLOR
        fg_color = color_outline(entry_color)
        msg_label = GWResultsLogEntry(text=message, color=fg_color, background_color=entry_color)
        self.results_log_actual.add_widget(msg_label)
        LOG.debug(f"self.height = {self.height}")
        LOG.debug(f"self.results_log_actual.height = {self.results_log_actual.height}")
        self.scroll_y = 0

    def update_section(self, section_name: str, section_info: Union[str, list], name_color=None, info_color=None):
        """
        Adds or updates a "section" row to the log. This row consists of two
        labels, a section name on the left, and a corresponding section info
        on the right. Keeps track of previous sections by name, and if a name
        reoccurs that section will be updated, as opposed to a new section
        being added to the end.
        """
        if section_name in self.sections:
            section = self.sections[section_name]
        else:
            section = GWResultsLogSection()
            section.section_name.text = section_name
            self.sections[section_name] = section
            self.results_log_actual.add_widget(section, index=-1)  # index=1 means at the bottom except just above the filler

        if isinstance(section_info, list):
            section_info = '\n'.join(section_info)
        section.section_info.text = section_info
