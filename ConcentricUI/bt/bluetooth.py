from time import time, sleep

from ConcentricUI.bt.bluetoothcore import BluetoothCore
from ConcentricUI.bt.byteprocessing import ByteProcessing
from ConcentricUI.bt.bluetoothwithqueue import BluetoothQueue

from ConcentricUI.bt import bluetoothflags as flags

from ConcentricUI.utilities.runinthread import run_in_thread

#from service import self.servicecommon

CONNECTION_CHECK_ASK_TIME = 1
TIMEOUT = 2

class Bluetooth(BluetoothCore, ByteProcessing, BluetoothQueue):

    def __init__(self, service=None):
        if service:
            self.service = service
        super(Bluetooth, self).__init__()

        self.readied_bytes = {}

        self.connection_update_time = 0

    def disconnect(self):
        super().disconnect()
        self.servicecommon.osc.function('bluetooth.set_bluetooth_button', args=[])
        self.on_disconnection()

    def autoconnect(self):
        self.servicecommon.osc.function('bluetooth.send_last_paired_device')
        #  this will get the last paired device, which will trigger polling to connect to that device

    def successful_connection(self, address):
        super(Bluetooth, self).successful_connection(address)
        self.set_paired_devices_button()

    def set_paired_devices_button(self):

        paired_device_name = self.paired_device_name if self.paired_device_name else 'auto'

        self.servicecommon.osc.function('bluetooth.set_bluetooth_button', args=[paired_device_name])

    def on_connection(self):
        self.start_regularly_checking_connection()
        print('connected')
        self.servicecommon.osc.function('bluetooth.on_connection')


    def on_disconnection(self):
        self.stop_regularly_checking_connection()
        print('disconnected')
        self.servicecommon.osc.function('bluetooth.on_disconnection')


    def on_apparent_disconnection(self):
        global CHECK_CONNECTION
        if not CHECK_CONNECTION:
            return
        print('ITS APPARENT THAT THERE IS NOT A CONNECTION!!!')
        self.disconnect()
        #  you would have had to have connected for last_paired_device_address to be set, so just repoll to that address
        self.poll_connection(self.last_paired_device_address)
        #self.connect(self.last_paired_device_address)

    @run_in_thread
    def start_regularly_checking_connection(self):
        global CHECK_CONNECTION
        CHECK_CONNECTION = True
        while CHECK_CONNECTION:
            self.ask_connection()
            sleep(CONNECTION_CHECK_ASK_TIME)

    @staticmethod
    def stop_regularly_checking_connection():
        global CHECK_CONNECTION
        CHECK_CONNECTION = False

    def ask_connection(self):
        self.queue_byte(flags.BLUETOOTH.ASK)
        self.run_time_out(self.connection_update_time)

    def answered_connection(self):
        self.connection_update_time = time()

    @run_in_thread
    def run_time_out(self, last_connection_update_time):
        sleep(TIMEOUT)
        if last_connection_update_time == self.connection_update_time:
            self.on_apparent_disconnection()

    def send_readied_bytes(self):

        total_bytes = []

        for bytes in self.readied_bytes.values():
            total_bytes.extend(bytes)

        print('this is just a test. but bytes to be sent are', bytes)

        self.queue_byte(bytes, prepend_flag=None)

    def update_readied_bytes(self, key, bytes):
        print('updating', key, 'to', bytes)
        self.readied_bytes[key] = bytes