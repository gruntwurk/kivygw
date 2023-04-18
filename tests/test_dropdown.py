from enum import Enum, unique
from kivygw import GWButton
# import pytest
from kivygw.utils.colors import int_tuple

from kivygw.widgets.dropdown import colorize_widget_per_enum

KHAKI = (240, 230, 140, 255)
PINK = (255, 192, 203, 255)
RED = (255, 0, 0, 255)
ORANGE = (255, 165, 0, 255)
YELLOW = (255, 255, 0, 255)


@unique
class Fruit(Enum):
    apple = ('Apples are usually red', RED)
    orange = ('Oranges are orange', ORANGE)
    lemon = ('Lemons are yellow', YELLOW)
    grapefruit = ('Grapefruits can be pink', PINK)

    def description(self) -> str:
        return self.value[0]

    def color(self) -> tuple:
        return self.value[1]


def test_colorize_widget_per_enum():
    w = GWButton()
    assert int_tuple(w.background_color) == KHAKI

    w.text = 'Not a fruit'
    colorize_widget_per_enum(w, Fruit)
    assert int_tuple(w.background_color) == KHAKI

    w.text = 'Apples are usually red'
    colorize_widget_per_enum(w, Fruit)
    assert int_tuple(w.background_color) == RED

    w.text = 'Oranges are orange'
    colorize_widget_per_enum(w, Fruit)
    assert int_tuple(w.background_color) == ORANGE

    w.text = 'Lemons are yellow'
    colorize_widget_per_enum(w, Fruit)
    assert int_tuple(w.background_color) == YELLOW
