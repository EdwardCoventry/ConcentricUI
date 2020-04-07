from kivy.properties import BooleanProperty, NumericProperty, ReferenceListProperty, StringProperty
from kivy.uix.label import Label

from ConcentricUI.behaviours.concentricfontscaling import ConcentricFontScaling


class ConcentricLabel(Label, ConcentricFontScaling):
    scale_text = BooleanProperty(True)
    inner_width, inner_height = NumericProperty(), NumericProperty()
    inner_size = ReferenceListProperty(inner_width, inner_height)

    text = StringProperty(allownone=True)

    def update(self, *args):
        try:
            self.texture_update()
        except:
            pass
            #print('this will come back to bite me')
            #fixme

    def __init__(self, **kwargs):
        super(ConcentricLabel, self).__init__(**kwargs)

        self.color = self.text_colour
        self.bind(text_colour=self.set_colour)

    def set_colour(self, wid, colour):
        self.color = self.text_colour
