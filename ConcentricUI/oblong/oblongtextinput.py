""" Some notes go here """

all__ = ('OblongTextInput',)

from concentricui.behaviours.concentrictextinput import ConcentricTextInput
from concentricui.oblong.concentricoblongs import ConcentricOblongs


class OblongTextInput(ConcentricOblongs, ConcentricTextInput):

    # colour_instruction_list = ObjectProperty()

    # def on_text(self, wid, text):
    #
    #     print('testsettsttsxzxt', text)
    #     self.font_size = self.inner_height

    def __init__(self, **kwargs):
        super(OblongTextInput, self).__init__(**kwargs)

        # self.add_widget(ConcentricTextInput(**kwargs))
        # self.text_input = ConcentricTextInput(draw_shape_toggle=False)
        # self.content_pin = ConcentricTextInput(do_padding='test')

        # self.colour_instruction_list = self.content_pin.colour_instruction_list

        # self.bind(size=self.set_text_input_size)
        # self.bind(pos=self.set_text_input_pos)

        # self.bind(inner_size=self.set_text_input_inner_dimensions)

        # self.text_input.bind(text=self.set_text_input_size)
        # self.text_input.bind(text=self.set_text_input_pos)

    # def set_text_input_size(self, wid, size):
    #
    #     if self.orientation == 'horizontal':
    #         left = self.opening_pin.right if self.opening_pin else self.inner_x
    #         right = self.closing_pin.x if self.closing_pin else self.inner_right
    #
    #         print('innnniiiiii', self.inner_x)
    #
    #         width = right - left
    #         height = self.height
    #
    #     if self.orientation == 'vertical':
    #         bottom = self.opening_pin.top if self.opening_pin else self.inner_y
    #         top = self.closing_pin.y if self.closing_pin else self.inner_top
    #
    #         height = top - bottom
    #         width = self.inner_width
    #
    #     self.text_input.size = width, height
    #
    # def set_text_input_pos(self, wid, pos):
    #
    #     if self.orientation == 'horizontal':
    #         left = self.opening_pin.right if self.opening_pin else self.inner_x
    #         x = left + self.text_input.width/2
    #         y = self.center_y
    #
    #     if self.orientation == 'vertical':
    #         bottom = self.opening_pin.top if self.opening_pin else self.inner_y
    #         y = bottom + self.text_input.height/2
    #         x = self.center_x
    #
    #     self.text_input.center = x, y
