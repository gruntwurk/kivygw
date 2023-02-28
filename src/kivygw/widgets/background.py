import logging
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Color, RoundedRectangle
from kivy.properties import ColorProperty, NumericProperty, ListProperty

from kivygw.utils.colors import color_outline, color_subdued

LOG = logging.getLogger("kivygw")
TRANSPARENT = (0, 0, 0, 0)

__ALL__ = [
    'BackgroundColor',
]


class BackgroundColor(Widget):
    """
    A composable widget for setting the background color of another widget.

    Example (in the `.kv` file)
    ~~~~
    <MyLabel@Label+BackgroundColor>
        background_color: 0, 1, 0, 0.25
        border_width: 2
        border_color: 1, 0, 0, 0.25
        corner_radius: 0

    ~~~~

    See also GWLabel.
    """
    background_color = ColorProperty('silver')
    border_color = ColorProperty(None)
    border_width = NumericProperty(2)
    corner_radius = ListProperty([3,])

    def __init__(self, **kwargs):
        # LOG.trace("BackgroundColor Mixin initiated.")
        super().__init__(**kwargs)
        self.bind(pos=self.update_rect_sizes)
        self.bind(size=self.update_rect_sizes)
        self.bind(border_width=self.update_rect_sizes)

        self.bind(background_color=self.update_rect_colors)
        self.bind(border_color=self.update_rect_colors)

        c: Canvas = self.canvas
        with c.before:
            self.outer_color = Color(self.background_color)
            self.outer_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.corner_radius)
            self.inner_color = Color(rgba=TRANSPARENT)
            self.inner_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.corner_radius)

        self.update_rect_colors()
        self.update_rect_sizes()

    def update_rect_colors(self, *args):
        # LOG.debug(f"BackgroundColor.background_color = {self.background_color}")
        # LOG.debug(f"BackgroundColor.border_color = {self.border_color}")
        self.border_color = [0, 0, 0, 0]  # color_subdued(self.background_color)
        self.color = color_outline(self.background_color)

        self.outer_color.rgba = self.border_color
        self.inner_color.rgba = self.background_color

    def update_rect_sizes(self, *args):
        self.outer_rect.pos = self.pos
        self.outer_rect.size = self.size
        self.inner_rect.pos = (self.x + self.border_width, self.y + self.border_width)
        self.inner_rect.size = (self.width - self.border_width * 2, self.height - self.border_width * 2)



