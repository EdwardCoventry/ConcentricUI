""" Some notes go here """

all__ = ('OblongButton',)

from ConcentricUI.behaviours.concentricbutton import ConcentricButton
from ConcentricUI.oblong.concentricoblongs import ConcentricOblongs


class OblongButton(ConcentricOblongs, ConcentricButton):

    def __init__(self, **kwargs):
        super(OblongButton, self).__init__(**kwargs)
