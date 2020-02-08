""" Some notes go here """

all__ = ('OblongToggleButton',)

from concentricui.behaviours.concentrictogglebutton import ConcentricToggleButton
from concentricui.oblong.concentricoblongs import ConcentricOblongs


class OblongToggleButton(ConcentricOblongs, ConcentricToggleButton):

    def __init__(self, **kwargs):
        super(OblongToggleButton, self).__init__(**kwargs)
