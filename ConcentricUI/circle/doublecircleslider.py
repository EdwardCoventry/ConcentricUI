""" Some notes go here """

all__ = ('DoubleCircleSlider',)

from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty

from ConcentricUI.behaviours.concentricshapes import ConcentricShapes
from ConcentricUI.circle.circleslider import CircleSlider
from ConcentricUI.oblong.concentricoblongs import ConcentricOblongs


class DoubleCircleSlider(ConcentricShapes):
    #  fixme i'd like to have something such that if the two slider values are the same, then each is shifted by half of
    #  fixme its width away from each other

    integers = BooleanProperty(False)
    decimal_places = NumericProperty()

    #  not sure how implemented this is
    update_slowdown = NumericProperty()

    # not yet implemented
    space_values = NumericProperty()


    min = CircleSlider.min
    max = CircleSlider.max
    padding = CircleSlider.padding
    orientation = CircleSlider.orientation
    range = CircleSlider.range
    step = CircleSlider.step
    display_value_toggle = CircleSlider.display_value_toggle
    slider_bar_toggle = CircleSlider.slider_bar_toggle

    display_value_formatting = StringProperty()

    min_slider = ObjectProperty()
    max_slider = ObjectProperty()

    min_value = NumericProperty()
    max_value = NumericProperty()

    values = ReferenceListProperty(min_value, max_value)

    closer_widget = ObjectProperty(None, allownone=True)

    def on_display_value_toggle(self, wid, bind_text_toggle):
        if self.min_slider and self.max_slider:
            self.min_slider.display_value_toggle = bind_text_toggle
            self.max_value.display_value_toggle = bind_text_toggle

    def draw_shape(self, **kwargs):
        return

    def __init__(self, **kwargs):

        self.min_slider = None
        self.max_slider = None
        self.slider_bar = None

        super(DoubleCircleSlider, self).__init__(**kwargs)

        if not self.min_value:
            self.min_value = self.range[0]
        elif not self.min <= self.min_value <= self.max:
            raise Exception("min value {} out of range {}".format(self.min_value, self.range))
        if not self.max_value:
            self.max_value = self.range[1]
        elif not self.min <= self.max_value <= self.max:
            raise Exception("max value {} out of range {}".format(self.max_value, self.range))

        # self.orientation = kwargs.pop('orientation')
        # self.shape_size_hint_list = kwargs.pop('shape_size_hint_list')
        # self.master_colour = kwargs.pop('master_colour')

        self.cursor_size = 0, 0
        self.sensitivity = 'handle'

        min_kwargs = {'value': self.min_value,
                      'integers': self.integers,
                      'decimal_places': self.decimal_places,
                      'update_slowdown': self.update_slowdown,
                      'min': self.min,
                      'max': self.max,
                      'padding': self.padding,
                      'orientation': self.orientation,
                      # 'range': self.range,
                      'step': self.step,
                      'sensitivity': 'handle',
                      'pos': self.pos,
                      'size': self.size,
                      'text_colour': self.text_colour,
                      'colour_scheme': self.colour_scheme,
                      'master_colour': self.master_colour,
                      'shape_dictionary': self.shape_dictionary,
                      'display_value_toggle': self.display_value_toggle,
                      'display_value_formatting': self.display_value_formatting,
                      'slider_bar_toggle': False,
                      'draw_shape_toggle': False}

        max_kwargs = {'value': self.max_value,
                      'integers': self.integers,
                      'decimal_places': self.decimal_places,
                      'update_slowdown': self.update_slowdown,
                      'min': self.min,
                      'max': self.max,
                      'padding': self.padding,
                      'orientation': self.orientation,
                      # 'range': self.range,
                      'step': self.step,
                      'sensitivity': 'handle',
                      'pos': self.pos,
                      'size': self.size,
                      'text_colour': self.text_colour,
                      'colour_scheme': self.colour_scheme,
                      'master_colour': self.master_colour,
                      'shape_dictionary': self.shape_dictionary,
                      'display_value_toggle': self.display_value_toggle,
                      'display_value_formatting': self.display_value_formatting,
                      'slider_bar_toggle': False,
                      'draw_shape_toggle': False}

        if self.slider_bar_toggle:

            print('^^^^^^^^^^^^^')

            """ you can change do shape_dictionary=self.shape_dictionary if you want this little bar to be concentric
                but im pretty sure it looks awful so im not even going to provide an option for that """
            # self.slider_bar = ConcentricOblongs(size=self.size, pos=self.pos, orientation=self.orientation,
            #                                     master_colour=self.master_colour, colour_scheme=self.colour_scheme,
            #                                     allow_concentric=False)
            self.slider_bar = ConcentricOblongs(size=self.size,
                                                pos=self.pos,
                                                orientation=self.orientation,
                                                master_colour=self.master_colour,
                                                colour_scheme=self.colour_scheme,
                                                allow_concentric=True)
            self.add_widget(self.slider_bar)

            self.bind(size=self.set_slider_bar_size_and_pos)
            self.bind(pos=self.set_slider_bar_size_and_pos)

        # self.bind(master_colour=self.set_slider_bar_colour)

        self.min_slider = CircleSlider(**min_kwargs)
        self.max_slider = CircleSlider(**max_kwargs)

        self.min_slider.bind(value=self.set_double_slider_min_max)
        self.max_slider.bind(value=self.set_double_slider_min_max)

        self.bind(text_colour=self.set_cursor_text_colour)

        self.add_widget(self.min_slider)
        self.add_widget(self.max_slider)

    def pass_master_colour_to_children(self, wid, colour):
        super(DoubleCircleSlider, self).pass_master_colour_to_children(wid, colour)
        self.set_slider_bar_colour(wid, colour)

    def set_slider_bar_colour(self, wid, colour):

        print('yyyyyyyyyyyyyyyyyyyy', self.slider_bar)

        if self.slider_bar:
            self.slider_bar.master_colour = colour

        if self.min_slider and self.max_slider:
            self.min_slider.master_colour = colour
            self.max_slider.master_colour = colour

            self.min_slider.pass_master_colour_to_children(wid, colour)
            self.max_slider.pass_master_colour_to_children(wid, colour)

    def set_slider_bar_size_and_pos(self, *args):
        Clock.schedule_once(self.do_set_slider_bar_size_and_pos, -1)

    def do_set_slider_bar_size_and_pos(self, *args):
        if self.slider_bar:
            self.slider_bar.size = (self.width - self.min_slider.circle_label.get_inner_shape_width(),
                                    self.height / 10) if self.orientation == 'horizontal' else (
                self.width / 10, self.height - self.min_slider.circle_label.get_inner_shape_height())
            self.slider_bar.center = self.center

        self.min_slider.size = self.size
        self.max_slider.size = self.size

        self.min_slider.center = self.center
        self.max_slider.center = self.center

    # def on_slider_bar(self):
    #     self.set_slider_bar_size_and_pos()
    #     #self.set_slider_bar_colour()

    def set_cursor_text_colour(self, *args):
        self.min_slider.text_colour = self.text_colour
        self.max_slider.text_colour = self.text_colour

    def on_touch_down(self, touch):

        # self.min_slider.update_shape_list_pos()
        # self.max_slider.update_shape_list_pos()

        if not self.collide_point(*touch.pos):
            return False

        pos_dimension = 0 if self.orientation is 'horizontal' else 1

        touch_distance_from_min_slider = abs(self.min_slider.value_pos[pos_dimension] - touch.pos[pos_dimension])
        touch_distance_from_max_slider = abs(self.max_slider.value_pos[pos_dimension] - touch.pos[pos_dimension])

        self.closer_widget = self.min_slider if touch_distance_from_min_slider < touch_distance_from_max_slider else self.max_slider

        if self.sensitivity == 'handle':
            #  check you've actually collided with it...... could even do this earlier
            if not self.closer_widget.circle_label.collide_point(*touch.pos):
                return True
        elif self.sensitivity == 'all':
            pass
        else:
            raise Exception("This shouldnt happen. sensitivity should be 'handle', or 'all'")

        #  removing and adding a widget moves it to top of draw order
        self.remove_widget(self.closer_widget)
        self.add_widget(self.closer_widget)

        touch.grab(self.closer_widget)

        # print(':)', self.master_colour, self._master_colour, self.pseudo_bind_master_colour_attribute)

        return True

    def on_touch_move(self, touch):

        if not self.collide_point(*touch.pos):
            return False

        if self.closer_widget:
            if self.closer_widget.selected:
                self.closer_widget.on_touch_move(touch)

                return True

    def on_touch_up(self, touch):

        if not self.collide_point(*touch.pos):
            return False

        if self.closer_widget:
            closer_widget = self.closer_widget
            self.closer_widget = None
            closer_widget.on_touch_move(touch)
        else:
            super(DoubleCircleSlider, self).on_touch_up(touch)

    def set_double_slider_min_max(self, *args):
        self.min_value, self.max_value = sorted((self.min_slider.value, self.max_slider.value))

    # def on_size(self, wid, size):
    #     self.min_slider.size = size
    #     self.max_slider.size = size

    # def on_pos(self, wid, pos):
    #     self.min_slider.pos = pos
    #     self.max_slider.pos = pos
