""" Some notes go here """

all__ = ('OblongButton',)

from concentricui.behaviours.concentricbutton import ConcentricButton
from concentricui.oblong.concentricoblongs import ConcentricOblongs


class OblongButton(ConcentricOblongs, ConcentricButton):

    def __init__(self, **kwargs):
        super(OblongButton, self).__init__(**kwargs)
