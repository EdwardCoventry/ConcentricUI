from ConcentricUI.bt.bluetoothcore import BluetoothCore
from ConcentricUI.bt.byteprocessing import ByteProcessing
from ConcentricUI.bt.bluetoothwithqueue import BluetoothQueue

from service import servicecommon


class Bluetooth(BluetoothCore, ByteProcessing, BluetoothQueue):


    def __init__(self, service=None):
        if service:
            self.service = service
        super(Bluetooth, self).__init__()
        #self._last_paired_device = None

    def autoconnect(self):
        servicecommon.osc.function('bluetooth.send_last_paired_device')
        #  this will get the last paired device, which will trigger polling to connect to that device

    def successful_connection(self, address):
        super(Bluetooth, self).successful_connection(address)
        self.set_paired_devices_button()

    def set_paired_devices_button(self):

        paired_device_name = self.paired_device_name if self.paired_device_name else 'auto'

        servicecommon.osc.function('bluetooth.set_bluetooth_button', args=[paired_device_name])