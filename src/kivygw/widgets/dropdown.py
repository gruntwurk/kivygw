import logging
from enum import Enum
from kivy.uix.spinner import Spinner, SpinnerOption
# from kivy.uix.dropdown import DropDown
from kivy.properties import NumericProperty, StringProperty

from kivygw.utils.enums import enum_by_value

from ..utils.colors import float_tuple, color_outline, is_color
from ..utils.class_utils import class_from_name

__ALL__ = [
    'EnumDropDown'
]

LOG = logging.getLogger("kivygw")
DEFAULT_DROPDOWN_SELECTION_HEIGHT = 40


class DropDownChoice(SpinnerOption):
    def __init__(self, text: str, **kwargs):
        super(DropDownChoice, self).__init__(text=text, **kwargs)

    def configure(self, parent, *args):
        self.height = parent.height_per
        colorize_widget_per_enum(self, parent.enum_class)


class EnumDropDown(Spinner):
    """
    A dropdown widget (aka. spinner) that auto-populates with all of the
    possible values of a given Enum class.

    * If the Enum class has a class method called `default()`, then
      that method will determine the initial value for the spinner;
      otherwise, the first value in the list (as declared in the enum class)
      will be used.
    * If the Enum class has a class method called `by_value()`, then this
      dropdown widget will know how to get back to the enum by the text that
      is displayed.
    * In that case, if the Enum class also has a method called
      `color()`, then that method will be called to set the background
      color of the choice (which is merely a Button). `color()` needs to
      return an RGB 3-tuple or an RGBA 4-tuple of ints (0-255).

    :example: (in the `.kv` file)
        EnumDropDown:
            enum_class_name: "models.member_attributes.MemberRank"
            height_per: 33
            id: _rank
            on_text: root.validate_member_rank()

    :property enum_class_name: The class name of the enum that provides the
        possible values.

    :property height_per: How high (px) to make each choice. Default is 40.
    """
    enum_class_name = StringProperty("")
    height_per = NumericProperty(DEFAULT_DROPDOWN_SELECTION_HEIGHT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option_cls = DropDownChoice

    def on_kv_post(self, base_widget):
        self.enum_class: Enum = class_from_name(self.enum_class_name)
        self.values = [e.display_name() for e in self.enum_class]
        if self.values:
            self.configure_each_choice()
            if hasattr(self.enum_class, 'default'):
                self.text = self.enum_class.default().display_name()
            else:
                self.text = self.values[0]
        super().on_kv_post(base_widget)

    def configure_each_choice(self):
        container = self._dropdown.children[0]
        # LOG.debug("container = {}".format(container))
        for choice in container.children:
            # LOG.debug("choice = {}".format(choice))
            choice.configure(parent=self)

    def on_text(self, *args):
        colorize_widget_per_enum(self, self.enum_class)


def colorize_widget_per_enum(widget, enum_class):
    """
    Colorizes a particular dropdown choice widget (usually a Button) according
    to the definition of the enum. Specifically, if the enum has a color()
    method, that will be used. Alternatively, if the enum has a secondary_values()
    method, and if secondary_values() returns a tuple that appears to describe
    a color, then that is used. Otherwise, nothing changes.

    :param widget: The dropdown choice widget (e.g a button that is the child
        of a spinner).

    :param enum_class: The ennum class that is associated with the dropdown
        (i.e. how the text of the widget was determined).
    """
    if not (e := enum_by_value(enum_class, widget.text)):
        return

    widget.background_normal = ''
    # TODO move this into an abstract function(?)
    if hasattr(enum_class, "color"):
        int_color = e.color()
    elif hasattr(enum_class, "secondary_values"):
        int_color = e.secondary_values()
    else:
        return
    if is_color(int_color):
        widget.background_color = float_tuple(int_color)
        widget.color = float_tuple(color_outline(int_color))
