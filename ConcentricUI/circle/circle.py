from math import sqrt

from kivy.graphics import Ellipse
from kivy.properties import NumericProperty, ReferenceListProperty

""" I have removed all of my AliasProperties as it seems that the base class Ellipse cannot use the event dispatcher """


class Circle(Ellipse):

    # def get_diameter(self):
    #     """ This occurs when you want to get the diameter """
    #     return min(self.size)
    #
    # def set_diameter(self, value):
    #     """ I'm not too sure what would happen if the diameter was set..
    #         but i suppose that it would change the size
    #         meaning that the widget would only take up the size of the circle itself.
    #         To be seen. """
    #     self.size = value, value
    #
    # diameter = AliasProperty(get_diameter, set_diameter, bind=['size'])

    def get_center_x(self):
        return self.x + self.size[0] / 2.

    def set_center_x(self, value):
        pass
        #self.pos = value + self.size[0] / 2., self.pos[1]
        self.pos = value - self.size[0] / 2., self.pos[1]

    # center_x = AliasProperty(get_center_x, set_center_x, bind=('x', 'width'))
    center_x = NumericProperty()

    def get_center_y(self):
        """ So useful! """
        return self.pos[1] + self.diameter / 2

    def set_center_y(self, value):

        """ Can't believe this wasn't already implemented! """
        self.pos = self.pos[0], value - self.size[1] / 2.
        #self.pos = self.pos[0], value - (self.size[1]/2. - value/2.)


    # center_y = AliasProperty(get_center_y, set_center_y, bind=['size', 'pos'])
    center_y = NumericProperty()

    center = ReferenceListProperty(center_x, center_y)

    def set_center(self, center):
        center_x, center_y = center
        self.set_center_x(center_x)
        self.set_center_y(center_y)

    def set_size(self, widget_size, size_hint):
        diameter = min(widget_size)
        self.size = diameter * size_hint, diameter * size_hint

    def __init__(self, **kwargs):
        super(Circle, self).__init__(**kwargs)

    def to_inner_center(self, x, y):
        local_x, local_y = x - self.pos[0], y - self.pos[1]
        from_center_pos = local_x - self.size[0] / 2, local_y - self.size[1] / 2
        return from_center_pos

    def get_inner_x_at_y(self, y, scale_bounds=False):

        radius = min(self.size) / 2

        if scale_bounds:
            radius *= scale_bounds

        # if scale_bounds:
        #     y /= radius

        if abs(y) > radius:
            return None

        x = sqrt(abs(radius ** 2 - y ** 2))
        return x

    def get_inner_y_at_x(self, x, scale_bounds=False):

        radius = min(self.size) / 2

        if scale_bounds:
            radius *= scale_bounds

        if abs(x) > radius:
            return None

        y = sqrt(abs(radius ** 2 - x ** 2))
        return y
