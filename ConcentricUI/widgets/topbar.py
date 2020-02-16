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

        self.bluetooth_button = TextButton(text='-')
        self.home_button = TextButton(text='Home', on_release=self.take_me_home)
        self.settings_button = TextButton(text='Settings', on_release=self.open_settings)
        box_layout.add_widget(self.bluetooth_button)
        box_layout.add_widget(self.home_button)
        box_layout.add_widget(self.settings_button)

        self.content_pin = box_layout

    def take_me_home(self, wid):
        print('wid', wid)
        App.get_running_app().root.current = 'Home Screen'

    # def pass_master_colour_to_children(self, wid, colour):
    #     if self.screen_change_spinner:
    #         self.screen_change_spinner.master_colour = self.master_colour
    #     self.set_rectangle_colour(wid, colour)

    def open_settings(self, *args):
        App.get_running_app().open_settings()
