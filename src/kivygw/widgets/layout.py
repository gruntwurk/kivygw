import itertools
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

__all__ = [
    'GWMultiColumnLayout',
]

import logging

LOG = logging.getLogger("main")

# class FixedGridLayout(BoxLayout):
#     rows = NumericProperty()
#     cols = NumericProperty()
#     min_width = NumericProperty()
#     min_height = NumericProperty()
#     font_size = NumericProperty()

#     def __init__(self, rows=0, cols=0, min_width=0, min_height=0, font_size=12, **kwargs):
#         super().__init__(**kwargs)
#         self.rows = rows
#         self.cols = cols
#         self.min_width = min_width
#         self.min_height = min_height
#         self.font_size = font_size
#         self.orientation = 'vertical'
#         self.construct_grid()
#         self.size_hint_y = None
#         self.bind(rows=self.construct_grid)
#         self.bind(cols=self.construct_grid)
#         self.bind(font_size=self.resize_font)

#     def construct_grid(self, *args):
#         if self.rows * self.cols == 0:
#             # nothing to do, leave the current grid, if any, alone
#             return
#         self.clear_widgets()
#         self.cells = []
#         for _ in range(self.rows):
#             row_cells = []
#             self.cells.append(row_cells)
#             row_widget = BoxLayout(orientation='horizontal', size_hint_y=None, size_hint_min_y=self.min_height)
#             self.add_widget(row_widget)
#             for _ in range(self.cols):
#                 cell_widget = BoxLayout(size_hint_min_y=self.min_height)
#                 row_cells.append(cell_widget)
#                 row_widget.add_widget(cell_widget)

#     def set_cell(self, col, row, widget):
#         cell: BoxLayout = self.cells[row][col]
#         cell.clear_widgets()
#         cell.add_widget(widget)
#         cell.size_hint_y = None
#         widget.bind(height=cell.setter('height'))

#     def resize_font(self, *args):
#         for row, col in itertools.product(range(self.rows), range(self.cols)):
#             if self.cells[row][col].children:
#                 widget = self.cells[row][col].children[0]
#                 widget.font_size = self.font_size


class GWMultiColumnLayout(BoxLayout):
    cols = NumericProperty()
    min_col_width = NumericProperty()
    font_size = NumericProperty()

    def __init__(self, cols=0, min_width=0, font_size=12, **kwargs):
        super().__init__(**kwargs)
        self.cols = cols
        self.min_width = min_width
        self.font_size = font_size
        self.orientation = 'horizontal'

    def on_kv_post(self, base_widget):
        self.size_hint_y = None
        self.bind(cols=self.construct_grid)
        super().on_kv_post(base_widget)
        self.construct_grid()

    @property
    def columns(self):
        return self._columns

    def construct_grid(self, *args):
        if self.cols <= 0:
            return
        self.clear_widgets()
        self._columns = []
        for _ in range(self.cols):
            column_widget = BoxLayout(
                orientation='vertical',
                size_hint_min_x=self.min_col_width,
                size_hint_y=None,
                pos_hint={'top': 1}
                )
            column_widget.bind(minimum_height=column_widget.setter('height'))
            self._columns.append(column_widget)
            self.add_widget(column_widget)

    def visit_all_children(self, do_something: callable):
        for column in self.columns:
            for child in column.children:
                do_something(child)
