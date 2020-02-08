""" Some notes go here """

all__ = ('OblongTextInput',)

from concentricui.behaviours.concentrictextinput import ConcentricTextInput
from concentricui.oblong.concentricoblongs import ConcentricOblongs


class OblongTextInput(ConcentricOblongs, ConcentricTextInput):

    def __init__(self, **kwargs):
        super(OblongTextInput, self).__init__(**kwargs)

    # def update_padding(self, *args):
    #
    #     if not self.text:
    #         self.padding = self.width/2, self.center_y/2
    #         return
    #
    #     text_width = self._get_text_width(
    #         self.text,
    #         self.tab_width,
    #         self._label_cached
    #     )
    #
    #     padding_y = self.center_y/2
    #     inner_width = self.get_inner_width_at_y(self.center_y + self.font_size/2)
    #
    #     padding_x_when_text_box_not_filled = (self.width - text_width) / 2
    #     padding_x_when_text_box_is_filled = (self.width - inner_width) / 2
    #     padding_x = max(abs(padding_x_when_text_box_not_filled), abs(padding_x_when_text_box_is_filled))
    #
    #     self.padding = padding_x, padding_y
