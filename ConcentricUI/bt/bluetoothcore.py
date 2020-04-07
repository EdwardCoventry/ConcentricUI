from time import sleep

from kivy import platform

from ConcentricUI.utilities.runinthread import run_in_thread

if platform == 'android':
    from jnius import autoclass
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    IOException = autoclass('java.io.IOException')
    UUID = autoclass('java.util.UUID')
elif platform == 'win':
    import bluetooth

#  just going to set this here for now..
#  if it polls too frequently it could be intensive??
RECEIVE_POLLING_FREQUENCY = 60 #/s
if RECEIVE_POLLING_FREQUENCY:
    RECEIVE_WAIT_TIME = 1/RECEIVE_POLLING_FREQUENCY
else:
    RECEIVE_WAIT_TIME = 0

# CONNECT_POLLING_FREQUENCY = 2 #/s
# if CONNECT_POLLING_FREQUENCY:
#     CONNECT_WAIT_TIME = 1/CONNECT_POLLING_FREQUENCY
# else:
#     CONNECT_WAIT_TIME = 0

CONNECT_WAIT_TIME = 2

#  int_to_bytes and bytes_to_int are for windows bluetooth
def int_to_bytes(i: int, *, signed: bool = False) -> bytes:
    length = ((i + ((i * signed) < 0)).bit_length() + 7 + signed) // 8
    return i.to_bytes(length, byteorder='big', signed=signed)

def bytes_to_int(b: bytes, *, signed: bool = False) -> int:
    return int.from_bytes(b, byteorder='big', signed=signed)

class AndroidBluetoothConnectivity(object):

    def get_paired_devices(self):
        paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        address_name_list = [(device.getAddress(), device.getName()) for device in paired_devices]
        self.paired_devices = dict(address_name_list)
        return address_name_list

    def close_streams(self):
        if self.send_stream:
            self.send_stream.close()
        if self.recv_stream:
            self.recv_stream.close()
        self.recv_stream, self.send_stream = None, None

    def open_streams(self, address):

        if not address:
            raise Exception('No address given')

        device = BluetoothAdapter.getDefaultAdapter().getRemoteDevice(address)
        socket = device.createRfcommSocketToServiceRecord(
            UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
        recv_stream = socket.getInputStream()
        send_stream = socket.getOutputStream()
        try:
            socket.connect()
            print('________CONNECTED_______')

        except Exception as e:
            print('was not able to connect because {}'.format(e))
            return False

        self.recv_stream, self.send_stream = recv_stream, send_stream
        self.last_paired_device_address = address

        if recv_stream and send_stream:
            return True
        else:
            return False

    def send_byte(self, data):

        #print('ccccccccccc')

        if self.send_stream:
            #print('ddddd', data)
            self.send_stream.write(data)
            self.send_stream.flush()
            return True
        else:
            Warning("No send stream set up. {} not sent".format(data))
            return False

    def read_byte(self):
        if self.recv_stream.available():
            return self.recv_stream.read()
        else:
            return None

class WindowsBluetoothConnectivity(object):

    def get_paired_devices(self):
        paired_devices = bluetooth.discover_devices(lookup_names=True)


        if not paired_devices:
            paired_devices = [('hey' + str(x), str(x)+'.') for x in range(12)]

        self.paired_devices = dict(paired_devices)
        return paired_devices

    def close_streams(self):
        if self.send_stream:
            self.send_stream.close()
        if self.recv_stream:
            self.recv_stream.close()
        self.recv_stream, self.send_stream = None, None

    def open_streams(self, address):

        if not address:
            raise Exception('No address given')

        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        #try:
        #socket.connect((address, 1))
        port = 1
        #socket.bind(("", port))
        #socket.listen(2)
        socket.connect((address, port))

        # except OSError as e:
        #     print('excepted!!', e)
        #     socket.close()
        #     return

        self.send_stream = socket
        #self.recv_stream = client_sock
        self.last_paired_device_address = address

        if socket:
            return True
        else:
            return False

    def send_byte(self, data):
        if self.send_stream:
            self.send_stream.send(int_to_bytes(data))
        else:
            Warning("No send stream set up. {} not sent".format(data))

    def read_byte(self):
        data = self.send_stream.recv(1)
        if len(data):
            return data
        else:
            return None


if platform == 'android':
    device_bluetooth_core = AndroidBluetoothConnectivity
elif platform == 'win':
    device_bluetooth_core = WindowsBluetoothConnectivity


class BluetoothCore(device_bluetooth_core):

    def __init__(self, service=None):
        """ last_paired_device_address is used for resetting connection """
        self.paired_device_name = None
        self.paired_devices = None
        self._last_paired_device_address = None
        self.recv_stream, self.send_stream = None, None

        self.on_receive_byte = None

        self.flag_functions = {}
        self.active_flag_function = None
        self.argument_buffer = []
        self.required_argument_count = None
        self.multibyte_processing = None

        global RECEIVE_THREAD_RUNNING
        RECEIVE_THREAD_RUNNING = None

        global POLL_CONNECTION
        POLL_CONNECTION = False

        super(BluetoothCore, self).__init__()

    def get_paired_devices(self):
        return super(BluetoothCore, self).get_paired_devices()

    def close_streams(self):
        super(BluetoothCore, self).close_streams()

    def open_streams(self, address):
        return super(BluetoothCore, self).open_streams(address)

    def send_byte(self, data):

        print('@@@@@@@>>>>>', data)

        super(BluetoothCore, self).send_byte(data)

    def read_byte(self):
        return super(BluetoothCore, self).read_byte()

    def connect(self, address=None):
        if address:

            connection = self.open_streams(address)

            if connection:

                global POLL_CONNECTION
                POLL_CONNECTION = False
                self.successful_connection(address)
                self.run_read()
            else:
                print("couldnt connect to address {}".format(address))

        else:
            raise Exception("No address provided ... so how exactly should this program know what to connect to")

    def successful_connection(self, address):
        if self.paired_devices:
            self.paired_device_name = self.paired_devices[address]
            print('you are connected to device {}'.format(self.paired_device_name))

    @run_in_thread
    def run_read(self):
        global RECEIVE_THREAD_RUNNING
        while True:
            if RECEIVE_THREAD_RUNNING:
                byte = self.read_byte()
                if byte is not None:
                    self.process_byte(byte)
                sleep(RECEIVE_WAIT_TIME)
            else:
                break

    def disconnect(self):
        #  close thread
        global RECEIVE_THREAD_RUNNING
        RECEIVE_THREAD_RUNNING = False
        #  close streams
        self.close_streams()

    def reset(self):
        if self.send_stream:
            self.send_stream.flush()

    def process_byte(self, byte):

        """
        actually i'm only going to implement single byte sending for now.. so the maximum value of each arg is 255
        you can have multiple arguments though
        so for example from the compass to the device we could send a pos/neg direction flag, and a bearing
        """

        #  if there is already a flag set then do the following
        if self.active_flag_function:
            #  here we are building the args as bytes
            self.argument_buffer.append(byte)
            #  if we have all the required arg bytes
            if len(self.argument_buffer) == self.required_argument_count:
                #  make a copy of the function and arguments
                funct = self.active_flag_function
                args = self.argument_buffer
                #  clear the class instance reference to the function and arguments
                self.active_flag_function = None
                self.argument_buffer = None
                self.required_argument_count = None
                self.multibyte_processing = None
                #  ok actually run the function
                funct(*args)
        else:
            self.set_flag(byte)

    def set_flag(self, byte):
        flag = self.flag_functions.get(byte)
        self.active_flag_function = flag['function']
        self.required_argument_count = flag['count']
        self.multibyte_processing = True if flag['byte mode'] == 'multi' else False
        #  we set argument_buffer to none after the execution of the last function,
        #  we now we reinitialise it as a blank list
        self.argument_buffer = []

    @run_in_thread
    def poll_connection(self, address):

        global POLL_CONNECTION

        if POLL_CONNECTION:
            print('CONNECTION ALREADY POLLING')
            return False

        POLL_CONNECTION = True

        while True:

            #print('POLL CONNECTION', POLL_CONNECTION, address)

            if not POLL_CONNECTION:
                break

            self.connect(address=address)

    def stop_poll_connection(self):

        global POLL_CONNECTION
        POLL_CONNECTION = False

    def restart_poll_connection(self, address):
        self.stop_poll_connection()
        self.poll_connection(address)