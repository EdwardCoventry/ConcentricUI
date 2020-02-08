""" Some notes go here """

all__ = ('ConcentricRoundedRectangles',)

from concentricui.behaviours.concentricshapes import ConcentricShapes
from concentricui.roundedrectangle.roundedrectangle import RoundedRec


class ConcentricRoundedRectangles(ConcentricShapes):
    draw_shape_toggle = True

    def draw_shape(self, shape_size_hint, shape_colour, **kwargs):
        """ overwrite this function for circle, oblong, rounded rectangle """
        # shape_size = shape_size_hint * self.width, shape_size_hint * self.height
        # Color(*shape_colour)
        shape = RoundedRec()
        # shape = RoundedRectangle(center=self.center, size=shape_size)
        return shape
