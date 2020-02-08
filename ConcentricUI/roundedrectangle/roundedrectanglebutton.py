""" Some notes go here """

all__ = ('RoundedRectangleButton',)

from concentricui.behaviours.concentricbutton import ConcentricButton
from concentricui.roundedrectangle.concentricroundedrectangles import ConcentricRoundedRectangles


class RoundedRectangleButton(ConcentricRoundedRectangles, ConcentricButton):

    def __init__(self, **kwargs):
        super(RoundedRectangleButton, self).__init__(**kwargs)
