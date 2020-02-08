""" Some notes go here """

all__ = ('CircleToggleButton',)

from concentricui.behaviours.concentrictogglebutton import ConcentricToggleButton
from concentricui.circle.concentriccircles import ConcentricCircles


class CircleToggleButton(ConcentricCircles, ConcentricToggleButton):

    def __init__(self, **kwargs):
        super(CircleToggleButton, self).__init__(**kwargs)
