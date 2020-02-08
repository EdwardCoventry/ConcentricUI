""" Some notes go here """

all__ = ('OblongSpinner',)

from kivy.compat import string_types
from kivy.factory import Factory
from kivy.properties import NumericProperty, DictProperty, ObjectProperty
from kivy.uix.spinner import Spinner

from concentricui.oblong.concentricoblongs import ConcentricOblongs
from concentricui.oblong.oblongbutton import OblongButton


class OblongSpinnerButton(OblongButton):
    parent_spinner = ObjectProperty()

    def __init__(self, **kwargs):
        super(OblongSpinnerButton, self).__init__(**kwargs)

        self.size_hint_y = None

    """ I need to bind this in screen change spinner instead.. """
    # def on_release(self, *args):
    #     App.get_running_app().root.current = self.text


from kivy.uix.dropdown import DropDown


class OblongSpinner(Spinner, ConcentricOblongs):
    dropdown_cls = ObjectProperty(DropDown)
    option_cls = ObjectProperty(OblongSpinnerButton)

    option_cls_kwargs = DictProperty()

    total_height = NumericProperty()

    #  in the original spinner class this is a boolproperty. but why limit to binary!
    sync_height = NumericProperty()

    def create_option_subclass(self, *args, **kwargs):

        option_cls_kwargs = kwargs

        class coloured_option(self.option_cls):

            def __init__(cls, **kwargs):

                cls.widget_walk_starting_point = self
                cls.parent_spinner = self

                # cls.shape_count = option_cls_kwargs['shape_count'] if 'shape_count' in option_cls_kwargs else self.shape_count
                cls.shape_size_hint_list = option_cls_kwargs[
                    'shape_size_hint_list'] if 'shape_size_hint_list' in option_cls_kwargs else self.shape_size_hint_list
                # cls.shape_colour_list = option_cls_kwargs['shape_colour_list'] if 'shape_colour_list' in option_cls_kwargs else self.shape_colour_list
                cls.colour_scheme = option_cls_kwargs[
                    'colour_scheme'] if 'colour_scheme' in option_cls_kwargs else self.colour_scheme
                cls.master_colour = option_cls_kwargs[
                    'master_colour'] if 'master_colour' in option_cls_kwargs else self.master_colour
                cls.text_colour = option_cls_kwargs[
                    'text_colour'] if 'text_colour' in option_cls_kwargs else self.text_colour

                if self.total_height:
                    cls.height = (self.total_height - self.height) / len(self.values)
                else:
                    cls.height = self.height / 2

                super(coloured_option, cls).__init__(**kwargs)

        self.option_cls = coloured_option

    # def set_text_size(self, *args):
    #     self.text_size = self.size
    #     self.valign = 'center'
    #     self.halign = 'center'
    #     self.font_size = self.height*0.8

    # sync_height = True
    # text_autoupdate = True

    def on_text(self, wid, text):


        if not self.content_pin:
            self.content_pin = self.text
        elif type(self.content_pin) is str:
            self.content_pin = text
        else:
            self.content_pin.text = text

    def __init__(self, **kwargs):
        super(OblongSpinner, self).__init__(**kwargs)

        self.create_option_subclass(**self.option_cls_kwargs)

        self.color = 0, 0, 0, 0

        if not self.content_pin:
            self.content_pin = self.text

        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.background_down = ''
        self.background_disabled_normal = ''
        self.background_disabled_down = ''

    def _update_dropdown(self, *largs):
        dp = self._dropdown
        cls = self.option_cls
        values = self.values
        text_autoupdate = self.text_autoupdate
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        dp.clear_widgets()
        for value in values:
            item = cls(text=value)
            #  bellow is the line i have changed
            item.height = self.height * self.sync_height if self.sync_height else item.height
            item.bind(on_release=lambda option: dp.select(option.text))
            dp.add_widget(item)
        if text_autoupdate:
            if values:
                if not self.text or self.text not in values:
                    self.text = values[0]
            else:
                self.text = ''
    #
    # def on_master_colour(self, wid, value):
    #     super(OblongSpinner, self).on_master_colour(wid, value)
    #
    #     print('----------------------------------------------')
    #     self.set_secondary_colours()
    #
    #
    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         self.set_secondary_colours()
    #         print('!!!!!!!!!!!!!!!!!!', 'self.shape_colour_list', self.shape_colour_list, 'self.colour_instruction_list', self.colour_instruction_list)
