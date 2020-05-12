
from kivy.app import App
from kivy.clock import mainthread
from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.widget import Widget

from ConcentricUI.bt.bluetoothbuttons import PairedDevicesPopup


class BluetoothProxy(Widget):

    connected = BooleanProperty(False)

    paired_devices = ListProperty()

    def on_paired_devices(self, wid, devices):
        App.get_running_app().paired_devices = devices

    def __init__(self, service):



        self.paired_devices_popup = PairedDevicesPopup()


        self.service = service

        super(BluetoothProxy, self).__init__()

    def connect(self, address):
        self.service.function('bluetooth.connect', args=[address])

    def disconnect(self):
        self.service.function('bluetooth.disconnect', args=[])

    def poll_connection(self, address):
        self.service.function('bluetooth.poll_connection', args=[address])

    def stop_poll_connection(self):
        self.service.function('bluetooth.stop_poll_connection', args=[])

    def get_paired_devices(self):
        self.service.return_function('bluetooth.get_paired_devices', 'bluetooth.paired_devices', args=[])

    def connect_bluetooth(self, retry=True):

        paired_device = App.get_running_app().config['bt']['paired device']

        if paired_device not in ('disconnect', 'disconnected'):
            address, name = eval(paired_device)
            App.get_running_app().bluetooth_button.text = name

            if retry:
                self.poll_connection(address=address)
            else:
                self.connect(address=address)
        else:
            App.get_running_app().bluetooth_button.text = 'disconnected'
            App.get_running_app().bluetooth.connect(address=None)

    @mainthread
    def set_bluetooth_button(self, device_name=None):

        paired_devices_button = App.get_running_app().bluetooth_button
        paired_devices_button.text = device_name
        if device_name:
            paired_devices_button.text = ''
            paired_devices_button.button_source = 'bluetooth_on'
        else:
            paired_devices_button.text = ''
            paired_devices_button.button_source = 'bluetooth_off'

    def send_last_paired_device(self):

        device = App.get_running_app().config.get('bt', 'paired device')
        if device in ('disconnect', 'disconnected'):
            self.disconnect()
            return None
        else:
            address, name = eval(device)
            App.get_running_app().compass_service.function('bluetooth.poll_connection', args=[address])
            return address


    #  sending

    def queue_flag(self, flag):
        self.service.function('bluetooth.queue_flag', args=[flag])


    def queue_byte(self, byte_list, prepend_flag=None):
        #self.service.function('bluetooth.queue_byte', args=[byte_list, prepend_flag])
        self.service.function('bluetooth.queue_byte', args=[byte_list], kwargs={'prepend_flag': prepend_flag})

    def queue_integer(self, integer, prepend_byte_count=False, prepend_flag=None):
        self.service.function('bluetooth.queue_integer', args=[integer],
                              kwargs={'prepend_byte_count': prepend_byte_count,
                                      'prepend_flag': prepend_flag})
