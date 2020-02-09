""" Some notes go here """

all__ = ('CircleTextInput',)

from ConcentricUI.behaviours.concentrictextinput import ConcentricTextInput
from ConcentricUI.circle.concentriccircles import ConcentricCircles


class CircleTextInput(ConcentricTextInput, ConcentricCircles):

    def __init__(self, **kwargs):
        super(CircleTextInput, self).__init__(**kwargs)
