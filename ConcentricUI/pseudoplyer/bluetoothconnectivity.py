from kivy import platform

from ConcentricUI.utilities.runinthread import run_in_thread

if platform == 'android':
    from jnius import autoclass
    BluetoothAdapter = autoclass('android.bt.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bt.BluetoothDevice')
    BluetoothSocket = autoclass('android.bt.BluetoothSocket')
    IOException = autoclass('java.io.IOException')
    UUID = autoclass('java.util.UUID')
elif platform == 'win':
    pass
    import bluetooth


class AndroidBluetoothConnectivity(object):

    def get_socket_stream_list(self):
        paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        address_name_list = [(device.getAddress(), device.getName()) for device in paired_devices]
        print('5555555555555555555555555555555555555555555', address_name_list)
        return address_name_list

    def set_socket_stream(self, address):

        if not address:
            self.recv_stream, self.send_stream = None, None
            print('Bluetooth connection removed')
            return

        device = BluetoothAdapter.getDefaultAdapter().getRemoteDevice(address)
        socket = device.createRfcommSocketToServiceRecord(
            UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
        recv_stream = socket.getInputStream()
        send_stream = socket.getOutputStream()

        socket.connect()
        self.recv_stream, self.send_stream = recv_stream, send_stream
        self.last_paired_device_address = address

    def send_data(self, data):

        if self.send_stream:
            try:
                self.send_stream.write(data)
                self.send_stream.flush()
                return True
            except:
                try:
                    self.set_socket_stream(address=self.last_paired_device_address)
                    self.send_stream.write(data)
                    self.send_stream.flush()
                    print(':)')
                    return True
                except Exception as e:
                    print(':(', e)
                    return False

        else:
            Warning("No send stream set up. {} not sent".format(data))
            return False

    #  https://stackoverflow.com/questions/29719898/how-to-convert-android-bluetooth-socket-inputstream-to-python-string-in-kivy
    @run_in_thread
    def receive_data(self):
        global RECEIVE_THREAD_RUNNING
        RECEIVE_THREAD_RUNNING = True
        while True:
            if not RECEIVE_THREAD_RUNNING:
                break
            if self.recv_stream.available():
                try:
                    data = self.recv_stream.readLine()
                    self.do_on_data(data)
                # except IOException as e:
                #     print("IOException: ", e.message)
                # except JavaException as e:
                #     print("JavaException: ", e.message)
                except:
                    print("Misc error ... ")

    def do_on_data(self, data):
        print('ANDROID RECEIVED:', data)


class WindowsBluetoothConnectivity(object):

    def get_socket_stream_list(self):

        paired_devices = bluetooth.discover_devices(lookup_names=True)

        return paired_devices

    def set_socket_stream(self, address, unset=False):

        if not address:
            if self.send_stream:
                self.send_stream.close()
            self.recv_stream, self.send_stream = None, None
            print('Bluetooth connection removed')
            return
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        try:
            socket.connect((address, 1))
        except OSError as e:
            print('excepted!!', e)
            socket.close()
            return

        self.send_stream = socket

    def send_data(self, data):
        if self.send_stream:
            self.send_stream.send(bytes(str(data), 'UTF-8'))
        else:
            Warning("No send stream set up. {} not sent".format(data))



if platform == 'android':
    device_connectivity = AndroidBluetoothConnectivity
elif platform == 'win':
    device_connectivity = WindowsBluetoothConnectivity


class BluetoothConnectivity(device_connectivity):

    def __init__(self):
        """ last_paired_device_address is used for resetting connection """
        self.last_paired_device_address = None
        self.recv_stream, self.send_stream = None, None

        global RECEIVE_THREAD_RUNNING
        RECEIVE_THREAD_RUNNING = None

    def connect(self, address=None):
        if address:
            self.set_socket_stream(address)
            self.receive_data()
        else:
            self.disconnect()

    def disconnect(self):
        global RECEIVE_THREAD_RUNNING
        RECEIVE_THREAD_RUNNING = False

        self.set_socket_stream(None)

    def reset(self):
        pattern_string = '0'
        if self.send_stream:
            self.send_stream.write('{}\n'.format(pattern_string))
            self.send_stream.flush()
