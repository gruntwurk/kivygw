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


DEFAULT_NAME_COLOR = 'firebrick'
DEFAULT_INFO_COLOR = 'gold'


class GWResultsLogSection(BoxLayout):
    name_color = ColorProperty(DEFAULT_NAME_COLOR)
    info_color = ColorProperty(DEFAULT_INFO_COLOR)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.size_hint_min_y: 20
        self.section_name = GWLabel(
            size_hint=(.15, 1.0), size_hint_min_y=20,
            # color=color_outline(self.name_color),
            background_color=self.name_color,
            halign='right'
            )
        self.section_info = GWLabel(
            size_hint=(.85, 1.0), size_hint_min_y=20,
            # color=color_outline(self.info_color),
            background_color=self.info_color
            )
        self.section_info.bind(texture=self.adjust_entry_height)
        self.bind(name_color=self.update_name_color)
        self.bind(info_color=self.update_info_color)
        self.add_widget(self.section_name)
        self.add_widget(self.section_info)

    def update_name_color(self, instance, color):
        self.section_name.background_color = color
        self.section_name.color = color_outline(color)
        self.section_name.border_color = color_outline(color)

    def update_info_color(self, instance, color):
        self.section_info.background_color = color
        self.section_info.color = color_outline(color)
        self.section_info.border_color = color_outline(color)

    def adjust_entry_height(self, instance, texture):
        if texture:
            self.height = texture.height


class GWResultsLogEntry(GWLabel):
    def __init__(self, **kwargs):
        self.size_hint_min_y = 20
        self.size_hint_y = None
        self.bind(texture=self.adjust_entry_height)
        self.bind(background_color=self.update_entry_color)
        super().__init__(**kwargs)

    def adjust_entry_height(self, instance, texture):
        if texture:
            self.height = texture.height

    def update_entry_color(self, instance, color):
        self.color = color_outline(color)
        self.border_color = color_outline(color)


class GWScrollingResultsLog(GWScrollView):
    default_name_color = ColorProperty(DEFAULT_NAME_COLOR)
    default_info_color = ColorProperty(DEFAULT_INFO_COLOR)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sections = {}

    def on_kv_post(self, base_widget):
        self.initialize_actual_results_log_layout()
        super().on_kv_post(base_widget)

    def initialize_actual_results_log_layout(self):
        self.results_log_actual = BoxLayout(orientation='vertical', size_hint_y=None, padding=4, spacing=4)
        self.results_log_actual.bind(minimum_height=self.results_log_actual.setter('height'))
        self.add_widget(self.results_log_actual)

    def log_result(self, message: str, entry_color=None):
        if not entry_color:
            entry_color = self.default_info_color
        msg_label = GWResultsLogEntry(text=message, color=color_outline(entry_color), background_color=entry_color)
        self.results_log_actual.add_widget(msg_label)
        LOG.debug(f"self.height = {self.height}")
        LOG.debug(f"self.results_log_actual.height = {self.results_log_actual.height}")

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
            section = GWResultsLogSection(
                name_color=name_color or self.default_name_color,
                info_color=info_color or self.default_info_color
                )
            section.section_name.text = section_name
            self.sections[section_name] = section
            self.results_log_actual.add_widget(section)

        if isinstance(section_info, list):
            section_info = '\n'.join(section_info)

        section.section_info.text = section_info
