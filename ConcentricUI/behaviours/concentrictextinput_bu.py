""" Some notes go here """

all__ = ('ConcentricButton',)

from kivy.cache import Cache
from kivy.graphics import Color
from kivy.properties import ObjectProperty, VariableListProperty, BooleanProperty, AliasProperty
from kivy.uix.textinput import TextInput

from concentricui.behaviours.concentricfontscaling import ConcentricFontScaling
from concentricui.behaviours.concentricshapes import ConcentricShapes

Cache_get = Cache.get
Cache_append = Cache.append


class ConcentricTextInput(ConcentricShapes, ConcentricFontScaling, TextInput):

    def update(self, *args):
        pass

    def get_texture_size(self):

        label_size_list = [x.size for x in self._lines_labels]

        label_width_list = [x[0] for x in label_size_list]
        label_height_list = [x[1] for x in label_size_list]

        if not (len(list(label_width_list)) and len(list(label_height_list))):
            return None

        max_texture_width = max(label_width_list)
        total_texture_height = sum(label_height_list)

        return max_texture_width, total_texture_height

    def set_texture_size(self, value):
        raise Exception('certainly not yet implemented')

    texture_size = AliasProperty(get_texture_size, set_texture_size)

    def update_padding(self, *args):
        text_width = self._get_text_width(
            self.text,
            self.tab_width,
            self._label_cached
        )
        self.padding = (self.width - text_width) / 2, self.height - self.font_size / 2

    def update_hint_padding(self, *args):
        text_width = self._get_text_width(
            self.hint_text,
            self.tab_width,
            self._label_cached
        )
        self.padding = (self.width - text_width) / 2, self.padding[1]

    def clear_input(self):
        self.text = ""

    def on_width(self, instance, value):
        self.update_padding()

    def set_focus(self, focus):
        self.toggle_focus = focus
        self.focus = focus

    text_display = ObjectProperty()

    padding = VariableListProperty()

    scale_text = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.background_color = [0, 0, 0, 0]
        self.background_normal = ''
        self.background_down = ''
        self.background_disabled_normal = ''
        self.background_disabled_down = ''

        self.foreground_color = (0, 1, 0, 1)
        # self.color = (0,1,0,1)

        # self.text_size = 400,400

        # self.font_size = self.inner_height
        self.multiline = False
        self.padding = [0, 0, 0, 0]
        # self.hint_text = 'save soem typing'
        # self.hint_text_color = (1,1,1)

        self.halign = 'center'
        self.valign = 'center'

        # kwargs['foreground_color'] = (1,1,1,1)

        super(ConcentricTextInput, self).__init__(**kwargs)

        with self.canvas.before:
            Color(*self.foreground_color)
        #
        # if self.scale_text:
        #     self.bind(inner_size=Clock.schedule_once(self.set_font_size, -1))

        # self.text_display = CircleLabel(size=self.size, pos=self.pos)

        # self.add_widget(self.text_display)

    #

    def on_text(self, wid, text):

        if self.shape_list:
            self.set_font_size()

    #
    # def on_label_cached(self, wid, label):
    #
    #     '''this could be quite useful....'''
