""" Some notes go here """

all__ = ('CircleButton',)

from ConcentricUI.behaviours.concentricbutton import ConcentricButton
from ConcentricUI.circle.concentriccircles import ConcentricCircles


class CircleButton(ConcentricCircles, ConcentricButton):

    def __init__(self, **kwargs):
        super(CircleButton, self).__init__(**kwargs)
