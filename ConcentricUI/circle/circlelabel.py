""" Some notes go here """

all__ = ('CircleLabel',)

from ConcentricUI.behaviours.concentriclabel import ConcentricLabel
from ConcentricUI.circle.concentriccircles import ConcentricCircles

class CircleLabel(ConcentricCircles, ConcentricLabel):

    def __init__(self, **kwargs):
        super(CircleLabel, self).__init__(**kwargs)

    # def on_size(self, wid, size):
