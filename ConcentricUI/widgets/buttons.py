
from kivy.app import App
from kivy.clock import mainthread

from ConcentricUI.circle.circlebutton import CircleButton

from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

class ModeButton(CircleButton):
    image_source = StringProperty()

    state_list_index = 0
    button_state = StringProperty()

    @staticmethod
    def get_button_state(clss):
        #  fixme i should make the function generate with the class already added
        index = clss.state_list_index
        return clss.state_list[index]

    @staticmethod
    def get_button_state_list_index(clss):
        #  fixme i should make the function generate with the class already added
        index = clss.state_list_index
        return index

    def __init__(self, **kwargs):
        super(ModeButton, self).__init__(**kwargs)
        self.set_button()

    def set_button(self, state=None, *args):

        if state:
            index = self.state_list.index(state)
            self.__class__.state_list_index = index
        else:
            index = self.__class__.state_list_index

        self.button_state = self.state_list[index]
        self.master_colour = self.colour_list[index]
        self.image_source = self.image_list[index]

    def increment_class_index(self, *args):
        #  use class variable
        self.__class__.state_list_index += 1
        if self.__class__.state_list_index == len(self.state_list):
            self.__class__.state_list_index = 0
        self.set_button()

    def on_release(self, *args):
        self.increment_class_index()

class OpenScreenButton(CircleButton):

    screen = None
    button_text = None

    def __init__(self, **kwargs):
        if self.button_text:
            self.text = self.button_text
        super(OpenScreenButton, self).__init__(**kwargs)
        self.font_size_hint = 0.7


    def on_release(self, *args):
        App.get_running_app().root.current = self.screen


class HomeButton(OpenScreenButton):
    def __init__(self, **kwargs):
        self.screen = 'Home Screen'
        self.button_source = 'home'
        super(HomeButton, self).__init__(**kwargs)

class ButtonsBox(BoxLayout):

    buttons = ListProperty()

    buttons_count = 5

    button_classes = ListProperty()

    def __init__(self, mode=None, **kwargs):

        self.mode = mode

        super(ButtonsBox, self).__init__(**kwargs)

        self.bind(pos=self.set_buttons_set_pos)

    def set_buttons_set_pos(self, wid, pos):
        self.pos = pos
        for button in self.buttons:
            button.pos = pos

    # def set_buttons_set_size(self, wid, size):
    #     if self.button_set:
    #         self.button_set.size = size

    def on_button_classes(self):

        for i, (button, clss) in enumerate(zip(self.buttons, self.button_classes)):
            if not isinstance(button, clss):
                new_button = clss()
                button = new_button
                self.buttons[i] = button

    def add_buttons_from_class_list(self, class_list):

        for clss in class_list:
            button = clss()
            self.buttons.append(button)
            self.add_widget(button)

class ScrollableButtonsBox(ScrollView):

    buttons_count = 5

    orientation = 'horizontal'

    def __init__(self, mode=None, **kwargs):
        super(ScrollableButtonsBox, self).__init__(**kwargs)

        self.scroll_type = ['content']

        self.bar_color = [0,0,0,0]
        self.bar_inactive_color = [0,0,0,0]

        self.mode = mode

        self.do_scroll_x = True
        self.do_scroll_y = False

        total_buttons_box_width = self.get_total_buttons_box_width(self.width)

        self.buttons_box = ButtonsBox(size=(total_buttons_box_width, self.height),
                                      pos=self.pos,
                                      mode=mode,
                                      size_hint=(None, None))

        self.buttons_box.bind(minimum_width=self.buttons_box.setter('width'))

        self.add_widget(self.buttons_box)

        self.bind(size=self.set_buttons_box_size)

        self.buttons_box.orientation = self.orientation

        self.buttons_box.add_buttons_from_class_list(self.buttons_list)

    def set_buttons_box_size(self, wid, size):
        self.buttons_box.size = self.get_total_buttons_box_width(size[0]), size[1]

    def get_total_buttons_box_width(self, width):
        total_buttons_box_width = width / self.buttons_count * len(self.buttons_list)
        return total_buttons_box_width


class ButtonsBoxHolder(AnchorLayout):

    button_set = ObjectProperty()

    mode = StringProperty()

    def __init__(self, **kwargs):
        super(ButtonsBoxHolder, self).__init__(**kwargs)

        self.anchor_y = 'top'

        self.bind(pos=self.set_buttons_set_pos,
                  size=self.set_buttons_set_size)

        if self.mode:
            self.switch_buttons_mode(None, self.mode)

        #Clock.schedule_once(self.bind_buttons)

        self.bind(mode=self.switch_buttons_mode)


    def set_buttons_set_pos(self, wid, pos):
        if self.button_set:
            self.button_set.pos = pos

    def set_buttons_set_size(self, wid, size):
        if self.button_set:
            self.button_set.size = size

    @mainthread
    def switch_buttons_mode(self, wid, mode):

        print('mode!', mode, self.button_set.mode if self.button_set else None)

        if self.button_set and self.button_set.mode == mode:
            return

        if mode in self.buttons_dictionary:
            #  initialise the buttons
            button_set = self.buttons_dictionary[mode](mode=mode)
        else:
            raise Exception("Button mode {} not recognised".format(mode))

        if self.button_set:

            self.remove_widget(self.button_set)

            self.button_set = button_set

            self.add_widget(self.button_set)
        else:

            self.button_set = button_set

            self.add_widget(self.button_set)

class BluetoothButton(CircleButton):

    def __init__(self, **kwargs):

        super(BluetoothButton, self).__init__(**kwargs)

        App.get_running_app().bluetooth_button = self

        #self.master_colour = '#B4D2E7'

        self.button_source = 'bluetooth_off'

        self.on_release = self.bluetooth_popup

    def bluetooth_popup(self, *args):
        App.get_running_app().bluetooth.stop_poll_connection()
        App.get_running_app().bluetooth.paired_devices_popup.get_devices_list()


class OpenSettingsButton(CircleButton):
    def __init__(self, **kwargs):
        super(OpenSettingsButton, self).__init__(**kwargs)
        self.button_source = "settings"

    def on_release(self, *args):
        App.get_running_app().open_settings()
