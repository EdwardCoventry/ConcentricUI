all__ = ('TopBar',)

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

from ConcentricUI.appcontroll.appcontroll import minimise_app, close_app
from ConcentricUI.oblong.concentricoblongs import ConcentricOblongs
from ConcentricUI.widgets.screenchangespinner import ScreenChangeSpinner
from ConcentricUI.widgets.textbutton import TextButton


class TopBarShape(ConcentricOblongs):

    def __init__(self, **kwargs):
        self.rectangle_colour_instruction = None

        self.shape_size_hint_list = [1]
        #self.allow_concentric = False  #  fixme allow concentric shades to the lightest colour..


        super(TopBarShape, self).__init__(**kwargs)


        self.pos_hint = {}

        with self.canvas:
            self.rectangle_colour_instruction = Color(*self.trim_colour)
            self.rectangle = Rectangle()

        self.bind(size=self.set_rectangle_size, pos=self.set_rectangle_pos, trim_colour=self.set_rectangle_colour)

    def set_rectangle_size(self, wid, size):
        self.rectangle.size = size[0], size[1] / 2
        self.set_rectangle_pos(wid, self.pos)

    def set_rectangle_pos(self, wid, pos):
        self.rectangle.pos = pos[0], pos[1] + self.size[1] / 2

    def set_rectangle_colour(self, wid, colour):
        if self.rectangle_colour_instruction:
            self.rectangle_colour_instruction.rgba = colour