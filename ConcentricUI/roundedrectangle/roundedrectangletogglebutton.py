""" Some notes go here """

all__ = ('RoundedRectangleToggleButton',)

from ConcentricUI.behaviours.concentrictogglebutton import ConcentricToggleButton
from ConcentricUI.roundedrectangle.concentricroundedrectangles import ConcentricRoundedRectangles


class RoundedRectangleToggleButton(ConcentricRoundedRectangles, ConcentricToggleButton):

    def __init__(self, **kwargs):
        super(RoundedRectangleToggleButton, self).__init__(**kwargs)
