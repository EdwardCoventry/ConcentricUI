""" Some notes go here """

all__ = ('ConcentricShapes',)

from concentricui.behaviours.concentricshapes import ConcentricShapes
from concentricui.circle.circle import Circle


class ConcentricCircles(ConcentricShapes):
    draw_shape_toggle = True

    def draw_shape(self, shape_size_hint, shape_colour, image_source=None, **kwargs):
        """ overwrite this function for circle, oblong, rounded rectangle """

        if image_source:
            shape = Circle(source="textures/buttons/cross_button.png")
            # shape = Circle(center=self.center, size=(d, d))
        else:
            shape = Circle()
        return shape
