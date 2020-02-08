""" Some notes go here """

all__ = ('ScreenChangeSpinner',)

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty

from concentricui.oblong.oblongspinner import OblongSpinner


class ScreenChangeSpinner(OblongSpinner):
    screen_names_list = ListProperty()
    text_autoupdate = True

    allow_concentric = False

    #  this is so i can keep a reference to all the screen change spinner instances in the class itself,
    #  so that they can all be updated if one is
    screen_change_spinner_instance_list = []

    def __init__(self, **kwargs):
        super(ScreenChangeSpinner, self).__init__(**kwargs)

        Clock.schedule_once(self.get_screen_names)

        self.__class__.screen_change_spinner_instance_list.append(self)

    def get_screen_names(self, *args):
        self.values = App.get_running_app().root.screen_names

    def _on_dropdown_select(self, instance, data, *largs):
        self.is_open = False

        for spinner in self.__class__.screen_change_spinner_instance_list:
            spinner.text = data

        #  here it changes the display screen
        App.get_running_app().root.current = data
