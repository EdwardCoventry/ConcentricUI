""" Some notes go here """

all__ = ('ConcentricOblongs',)

from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, AliasProperty, ReferenceListProperty
from kivy.uix.widget import Widget

from ConcentricUI.behaviours.concentricshapes import ConcentricShapes
from ConcentricUI.oblong.oblong import Oblong
from ConcentricUI.widgets.textbutton import Text


class ConcentricOblongs(ConcentricShapes):
    draw_shape_toggle = True

    orientation = StringProperty('horizontal')

    opening_pin = ObjectProperty()
    closing_pin = ObjectProperty()
    content_pin = ObjectProperty()

    pins = ReferenceListProperty(opening_pin, closing_pin, content_pin)

    pin_canvas_layer = None

    def __init__(self, **kwargs):

        self.font_ratio = 0.25

        if 'text_colour' in kwargs:
            self.text_colour = kwargs.pop('text_colour')
        if 'opening_pin' in kwargs:
            self.opening_pin = kwargs.pop('opening_pin')
        if 'closing_pin' in kwargs:
            self.closing_pin = kwargs.pop('closing_pin')
        if 'content_pin' in kwargs:
            self.content_pin = kwargs.pop('content_pin')

        super(ConcentricOblongs, self).__init__(**kwargs)

        self.add_pins()

        self.bind(size=Clock.schedule_once(self.set_pin_pos))
        self.bind(pos=self.set_pin_pos)
        self.bind(opening_anchor=self.set_pin_pos)
        self.bind(closing_anchor=self.set_pin_pos)
        self.bind(center=self.set_pin_pos)
        self.bind(shape_list=self.add_pins)

    def add_pins(self):
        for pin_position, pin in ('opening_pin', self.opening_pin), ('closing_pin', self.closing_pin), (
                'content_pin', self.content_pin):
            self.add_pin(pin_position=pin_position, pin_item=pin)

    def on_opening_pin(self, wid, pin):
        self.add_pin('opening_pin', pin)

    def on_closing_pin(self, wid, pin):
        self.add_pin('closing_pin', pin)

    def on_content_pin(self, wid, pin):
        self.add_pin('content_pin', pin)

    def add_pin(self, pin_position, pin_item, *args):

        little_pin_dict = {'opening_pin': self.opening_pin, 'closing_pin': self.closing_pin,
                           'content_pin': self.content_pin}

        pin = little_pin_dict[pin_position]

        if not pin:
            return
        if pin_item is True:
            """ This is for if you want a placeholder. It's a blank widget """
            pin_widget = Widget()
        elif type(pin) == str:
            pin_widget = Text(text=pin, color=self.text_colour, font_ratio=self.font_ratio)
            self.bind(text_colour=pin_widget.set_colour)
        elif type(pin) == int:
            pin_widget = Text(text=str(pin), color=self.text_colour, font_ratio=self.font_ratio)
            self.bind(text_colour=pin_widget.set_colour)
        elif type(pin) == float:
            pin_widget = Text(text="{0:.3g}".format(pin), color=self.text_colour, font_ratio=self.font_ratio)
            self.bind(text_colour=pin_widget.set_colour)
        elif issubclass(type(pin), ConcentricShapes):
            pin_widget = pin_item
        else:
            pin_widget = pin
        pin_widget.id = pin_position

        # if (hasattr(pin_widget, 'master_colour') and not pin_widget.master_colour) or (hasattr(pin_widget, 'colour_scheme') and pin_widget.colour_scheme):
        #     if self.master_colour:
        #         print('this')
        #         pin_widget.master_colour = self.master_colour
        #     elif self.colour_scheme:
        #         print('that')
        #         pin_widget.colour_scheme = self.colour_scheme

        setattr(pin_widget, 'colour_scheme', self.colour_scheme)
        # setattr(pin_widget, 'use_master_colour', self.use_master_colour)
        setattr(pin_widget, 'master_colour', tuple(self.master_colour))

        try:
            self.remove_widget(pin)
            self.add_widget(pin_widget, canvas=self.pin_canvas_layer)
        except:
            print("couldn't add {} widget. probably its already added".format(pin_position))

        setattr(self, pin_position, pin_widget)

        self.set_pin_pos()

    def set_pin_pos(self, *args):

        if not self.shape_list:
            return None

        if self.opening_pin:
            if issubclass(type(self.opening_pin), Widget):
                diameter = self.get_inner_shape_diameter()
                self.opening_pin.size = (diameter, diameter)
                self.opening_pin.center = self.opening_anchor

        if self.closing_pin:
            if issubclass(type(self.closing_pin), Widget):
                diameter = self.get_inner_shape_diameter()
                self.closing_pin.size = (diameter, diameter)
                self.closing_pin.center = self.closing_anchor
        if self.content_pin:
            if issubclass(type(self.content_pin), Widget):
                self.set_content_pin_size()
                self.set_content_pin_pos()

        for pin in (self.opening_pin, self.closing_pin, self.content_pin):
            # if issubclass(type(pin), Label)
            if hasattr(pin, 'text_size'):
                pin.text_size = pin.size

    def set_content_pin_size(self, *args):

        if self.orientation == 'horizontal':
            left = self.opening_pin.right if issubclass(type(self.opening_pin), Widget) else self.inner_x
            right = self.closing_pin.x if issubclass(type(self.closing_pin), Widget) else self.inner_right

            width = right - left
            height = self.height

        if self.orientation == 'vertical':
            bottom = self.opening_pin.top if issubclass(type(self.opening_pin), Widget) else self.inner_y
            top = self.closing_pin.y if issubclass(type(self.closing_pin), Widget) else self.inner_top

            height = top - bottom
            width = self.inner_width

        self.content_pin.size = width, height

    def set_content_pin_pos(self, *args):

        if self.orientation == 'horizontal':
            left = self.opening_pin.right if issubclass(type(self.opening_pin), Widget) else self.inner_x
            x = left + self.content_pin.width / 2
            y = self.center_y

        if self.orientation == 'vertical':
            bottom = self.opening_pin.top if issubclass(type(self.opening_pin), Widget) else self.inner_y
            y = bottom + self.content_pin.height / 2
            x = self.center_x

        self.content_pin.center = x, y

    def get_opening_anchor(self):
        if self.shape_list:
            return self.shape_list[-1].opening_circle_center
        else:
            return None

    def set_opening_anchor(self, value):
        pass

    def get_closing_anchor(self):
        if self.shape_list:
            return self.shape_list[-1].closing_circle_center
        else:
            return None

    def set_closing_anchor(self, value):
        pass

    opening_anchor = AliasProperty(get_opening_anchor, set_opening_anchor)
    closing_anchor = AliasProperty(get_closing_anchor, set_closing_anchor)

    def draw_shape(self, shape_size_hint, shape_colour, **kwargs):
        """ overwrite this function for circle, oblong, rounded rectangle """

        # Color(*shape_colour)
        width, height = self.width * shape_size_hint, self.height * shape_size_hint

        shape = Oblong(orientation=self.orientation, size=(width, height), size_hint=shape_size_hint,
                       min_size_hint=min(self.shape_size_hint_list), max_size_hint=max(self.shape_size_hint_list),
                       pos=self.pos)

        return shape

    def get_inner_shape_diameter(self):

        if self.orientation == 'horizontal':
            return self.get_inner_shape_height()
        elif self.orientation == 'vertical':
            return self.get_inner_shape_width()
        else:
            raise Exception("orientation should be horizontal or vertical.....")

    # def update_shape_list_size(self, *args):
    #
    #     super(ConcentricOblongs, self).update_shape_list_size(*args)
    #
    #     for shape in self.shape_list:
    #         shape.rectangle_width = self.width-self.height
