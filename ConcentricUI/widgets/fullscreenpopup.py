""" Some notes go here """

all__ = ('FullScreenPopup',)

from ConcentricUI.widgets.popup import ConcentricPopup


class FullScreenPopup(ConcentricPopup):

    def __init__(self, **kwargs):
        # self.colour_scheme = 'app'

        super(FullScreenPopup, self).__init__(**kwargs)