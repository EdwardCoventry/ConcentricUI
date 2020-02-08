""" Some notes go here """

all__ = ('ColourScreen',)

from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.screenmanager import Screen

from concentricui.colourscheme.colourwidget import ColourWidget
from concentricui.widgets.topbar import TopBar


class ColourScreen(Screen, ColourWidget):
    top_bar_size_hint = NumericProperty(0.04)
    top_bar_y = NumericProperty()
    screen_height = NumericProperty()
    screen_width = NumericProperty()
    screen_size = ReferenceListProperty(screen_width, screen_height)

    def add_widget(self, widget, index=0, canvas=None):
        widget.top = self.top_bar_y
        super(ColourScreen, self).add_widget(widget, index, canvas)

    def __init__(self, **kwargs):
        self.colour_scheme = 'app'

        super(ColourScreen, self).__init__(**kwargs)
        self.background_color = None
        self.background_normal = None
        self.background_down = None
        self.background_disabled_normal = None
        self.background_disabled_down = None

        with self.canvas:
            self.background_rectangle_colour_instruction = Color(*self.background_colour)
            self.background_rectangle = Rectangle()

        self.top_bar = TopBar(shape_size_hint_list=[1], colour_scheme=self.colour_scheme, master_colour='trim_colour',
                              top=self.top, size_hint_y=None)
        self.add_widget(self.top_bar)

        # self.test_button = Button(opacity=0.4)

        # self.add_widget(self.test_button)

        self.bind(size=self.set_size, background_colour=self.set_background_colour)

    def set_size(self, wid, size):
        self.top_bar.height = size[1] * self.top_bar_size_hint
        # self.top_bar.size_hint_y = 0.04
        self.top_bar_y = self.top_bar.y
        self.top_bar.top = self.top

        self.screen_height = self.top_bar_y

        self.background_rectangle.size = size

        # self.test_button.size = self.screen_size

    #
    # def add_widget(self, widget, index=0, canvas=None):
    #     super(self.add_widget(widget, index, canvas))

    def set_background_colour(self, wid, background_colour):
        self.background_rectangle_colour_instruction.rgba = self.background_colour
