""" Some notes go here """

all__ = ('ColourScreen',)

from kivy.core.window import Window

from functools import partial

from kivy.clock import Clock

from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.screenmanager import Screen

from ConcentricUI.colourscheme.colourwidget import ColourWidget
from ConcentricUI.behaviours.concentricfontscaling import ConcentricFontScaling
from ConcentricUI.behaviours.concentrictextinput import ConcentricTextInput

class ColourScreen(Screen, ColourWidget):

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
            self.background_rectangle = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.set_size, background_colour=self.set_background_colour)

    # def add_widget(self, widget, index=0, canvas=None):
    #     widget.background_colour = self.background_colour
    #     widget.foreground_colour = self.foreground_colour
    #     super(ColourScreen, self).add_widget(widget, index, canvas)

    def set_size(self, wid, size, *args):
        self.background_rectangle.size = self.size

    def set_background_colour(self, wid, background_colour):
        self.background_rectangle_colour_instruction.rgba = background_colour

    def on_enter(self, *args):
        for widget in self.walk():
            if issubclass(widget.__class__, ConcentricFontScaling):
                widget.set_font_size()

        super(ColourScreen, self).on_enter(*args)
