import logging
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Color, Rectangle
from kivy.properties import ColorProperty, NumericProperty

from kivygw.utils.colors import color_subdued

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

    ~~~~

    See also GWLabel.
    """
    background_color = ColorProperty()
    border_color = ColorProperty()
    border_width = NumericProperty(2)

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
            self.outer_color = Color(rgba=self.border_color or self.background_color)
            self.outer_rect = Rectangle(pos=self.pos, size=self.size)
            self.inner_color = Color(rgba=self.background_color if self.border_color else TRANSPARENT)
            self.inner_rect = Rectangle(pos=self.pos, size=self.size)

        self.update_rect_colors()
        self.update_rect_sizes()

    def update_rect_colors(self, *args):
        # LOG.debug(f"BackgroundColor.background_color = {self.background_color}")
        # LOG.debug(f"BackgroundColor.border_color = {self.border_color}")
        if not self.border_color:
            self.border_color = color_subdued(self.background_color)
        self.outer_color.rgba = self.border_color
        self.inner_color.rgba = self.background_color

    def update_rect_sizes(self, *args):
        self.outer_rect.pos = self.pos
        self.outer_rect.size = self.size
        self.inner_rect.pos = (self.pos[0] + self.border_width, self.pos[1] + self.border_width)
        self.inner_rect.size = (self.size[0] - self.border_width * 2, self.size[1] - self.border_width * 2)



