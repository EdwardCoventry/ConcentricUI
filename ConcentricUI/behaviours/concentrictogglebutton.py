""" Some notes go here """

all__ = ('ConcentricToggleButton',)

from kivy.uix.togglebutton import ToggleButtonBehavior

from concentricui.behaviours.concentricbutton import ConcentricButton


class ConcentricToggleButton(ConcentricButton, ToggleButtonBehavior):

    def __init__(self, **kwargs):
        super(ConcentricButton, self).__init__(**kwargs)

    def invert_state(self, *args):
        self.state = 'down' if self.state == 'normal' else 'normal'

    def set_state_down(self, *args):
        self.state = 'down'

    def set_state_normal(self, *args):
        self.state = 'normal'
