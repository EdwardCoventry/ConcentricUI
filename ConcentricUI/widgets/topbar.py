all__ = ('TopBar',)

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

from concentricui.appcontroll.appcontroll import minimise_app, close_app
from concentricui.oblong.concentricoblongs import ConcentricOblongs
from concentricui.widgets.screenchangespinner import ScreenChangeSpinner
from concentricui.widgets.textbutton import TextButton


class TopBarShape(ConcentricOblongs):

    def __init__(self, **kwargs):
        self.rectangle_colour_instruction = None
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


class TopBar(TopBarShape):

    def __init__(self, **kwargs):
        self.screen_change_spinner = None
        super(TopBar, self).__init__(**kwargs)

        self.allow_concentric = False
        # self.colour_scheme = 'screen'

        box_layout = BoxLayout(size=self.size,
                               orientation='horizontal')
        #  close and minimise buttons
        window_buttons_box = BoxLayout(orientation='horizontal')
        close_button = TextButton(text='x',
                                  on_release=close_app,
                                  master_colour='text_colour')
        minimise_button = TextButton(text='-',
                                     on_release=minimise_app,
                                     master_colour='text_colour')
        window_buttons_box.add_widget(close_button)
        window_buttons_box.add_widget(minimise_button)

        box_layout.add_widget(window_buttons_box)

        #  screen change spinner
        self.screen_change_spinner = ScreenChangeSpinner(shape_size_hint_list=[0.9, 1],
                                                         colour_scheme=self.colour_scheme,
                                                         master_colour=self.master_colour, sync_height=100,
                                                         font_ratio=0.7,
                                                         option_cls_kwargs={'shape_size_hint_list': [0.8, 1]})
        box_layout.add_widget(self.screen_change_spinner)

        #
        self.settings_button = TextButton(text='Settings', on_release=self.open_settings)
        box_layout.add_widget(self.settings_button)

        self.content_pin = box_layout

    def pass_master_colour_to_children(self, wid, colour):
        if self.screen_change_spinner:
            self.screen_change_spinner.master_colour = self.master_colour
        self.set_rectangle_colour(wid, colour)

    def open_settings(self, *args):
        App.get_running_app().open_settings()
