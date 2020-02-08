from math import sqrt

from kivy.graphics import InstructionGroup, VertexInstruction, Rectangle
from kivy.properties import AliasProperty

from concentricui.circle.circle import Circle

""" I have removed all of my AliasProperties as it seems that the base class Ellipse cannot use the event dispatcher """


class OblongInstructions(InstructionGroup):

    def __init__(self, **kwargs):
        super(OblongInstructions, self).__init__(**kwargs)


class Oblong(VertexInstruction):
    center_x = None
    center_y = None
    center = AliasProperty(center_x, center_y)

    #  circle diameters are the diameters of the semicircles at the end of the rectangle
    circle_diameters = 0

    # pos = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    pos = 0, 0
    """Property for getting/settings the position of the rectangle.
        """

    # size = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    size = 100, 100
    """Property for getting/settings the size of the rectangle.
        """

    # orientation = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    orientation = 'horizontal'
    """Property for getting/settings the size of the rectangle.
        """

    min_size_hint = None

    def __init__(self, size=(100, 100), size_hint=1, pos=(0, 0), orientation='horizontal', center=None,
                 min_size_hint=None, max_size_hint=None):  # real signature unknown

        self.orientation = orientation

        self.size_hint = size_hint
        self.min_size_hint = min_size_hint
        self.max_size_hint = max_size_hint

        #  define rectangle
        self.rectangle_size = None
        rectangle_size = self.get_rectangle_size()
        #  draw rectangle
        self.rectangle = Rectangle(size=rectangle_size, pos=(0, 0))
        self.set_rectangle_size(rectangle_size)

        #  define semicircles
        if self.orientation == 'horizontal':
            opening_angle_start, opening_angle_end = 0, -180
            closing_angle_start, closing_angle_end = 0, 180
        else:
            #  self.orientation == 'vertical':
            opening_angle_start, opening_angle_end = -90, 90
            closing_angle_start, closing_angle_end = 90, 270

        #  draw semicircles
        self.opening_circle = Circle(angle_start=opening_angle_start, angle_end=opening_angle_end)
        self.closing_circle = Circle(angle_start=closing_angle_start, angle_end=closing_angle_end)

        #  set pos
        if center:
            self.set_center(center)
            self.center_x, self.center_y = self.center
        else:
            self.set_pos(pos)

        #  set size
        self.set_size(size)

        #  set pos (again)
        center = self.get_center()
        self.set_center(center)
        self.update_rectangle_center()

    def get_rectangle_width(self):
        if self.orientation == 'horizontal':

            rectangle_width = self.size[0] - self.size[1] / self.size_hint

            if rectangle_width < 0:
                #  ie if oblong is taller than it is wide. in this case you will just get a circle
                rectangle_width = 0
            rectangle_width = rectangle_width
        else:
            #  self.orientation == 'vertical':
            rectangle_width = self.circle_diameters
        return rectangle_width

    def get_rectangle_height(self):
        if self.orientation == 'horizontal':
            rectangle_height = self.circle_diameters
        else:
            #  self.orientation == 'vertical':
            # rectangle_height = self.size[1] - self.size[0] * (2-self.size_hint)
            rectangle_height = self.size[1] - self.size[0] - 2 * self.size[0] * (1 - self.size_hint)
            if rectangle_height < 0:
                #  ie if oblong is wider than it is tall. in this case you will just get a circle
                rectangle_height = 0
            rectangle_height = rectangle_height
        return rectangle_height

    def get_rectangle_size(self):
        rectangle_width = self.get_rectangle_width()
        rectangle_height = self.get_rectangle_height()
        rectangle_size = rectangle_width, rectangle_height

        return rectangle_size

    def set_rectangle_size(self, value=None):
        if not value:
            value = self.rectangle_size
        self.rectangle_size = value
        self.rectangle.size = value
        self.rectangle_width = value[0]
        self.rectangle_height = value[1]

    def update_rectangle_center(self):

        if self.orientation == 'horizontal':
            rectangle_x = self.opening_circle_center[0]
            rectangle_y = self.center_y - self.rectangle_height / 2

        else:
            #  if self.orientation == 'vertical'
            rectangle_x = self.center_x - self.rectangle_width / 2
            rectangle_y = self.closing_circle_center[1]
        self.rectangle.pos = rectangle_x, rectangle_y

    def update_opening_and_closing_circle_centers(self):

        opening_circle_center = self.get_circle_center('opening')
        closing_circle_center = self.get_circle_center('closing')

        self.set_circle_center('opening', opening_circle_center)
        self.set_circle_center('closing', closing_circle_center)

        if self.orientation == 'horizontal':
            x = opening_circle_center[0] - self.circle_diameters / 2
            self.pos = x, self.pos[1]
        else:
            y = opening_circle_center[1] - self.circle_diameters / 2
            self.pos = self.pos[0], y

    def get_circle_center(self, end):

        assert end in ['opening', 'closing'], 'end should be either opening or closing'

        assert self.orientation in ['horizontal', 'vertical'], 'orientation should be either horizontal or vertical'

        if self.orientation == 'vertical':
            circle_center_x = self.center_x
            if end == 'opening':
                circle_center_y = self.center_y + self.rectangle_height / 2
            else:
                circle_center_y = self.center_y - self.rectangle_height / 2
        else:
            #  this makes horizontal the default
            if end == 'opening':
                circle_center_x = self.center_x - self.rectangle_width / 2  # + self.size[1]/2
            else:
                circle_center_x = self.center_x + self.rectangle_width / 2  # - self.size[1]/2

            circle_center_y = self.get_center_y()

        return circle_center_x, circle_center_y

    def set_circle_center(self, end, value):

        if end == 'opening':
            self.opening_circle_center = value
            self.opening_circle.set_center(value)
        else:
            #  if end == 'closing:
            self.closing_circle_center = value
            self.closing_circle.set_center(value)

    def set_center_x(self, value):
        """ This is when you have the center_x, and you want to set all else relevant """
        self.center_x = value
        self.pos = value - self.size[0] / 2., self.pos[1]

    def get_center_x(self):
        return self.pos[0] + self.size[0] / 2

    def get_center_y(self):
        return self.pos[1] + self.size[1] / 2

    def set_center_y(self, value):
        """ This is when you have the center_y, and you want to set all else relevant """
        self.center_y = value
        self.pos = self.pos[0], value - self.size[1] / 2.

    def set_center(self, center):
        """ This is when you have the center, and you want to set all else relevant """
        self.center_x, self.center_y = center
        self.set_center_x(self.center_x)
        self.set_center_y(self.center_y)

        self.update_opening_and_closing_circle_centers()
        self.update_rectangle_center()

    def get_center(self):
        center_x = self.get_center_x()
        center_y = self.get_center_y()
        center = center_x, center_y
        return center

    def set_size(self, widget_size, size_hint=1):

        self.size_hint = size_hint

        if self.orientation == 'horizontal':
            self.size = widget_size[0], widget_size[1] * size_hint
        else:
            self.size = widget_size[0] * size_hint, widget_size[1]

        self.closing_circle.set_size(widget_size, size_hint)
        self.opening_circle.set_size(widget_size, size_hint)

        #  i could have done closing circle, or index 1
        self.circle_diameters = self.opening_circle.size[0]

        rectangle_size = self.get_rectangle_size()
        self.set_rectangle_size(rectangle_size)

        center = self.get_center()
        self.set_center(center)
        self.update_opening_and_closing_circle_centers()
        self.update_rectangle_center()

        if self.orientation == 'horizontal':
            self.size = self.circle_diameters + self.rectangle_width, self.rectangle_height
        else:
            self.size = self.rectangle_width, self.circle_diameters + self.rectangle_height

    def set_pos(self, pos):
        self.pos = pos
        center = self.get_center()
        self.set_center(center)
        self.update_opening_and_closing_circle_centers()
        self.update_rectangle_center()

    # def get_pos(self):
    #
    #     x = self.get_inner_x_at_y(self.center_y)
    #     y = self.get_inner_y_at_x(self.center_x)
    #
    #     return self.center_x - x, self.center_y - y

    def to_inner_center(self, x, y):
        local_x, local_y = x - self.pos[0], y - self.pos[1]
        from_center_x, from_center_y = local_x - self.size[0] / 2, local_y - self.size[1] / 2
        # factor_in_rectangle = from_center_x + self.rectangle_width/2, from_center_y + self.rectangle_height
        return from_center_x, from_center_y

    def get_inner_x_at_y(self, y, scale_bounds=False):

        height = self.rectangle_height
        width = self.rectangle_width
        radius = self.circle_diameters / 2
        if scale_bounds:
            height *= scale_bounds
            width *= scale_bounds
            radius *= scale_bounds

        if self.orientation == 'horizontal':

            if abs(y) > height / 2:
                return None

            semicircle_y = abs(y)  # - self.rectangle_height/2
            semicircle = sqrt(abs(semicircle_y ** 2 - abs(radius) ** 2))
            return width / 2 + semicircle
        else:

            if abs(y) > (height + radius * 2) / 2:
                return None

            if abs(y) < height / 2:
                #  not in range of a corner, just in the central rectangle area
                return width / 2
            else:
                #  this statement is to actually remove the width of the corner
                #  think about it: at the very sides of the circles, you take off the entire radius
                semicircle_y = abs(y) - height / 2
                semicircle = sqrt(abs(semicircle_y ** 2 - abs(radius) ** 2))
                return semicircle

    def get_inner_y_at_x(self, x, scale_bounds=False):

        height = self.rectangle_height
        width = self.rectangle_width
        radius = self.circle_diameters / 2
        if scale_bounds:
            height *= scale_bounds
            width *= scale_bounds
            radius *= scale_bounds

        if self.orientation == 'horizontal':

            if abs(x) > (width + radius * 2) / 2:
                return None

            if abs(x) < width / 2:
                #  not in range of a corner, just in the central rectangle area
                return height / 2
            else:

                #  this statement is to actually remove the height of the corner
                #  think about it: at the very sides of the circles, you take off the entire radius
                semicircle_x = abs(x) - width / 2
                semicircle = sqrt(abs(semicircle_x ** 2 - abs(radius) ** 2))
                return semicircle

        else:

            if not scale_bounds:
                if abs(x) > width / 2:
                    return None

            semicircle_x = abs(x)  # - self.rectangle_width / 2
            semicircle = sqrt(abs(semicircle_x ** 2 - abs(radius) ** 2))
            return height / 2 + semicircle
