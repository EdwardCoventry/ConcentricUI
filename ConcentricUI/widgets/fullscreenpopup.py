""" Some notes go here """

all__ = ('FullScreenPopup',)

from kivy.app import App

from kivy.graphics import Color, Rectangle
from ConcentricUI.widgets.popup import ConcentricPopup


class FullScreenPopup(ConcentricPopup):

    def __init__(self, **kwargs):
        # self.colour_scheme = 'app'

        super(FullScreenPopup, self).__init__(**kwargs)

    #     print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', self.background_colour)
    #
    #     with self.canvas.before:
    #         self.background_rectangle_colour_instruction = Color(*App.get_running_app().background_colour)
    #         self.background_rectangle = Rectangle(size=self.size, pos=self.pos)
    #
    #     self.bind(size=self.set_size, background_colour=self.set_background_colour)
    #
    #
    # def set_size(self, wid, size, *args):
    #     self.background_rectangle.size = self.size
    #
    # def set_background_colour(self, wid, background_colour):
    #     self.background_rectangle_colour_instruction.rgba = background_colour
