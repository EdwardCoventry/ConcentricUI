""" Some notes go here """

all__ = ('CircleSlider',)

from functools import partial

from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty, AliasProperty
from kivy.uix.slider import Slider

from ConcentricUI.circle.circlelabel import CircleLabel
from ConcentricUI.circle.concentriccircles import ConcentricCircles
from ConcentricUI.oblong.concentricoblongs import ConcentricOblongs


class CircleSlider(Slider, ConcentricCircles):
    integers = BooleanProperty(False)

    decimal_places = NumericProperty(0)
    sig_figs = NumericProperty(None)

    def get_formatted_value(self):

        #  fixme add sig figs please

        if self.integers:
            return str(int(self.value))

        if self.value:
            # if self.sig_figs and self.decimal_places:
            #     formatting = "{" + ":{}.{}f".format(self.sig_figs, self.decimal_places) + "}"
            # elif self.sig_figs and not self.decimal_places:
            #     formatting = "{" + ":{}.{}f".format(self.sig_figs, self.decimal_places) + "}"
            # return formatting.format(self.value)
            return "{:.{}f}".format(self.value, self.decimal_places)
        else:
            return ''

    formatted_value = AliasProperty(get_formatted_value, bind=['value', 'decimal_places', 'sig_figs'])

    circle_label = ObjectProperty()
    display_value_toggle = BooleanProperty(False)

    #  0 is instant
    update_slowdown = NumericProperty(0)

    selected = BooleanProperty(False)

    slider_bar = ObjectProperty()
    slider_bar_toggle = ObjectProperty(True)

    draw_shape_toggle = ObjectProperty(False)

    def __init__(self, **kwargs):
        #
        # self.colour_scheme = kwargs.pop('colour_scheme')
        # self.master_colour = kwargs.pop('master_colour')

        self.circle_label = None
        if 'slider_bar_toggle' in kwargs:
            self.slider_bar_toggle = kwargs.pop('slider_bar_toggle')

        super(CircleSlider, self).__init__(**kwargs)
        # self.value = kwargs.pop('value')
        # self.sensitivity = kwargs.pop('sensitivity')

        #  disable all the slider's old images
        self.cursor_image = '../textures/blank.png'
        self.cursor_width = 0
        self.cursor_height = 0
        self.background_horizontal = ''
        self.background_disabled_horizontal = ''
        self.background_vertical = ''
        self.background_disabled_vertical = ''

        self.background_width = 0

        if self.slider_bar_toggle:
            """ you can change do shape_dictionary=self.shape_dictionary if you want this little bar to be concentric
                but im pretty sure it looks awful so im not even going to provide an option for that """
            self.slider_bar = ConcentricOblongs(size=self.size, pos=self.pos, orientation=self.orientation,
                                                master_colour=self.master_colour, colour_scheme=self.colour_scheme,
                                                allow_concentric=False)
            self.add_widget(self.slider_bar)
            self.bind(size=self.set_slider_bar_size_and_pos)
            self.bind(pos=self.set_slider_bar_size_and_pos)

        print('DID ITT')

        self.font_size_hint = 0.5
        self.circle_label = CircleLabel(text=self.formatted_value, font_size_hint=self.font_size_hint,
                                        text_colour=self.text_colour, bold=True, size=self.size, pos=self.pos,
                                        shape_dictionary=self.shape_dictionary, colour_scheme=self.colour_scheme,
                                        master_colour=self.master_colour)

        print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',
              self.text_colour)

        self.add_widget(self.circle_label)

        self.bind(size=self.update_shape_list_size)
        self.bind(center=self.update_shape_list_pos)
        self.bind(value_pos=self.update_shape_list_pos)

        self.bind_display_text()

    def on_display_value_toggle(self, wid, bind_text_toggle):
        self.bind_display_text()

    def bind_display_text(self):

        if not self.circle_label:
            return

        if self.display_value_toggle:
            self.circle_label.text = self.formatted_value
            self.bind(value=self.set_cursor_text)
            self.bind(text_colour=self.set_cursor_text_colour)
        else:
            self.unbind(value=self.set_cursor_text)
            self.unbind(text_colour=self.set_cursor_text_colour)
            self.circle_label.text = ''

    def set_cursor_text(self, *args):
        #  fixme - could use some cursor text formatting. eg decimal places/sig fig
        self.circle_label.text = self.formatted_value

    # def on_text_colour(self, wid, colour):
    #     self.set_cursor_text_colour()

    def set_cursor_text_colour(self, *args):
        print('om setting this')
        self.circle_label.text_colour = self.text_colour

    def on_size(self, wid, size):
        if self.circle_label:
            self.circle_label.size = size

    def set_slider_bar_size_and_pos(self, *args):
        if self.slider_bar:
            self.slider_bar.size = (self.width - self.circle_label.get_inner_shape_width(),
                                    self.height / 10) if self.orientation == 'horizontal' else (
                self.width / 10, self.height - self.circle_label.get_inner_shape_height())
            self.slider_bar.center = self.center

            print('good bat!!!', self.slider_bar.size)

    def set_slider_bar_colour(self, wid, colour):
        if self.slider_bar:
            self.slider_bar.master_colour = colour
        if self.circle_label:
            self.circle_label.master_colour = colour

    def pass_master_colour_to_children(self, wid, colour):
        super(CircleSlider, self).pass_master_colour_to_children(wid, colour)
        print('got here!!!!!!!!!!!!!!!')
        self.set_slider_bar_colour(wid, colour)

    def update_shape_list_size(self, *args):
        # self.circle_label.diamter = min(self.size)
        super(CircleSlider, self).update_shape_list_size()

    def update_shape_list_pos(self, *args):

        """ I'm overwriting this from concentric shapes """

        if self.orientation == 'horizontal':
            center = (self.value_pos[0], self.center_y)
        else:
            center = (self.center_x, self.value_pos[1])

        self.circle_label.center = center

        return

    def on_touch_down(self, touch):
        if self.circle_label.collide_point(*touch.pos):
            super(CircleSlider, self).on_touch_down(touch)
            self.selected = True

    def on_touch_up(self, touch):
        super(CircleSlider, self).on_touch_up(touch)
        self.selected = False

    def on_value(self, wid, value):

        if self.integers:
            value = int(value)

        if self.update_slowdown:
            Clock.create_trigger(partial(self.set_slow_value, value), self.update_slowdown, False)
            return
        else:
            self.value = value

    def set_slow_value(self, value):
        self.value = value
