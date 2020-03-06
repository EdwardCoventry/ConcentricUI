""" Some notes go here """

all__ = ('ConcentricPopup', 'RoundedRectangleConcentricPopup')

from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from ConcentricUI.colourscheme.colourwidget import ColourWidget
from ConcentricUI.roundedrectangle.concentricroundedrectangles import ConcentricRoundedRectangles
from ConcentricUI.widgets.textbutton import TextButton
from ConcentricUI.widgets.topbar import TopBarShape


# <NiceConcentricPopup>:
#
#     background_color: app.background_colour
#     background: ''
#     border: app.trim_colour
#     text_colour: app.foreground_colour
#     #separator_height: 0
#     content: use_as_contents
#     top_bar: top_bar
#
#     BoxLayout:
#         orientation: 'vertical'
#         TopBarShape:
#             id: top_bar
#             height: root.height*0.04
#             width: root.width
#
#             Button:
#                 pos: top_bar.pos
#                 size: top_bar.size
#                 text_size: self.width/3, self.height
#                 font_size: self.height*0.6
#                 #size_hint_x: 1/3
#                 halign: 'center'
#                 valign: 'center'
#                 text: 'close'
#                 color: root.text_colour
#
#                 on_release:
#                     root.save_and_close()
#
#
#         BoxLayout:
#             orientation: 'vertical'
#             id: use_as_contents


class ConcentricPopup(ModalView, ColourWidget):
    content = ObjectProperty()
    top_bar = ObjectProperty()

    background_rectangle = ObjectProperty()

    def __init__(self, **kwargs):
        # self.colour_scheme = 'app'

        # self.separator_color = [0, 0, 0, 0]
        # self.separator_height = 0

        super(ConcentricPopup, self).__init__(**kwargs)

        self.anchor_y = 'top'

        #
        self.background = "textures/blank.png"
        #self.background_color = App.get_running_app.background_colour
        #
        # self.background_colour = (1,0,1,1)
        with self.canvas.before:
            self.background_rectangle_colour_instruction = Color(*self.background_colour)
            self.background_rectangle = Rectangle()

        popup_boxlayout = BoxLayout(orientation='vertical')

        #
        self.top_bar = TopBarShape(id='top_bar',
                                   colour_scheme='app',
                                   show_trim=True,
                                   allow_concentric=False,
                                   size_hint_y=0.04,
                                   pos_hint={'top': 1})

        save_and_close_button = TextButton(text='Close', pos=self.top_bar.pos, size=self.top_bar.size)
        save_and_close_button.bind(on_release=self.save_and_close)
        self.top_bar.content_pin = save_and_close_button

        self.add_widget(popup_boxlayout)
        popup_boxlayout.add_widget(self.top_bar)
        #
        boxlayout = BoxLayout(orientation='vertical', top=self.top_bar.y, size_hint_y=(1 - self.top_bar.size_hint_y))
        popup_boxlayout.add_widget(boxlayout)
        self.content = boxlayout

    def on_background_colour(self, wid, colour):
        self.background_rectangle_colour_instruction.rgba = colour

    def on_size(self, wid, size):
        if self.background_rectangle:
            self.background_rectangle.size = size

        # self.background_rectangle_colour_instruction.rgba = self.background_colour

        # if self.top_bar:
        #     self.top_bar.size = self.height * 0.04, self.width

    # def on_pos(self, wid, pos):
    #     if self.top_bar:
    #         self.top_bar.top = self.top
    #

    def save_and_close(self, *args):

        """ save code goes here """
        self.dismiss()


class RoundedRectangleConcentricPopup(ConcentricPopup, ConcentricRoundedRectangles):

    def __init__(self, **kwargs):
        super(RoundedRectangleConcentricPopup, self).__init__(**kwargs)
