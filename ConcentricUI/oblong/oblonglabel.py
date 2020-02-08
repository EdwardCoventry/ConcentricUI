""" Some notes go here """

all__ = ('OblongLabel',)

from concentricui.behaviours.concentriclabel import ConcentricLabel
from concentricui.oblong.concentricoblongs import ConcentricOblongs


class OblongLabel(ConcentricOblongs, ConcentricLabel):

    def __init__(self, **kwargs):
        super(OblongLabel, self).__init__(**kwargs)
