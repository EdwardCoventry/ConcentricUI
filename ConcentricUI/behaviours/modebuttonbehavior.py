""" Some notes go here """

all__ = ('ModeButtonBehavior',)

from kivy.uix.widget import Widget
from kivy.properties import StringProperty

class ModeButtonBehavior(Widget):

    state_list_index = 0
    button_state = StringProperty()

    @staticmethod
    def get_button_state(clss):
        #  fixme i should make the function generate with the class already added
        index = clss.state_list_index
        return clss.state_list[index]

    @staticmethod
    def get_button_state_list_index(clss):
        #  fixme i should make the function generate with the class already added
        index = clss.state_list_index
        return index

    def __init__(self, **kwargs):
        super(ModeButtonBehavior, self).__init__(**kwargs)
        self.set_button()

    def set_button(self, state=None, *args):

        if state:
            index = self.state_list.index(state)
            self.__class__.state_list_index = index
        else:
            index = self.__class__.state_list_index

        self.button_state = self.state_list[index]
        self.button_colour = self.colour_list[index]
        self.button_image = self.image_list[index]

    def increment_class_index(self, *args):
        #  use class variable
        self.__class__.state_list_index += 1
        if self.__class__.state_list_index == len(self.state_list):
            self.__class__.state_list_index = 0
        self.set_button()

    def on_release(self, *args):
        self.increment_class_index()