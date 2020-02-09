""" Some notes go here """

all__ = ('OblongLabel',)

from ConcentricUI.behaviours.concentriclabel import ConcentricLabel
from ConcentricUI.oblong.concentricoblongs import ConcentricOblongs


class OblongLabel(ConcentricOblongs, ConcentricLabel):

    def __init__(self, **kwargs):
        super(OblongLabel, self).__init__(**kwargs)
