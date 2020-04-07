from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior

from ConcentricUI.colourscheme.colourwidget import ColourWidget
from ConcentricUI.behaviours.concentricshapes import ConcentricShapes


class Text(ColourWidget, Label):
    font_ratio = NumericProperty(0.7)

    def __init__(self, **kwargs):
        super(Text, self).__init__(**kwargs)

        self.halign = 'center'
        self.valign = 'center'

        self.colour_scheme = 'app'
        self.set_colour(self, self.text_colour)
        self.bind(size=self.set_size, text_colour=self.set_colour)

    def set_size(self, wid, size):
        self.text_size = size
        self.font_size = size[1] * self.font_ratio
        #super(Text, self).set_size(wid, size)

    def set_colour(self, wid, colour):
        self.color = colour

    def set_text(self, text, *args):
        self.text = text

class TextButton(Text, Button):

    def __init__(self, **kwargs):
        super(TextButton, self).__init__(**kwargs)

        self.background_color = [0, 0, 0, 0]
        self.background_normal = ''
        self.background_down = ''
        self.background_disabled_normal = ''
        self.background_disabled_down = ''

class TextToggleButton(TextButton, ToggleButtonBehavior):

    def __init__(self, **kwargs):
        super(TextToggleButton, self).__init__(**kwargs)
