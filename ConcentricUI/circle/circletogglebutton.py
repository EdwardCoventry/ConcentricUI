""" Some notes go here """

all__ = ('CircleToggleButton',)

from ConcentricUI.behaviours.concentrictogglebutton import ConcentricToggleButton
from ConcentricUI.circle.concentriccircles import ConcentricCircles


class CircleToggleButton(ConcentricCircles, ConcentricToggleButton):

    def __init__(self, **kwargs):
        super(CircleToggleButton, self).__init__(**kwargs)

    #def on_state(self, wid, args):