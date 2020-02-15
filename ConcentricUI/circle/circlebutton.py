""" Some notes go here """

all__ = ('CircleButton',)

from ConcentricUI.behaviours.concentricbutton import ConcentricButton
from ConcentricUI.circle.concentriccircles import ConcentricCircles

from kivy.clock import Clock

class CircleButton(ConcentricCircles, ConcentricButton):

    def __init__(self, **kwargs):
        super(CircleButton, self).__init__(**kwargs)