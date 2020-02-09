""" Some notes go here """

#  fixme - need to do something with the cursor position

all__ = ('ConcentricButton',)

from kivy.clock import Clock
from kivy.graphics import Color
from kivy.properties import ObjectProperty, ListProperty, VariableListProperty, BooleanProperty, NumericProperty
from kivy.uix.textinput import TextInputCutCopyPaste, TextInput

from ConcentricUI.behaviours.concentricshapes import ConcentricShapes
from ConcentricUI.roundedrectangle.roundedrectangle import RoundedRec as RoundedRectangle


class RoundedRectangleTextInputCutCopyPaste(TextInputCutCopyPaste):
    def __init__(self, **kwargs):
        super(RoundedRectangleTextInputCutCopyPaste, self).__init__(**kwargs)


from ConcentricUI.oblong.concentricoblongs import ConcentricOblongs
from ConcentricUI.oblong.oblong import Oblong


class OblongCursor(ConcentricOblongs):
    """ make use of TextInput.cursor_pos """

    def __init__(self, **kwargs):
        super(OblongCursor, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.width = 10
        # self.shape_size_hint_list = [1]
        # self.shape_colour_list = [[0,1,1,1]]


from kivy.uix import textinput

textinput.TextInputCutCopyPaste = RoundedRectangleTextInputCutCopyPaste


class ConcentricTextInput(ConcentricShapes, TextInput):
    # keyboard_mode = 'auto'

    do_padding = ObjectProperty('test')

    font_size_hint = NumericProperty(1)

    def update(self, *args):
        pass
        self.update_padding()

    def get_texture_size(self):

        for x in self._lines_labels:
            x.flip_horizontal()

        label_size_list = [x.size for x in self._lines_labels]

        label_width_list = [x[0] for x in label_size_list]
        label_height_list = [x[1] for x in label_size_list]

        if not (len(list(label_width_list)) and len(list(label_height_list))):
            return None

        max_texture_width = max(label_width_list)
        total_texture_height = sum(label_height_list)

        return max_texture_width, total_texture_height

    # def set_texture_size(self, value):
    #     self.set_oblong_cursor_pos()
    #     self.texture_size = value
    # raise Exception('certainly not yet implemented')

    # texture_size = AliasProperty(get_texture_size, set_texture_size, bind=['padding'])

    texture_size = ListProperty()

    def set_font_size(self, *args):

        # inner_height = self.get_inner_height_at_x(self.center_x)
        # if not inner_height:
        #     return
        # self.font_size = inner_height * 0.5
        #
        # self._trigger_refresh_text()
        # self.update_padding()
        #
        # Clock.schedule_once(self.texture_size_callback)

        self.font_size = self.inner_height * self.font_size_hint

        #self.padding_y = (self.font_size - self.height) / 2 + self.font_size / 2
        self.padding = 0, (self.height - self.inner_height) / 2
        #self.padding_y = 0

        self.oblong_cursor.set_size((self.cursor_width, self.font_size))

        self.set_oblong_cursor_pos()
        return
        #
        #
        # texture_width, texture_height = self.texture_size
        #
        # #  once i have a new value for texture height i can use this scalar to get the desired font size
        # texture_size_to_font_size_scalar = texture_height / self.font_size
        #
        # if texture_height > texture_width:
        #     font_size = self.inner_height / texture_size_to_font_size_scalar
        #
        # else:
        #
        #     #
        #     texture_size_to_inner_width_scalar = self.inner_width/texture_width
        #
        #     new_height = texture_size_to_inner_width_scalar * texture_height
        #
        #     font_size = new_height / texture_size_to_font_size_scalar
        # self.font_size = font_size
        # self._trigger_refresh_text()

    # def on_text(self, wid, text):
    #
    #     if self.text:
    #         self.set_font_size()
    #
    #     Clock.schedule_once(self.texture_size_callback)
    #
    #     print(':))', self.text_colour, self.foreground_color)

    # def texture_size_callback(self, *args):
    #
    #     self.texture_size = self.get_texture_size()
    #     #self.set_oblong_cursor_pos()

    def update_padding(self, *args):

        #return
        if not self.text:
            self.padding = self.width / 2, self.center_y / 2
            return

        text_width = self._get_text_width(
            self.text,
            self.tab_width,
            self._label_cached
        )

        padding_y = self.y / 2
        #padding_y = -1000
        inner_width = self.get_inner_width_at_y(self.center_y + self.font_size / 2)

        padding_x_when_text_box_not_filled = (self.width - text_width) / 2
        # padding_x_when_text_box_is_filled = (self.width - inner_width) / 2
        padding_x_when_text_box_is_filled = self.inner_x - self.x if self.inner_x else self.x
        # padding_x = min(abs(padding_x_when_text_box_not_filled), abs(padding_x_when_text_box_is_filled))

        if not inner_width:
            return
        padding_x = padding_x_when_text_box_not_filled if text_width < inner_width else padding_x_when_text_box_is_filled

        if not self.do_padding:
            self.padding = 0, 0
        elif self.do_padding == 'x':
            self.padding = padding_x, 0
        elif self.do_padding == 'y':
            self.padding = 0, padding_y
        elif self.do_padding == 'test':
            padding_x = padding_x_when_text_box_not_filled if text_width < inner_width else 0
            self.padding = padding_x, padding_y
        else:
            self.padding = padding_x, padding_y

    def update_hint_padding(self, *args):

        if not self.inner_x:
            return

        self.padding = self.inner_x, (self.height - self.font_size) / 2

    def clear_input(self):
        self.text = ""

    def on_size(self, instance, value):
        super(ConcentricTextInput, self).on_size(instance, value)
        Clock.schedule_once(self.set_font_size, -1)
        # Clock.schedule_once(self.update_padding)

    # def set_focus(self, focus):
    #     self.toggle_focus = focus
    #     self.focus = focus

    text_display = ObjectProperty()

    padding = VariableListProperty()

    scale_text = BooleanProperty(True)

    def set_oblong_cursor_pos(self, *args):
        if self.oblong_cursor:
            self.oblong_cursor.set_pos((self.cursor_pos[0], self.cursor_pos[1] - self.oblong_cursor.size[1]))

    def set_oblong_cursor_size(self, *args):
        if self.oblong_cursor and len(self.texture_size) == 2:
            texture_width, texture_height = self.texture_size
            self.oblong_cursor.set_size((self.cursor_width, texture_height))

    def set_oblong_cursor_colour(self, *args):
        if self.oblong_cursor:
            self.oblong_cursor_colour_instruction.rgba = self.cursor_color

    cursor_color = ListProperty([1, 1, 1, 0.5])
    selection_color = ListProperty([1, 1, 1, 0.5])

    def __init__(self, **kwargs):
        self.background_color = [0, 0, 0, 0]
        self.background_normal = ''
        self.background_down = ''
        self.background_disabled_normal = ''
        self.background_disabled_down = ''

        # self.foreground_color = (0,1,0,1)

        self.multiline = False
        self.padding = [0, 0, 0, 0]

        self.halign = 'center'
        self.valign = 'center'

        super(ConcentricTextInput, self).__init__(**kwargs)

        self.cursor_opacity = self.cursor_color[3]
        self.cursor_color[3] = 0

        # self.oblong_cursor = OblongCursor()
        #
        # self.add_widget(self.oblong_cursor)

        with self.canvas.after:
            self.oblong_cursor_colour_instruction = Color(*self.cursor_color)
            self.oblong_cursor = Oblong(size=(self.cursor_width, self.font_size), orientation='vertical')

        self.bind(cursor_pos=self.set_oblong_cursor_pos)
        # self.bind(size=self.set_oblong_cursor_size)
        # self.bind(texture_size=self.set_oblong_cursor_size)
        self.bind(cursor_color=self.set_oblong_cursor_colour)

        with self.canvas.before:
            self.text_colour_instruction = Color(*self.text_colour)

        self.bind(_cursor_blink=self.oblong_cursor_blink)
        self.bind(focus=self.hide_oblong_cursor_on_loose_focus)


        self.bind(text=self.set_font_size)

    def oblong_cursor_blink(self, wid=None, cursor_state=False):

        if self.selection_text or not self.text:
            cursor_state = False

        self.oblong_cursor_colour_instruction.a = cursor_state * self.cursor_opacity

    def hide_oblong_cursor_on_loose_focus(self, wid, focus):
        if self.focus == False:
            if self._cursor_blink:
                self._cursor_blink = False

    def _draw_selection(self, *largs):

        """" The one change is changing rectangle to rounded rectangle on the lastish line """

        pos, size, line_num, (s1c, s1r), (s2c, s2r), \
        _lines, _get_text_width, tab_width, _label_cached, width, \
        padding_left, padding_right, x, canvas_add, selection_color = largs
        # Draw the current selection on the widget.
        if line_num < s1r or line_num > s2r:
            return
        x, y = pos
        w, h = size
        x1 = x
        x2 = x + w
        if line_num == s1r:
            lines = _lines[line_num]
            x1 -= self.scroll_x
            x1 += _get_text_width(lines[:s1c], tab_width, _label_cached)
        if line_num == s2r:
            lines = _lines[line_num]
            x2 = (x - self.scroll_x) + _get_text_width(lines[:s2c],
                                                       tab_width,
                                                       _label_cached)
        width_minus_padding = width - (padding_right + padding_left)
        maxx = x + width_minus_padding
        if x1 > maxx:
            return
        x1 = max(x1, x)
        x2 = min(x2, x + width_minus_padding)
        canvas_add(Color(*selection_color, group='selection'))
        canvas_add(RoundedRectangle(
            pos=(x1, pos[1]), size=(x2 - x1, size[1]), group='selection'))

    # def set_colour(self, wid, colour):
    #     self.foreground_color = colour

    def on_text_colour(self, wid, colour):
        self.text_colour_instruction.rgba = colour
        self.foreground_color = self.text_colour

    def on_focus(self, wid, focus):
        #  simple enough
        self.show_trim = focus

