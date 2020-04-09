""" Some notes go here """

all__ = ('RoundedRectangleLabel',)

from ConcentricUI.behaviours.concentriclabel import ConcentricLabel
from ConcentricUI.roundedrectangle.concentricroundedrectangles import ConcentricRoundedRectangles


class RoundedRectangleLabel(ConcentricRoundedRectangles, ConcentricLabel):

    def __init__(self, **kwargs):
        super(RoundedRectangleLabel, self).__init__(**kwargs)