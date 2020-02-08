""" Some notes go here """

all__ = ('CircleButton',)

from concentricui.behaviours.concentricbutton import ConcentricButton
from concentricui.circle.concentriccircles import ConcentricCircles


class CircleButton(ConcentricCircles, ConcentricButton):

    def __init__(self, **kwargs):
        super(CircleButton, self).__init__(**kwargs)
