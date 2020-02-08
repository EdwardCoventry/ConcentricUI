from math import sqrt

from kivy.graphics import RoundedRectangle
from kivy.properties import NumericProperty

""" I have removed all of my AliasProperties as it seems that the base class Ellipse cannot use the event dispatcher """


class RoundedRec(RoundedRectangle):
    center_x = NumericProperty()
    center_y = NumericProperty()

    def set_center_x(self, value):
        self.pos = value - self.size[0] / 2., self.pos[1]

    def set_center_y(self, value):
        self.pos = self.pos[0], value - self.size[1] / 2.

    def set_center(self, center):
        center_x, center_y = center
        self.set_center_x(center_x)
        self.set_center_y(center_y)

    def set_size(self, widget_size, size_hint):

        width, height = widget_size

        border_horizontal = width * (1 - size_hint)
        border_vertical = height * (1 - size_hint)

        border = min(border_horizontal, border_vertical)

        #  fixme if needed you could pretty easily make have an option for max_border
        # self.size = width - border, height - border
        self.size = width - border, height - border

    def to_inner_center(self, x, y):
        local_x, local_y = x - self.pos[0], y - self.pos[1]
        from_center_x, from_center_y = local_x - self.size[0] / 2, local_y - self.size[1] / 2
        # factor_in_rectangle = from_center_x + self.rectangle_width/2, from_center_y + self.rectangle_height
        return from_center_x, from_center_y

    def get_inner_y_at_x(self, x, scale_bounds=False):

        """ for now this will onlx work if all radii are the same"""

        width, height = self.size
        radius = self.radius[0][1]

        if scale_bounds:
            width *= scale_bounds
            height *= scale_bounds
            radius *= scale_bounds

        if abs(x) > width / 2:
            return None

        vertical_without_corner = height / 2

        if - width / 2 + radius < x < width / 2 - radius:
            #  not in range of a corner, just in the central rectangle area
            return vertical_without_corner
        else:

            #  this statement is to actually remove the height of the corner
            #  think about it: at the very sides of the circles, you take off the entire radius
            corner_x = abs(x) - width / 2 + radius
            corner = radius - sqrt(abs(corner_x ** 2 - abs(radius) ** 2))
            return vertical_without_corner - corner

    def get_inner_x_at_y(self, y, scale_bounds=False):

        """ for now this will only work if all radii are the same"""

        width, height = self.size
        radius = self.radius[0][0]

        if scale_bounds:
            width *= scale_bounds
            height *= scale_bounds
            radius *= scale_bounds

        if abs(y) > height / 2:
            return None

        horizontal_without_corner = width / 2

        if - height / 2 + radius < y < height / 2 - radius:
            #  not in range of a corner, just in the central rectangle area
            return horizontal_without_corner
        else:

            #  this statement is to actually remove the width of the corner
            #  think about it: at the very bottom of the circles, you take off the entire radius from the width
            corner_y = abs(y) - height / 2 + radius
            corner = radius - sqrt(abs(corner_y ** 2 - abs(radius) ** 2))
            return horizontal_without_corner - corner
