from ConcentricUI.circle.circlebutton import CircleButton
from ConcentricUI.oblong.oblongbutton import OblongButton
from ConcentricUI.widgets.fullscreenpopup import FullScreenPopup
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, DictProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.utils import rgba



class PollConnectionButton(CircleButton):
    def __init__(self):
        self.text = 'poll'
        super().__init__()

    def on_release(self):
        App.get_running_app().bluetooth.connect_bluetooth(retry=True)

class ConnectButton(CircleButton):
    def __init__(self):
        self.text = 'con'
        super().__init__()

    def on_release(self):
        App.get_running_app().bluetooth.connect_bluetooth(retry=False)

class DisconnectButton(CircleButton):
    def __init__(self):
        self.text = 'dis'
        super().__init__()

    def on_release(self):
        App.get_running_app().bluetooth.stop_poll_connection()
        App.get_running_app().bluetooth.disconnect()

class ShowPairedDevicesButton(CircleButton):
    def __init__(self):
        self.text = 'pair'
        super().__init__()

    def on_release(self):
        App.get_running_app().bluetooth.stop_poll_connection()
        App.get_running_app().bluetooth.paired_devices_popup.get_devices_list()


class PairedDevicesPopupOption(OblongButton):
    popup = ObjectProperty()

    address = StringProperty()

    def __init__(self, **kwargs):
        super(PairedDevicesPopupOption, self).__init__(**kwargs)


    def set_paired_device(self, *args):

        App.get_running_app().config.set('bt', 'paired device', str((self.address, self.text)))
        App.get_running_app().save_config()


        App.get_running_app().bluetooth.poll_connection(self.address)

    def on_release(self, *args):
        self.set_paired_device()
        self.popup.save_and_close(self.address)

    def on_size(self, wid, size):
        Clock.schedule_once(self.set_font_size, 0)


class PairedDevicesPopup(FullScreenPopup):
    devices_dictionary = DictProperty()

    def __init__(self, **kwargs):

        super(PairedDevicesPopup, self).__init__(**kwargs)


        self.background_colour = rgba('#434359')


        self.devices_scroll_view = None
        self.devices_grid_layout = None

        #self.loading_message = Text(text='Loading Bluetooth Devices ...')

        #self.content.add_widget(self.loading_message)

    def get_devices_list(self):
        #  paired devices is a list of Bluetooth devices paired with the phone
        App.get_running_app().bluetooth.bind(paired_devices=self.set_values)
        App.get_running_app().bluetooth.get_paired_devices()
        if App.get_running_app().bluetooth.paired_devices:
            self.open()
        else:
            button = App.get_running_app().bluetooth_button
            #button.text = '...'
            button.button_source = 'bluetooth_mid'



    def fill_devices_scroll_view(self, *args):

        if self.devices_scroll_view:
            self.content.remove_widget(self.devices_scroll_view)

        try:
            self.content.remove_widget(self.loading_message)
        except:
            print('expected')

        self.devices_scroll_view = ScrollView(size=self.size,
                                              pos=self.pos)
        self.devices_grid_layout = GridLayout(size=self.size,
                                              pos=self.pos,
                                              padding=self.height/10,
                                              cols=1,
                                              size_hint_y=None)

        self.devices_grid_layout.bind(minimum_height=self.devices_grid_layout.setter('height'))
        #self.devices_grid_layout.bind(minimum_height=)


        self.devices_scroll_view.add_widget(self.devices_grid_layout)

        self.content.add_widget(self.devices_scroll_view)

        # button_width = self.width
        # button_height = self.height/5

        self.content.size = self.size

        for address, name in self.devices_dictionary.items():
            if not name:
                name = '-'
            button = PairedDevicesPopupOption(popup=self,
                                              content_pin=name,
                                              address=address,
                                              collision_layer='outer',
                                              height=self.height/1.5,
                                              size_hint_y=None)
            #  size=(button_width, button_height),
            # Clock.schedule_once(button.update_shape_list_size)
            # Clock.schedule_once(partial(button.initially_set_font_size, name))

            self.devices_grid_layout.add_widget(button)

    def set_values(self, *args):
        paired_devices = App.get_running_app().bluetooth.paired_devices
        App.get_running_app().bluetooth.unbind(paired_devices=self.set_values)
        self.devices_dictionary = dict(paired_devices)
        self.fill_devices_scroll_view()
        Clock.schedule_once(self.open)

    def save_and_close(self, address=None, *args):
        #App.get_running_app().bluetooth.poll_connection(address)
        super(PairedDevicesPopup, self).save_and_close(*args)

        button = App.get_running_app().bluetooth_button
        if button.button_source == 'bluetooth_mid':
            #button.text = ''
            button.button_source = 'bluetooth_off'

    def set_size(self, wid, size):
        self.size = size

    def set_pos(self, wid, pos):
        self.pos = pos