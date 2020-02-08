""" Some notes go here """

all__ = ('RoundedRectangleDropdown',)

from kivy.uix.dropdown import DropDown

from concentricui.roundedrectangle.concentricroundedrectangles import ConcentricRoundedRectangles


class RoundedRectangleDropdown(ConcentricRoundedRectangles, DropDown):

    def __init__(self, **kwargs):
        super(RoundedRectangleDropdown, self).__init__(**kwargs)
