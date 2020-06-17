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
# RECEIVE_POLLING_FREQUENCY = 60 #/s
# if RECEIVE_POLLING_FREQUENCY:
#     RECEIVE_WAIT_TIME = 1/RECEIVE_POLLING_FREQUENCY
# else:
#     RECEIVE_WAIT_TIME = 0

# CONNECT_POLLING_FREQUENCY = 2 #/s
# if CONNECT_POLLING_FREQUENCY:
#     CONNECT_WAIT_TIME = 1/CONNECT_POLLING_FREQUENCY
# else:
#     CONNECT_WAIT_TIME = 0

CONNECT_WAIT_TIME = 0.5
POLL_CONNECTION = False
RECEIVE_THREAD_RUNNING = False

#  int_to_bytes and bytes_to_int are for windows bluetooth
def int_to_bytes(i: int, *, signed: bool = False) -> bytes:
    length = ((i + ((i * signed) < 0)).bit_length() + 7 + signed) // 8
    if not length:
        length = 1
    #print('length!!!!!', length, 'for', i)
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

    # def get_mac_address(self):
    #     dummy_address = "00:37:34:174:118:109"
    #     return dummy_address


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
        #print('_____________THERE IS PROBABLY A BIG WAIT HERE_____________')
        #socket.settimeout(0.1)
        #socket.settimeout(0.5)
        socket.connect((address, port))
        #socket.settimeout(1000)
        #socket.settimeout(0)
        #print('_____________WAIT OVER_____________')
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
        #data = self.send_stream.recv(1)

        try:
            data = self.send_stream.recv(1)
        except OSError as e:
            print('BT ERROR:', e)
            return None
        if len(data):
            return int.from_bytes(data, 'little')
        else:
            return None

    def read_int(self):
        try:
            byte = self.send_stream.recv(1)
            bytes_count = int.from_bytes(byte, 'little')
            multi_bytes = self.send_stream.recv(bytes_count)
            integer = int.from_bytes(multi_bytes, 'little')
            print('INTEGER:', integer)
            return integer
        except OSError as e:
            print('BT ERROR:', e)
            return None

    # def get_mac_address(self):
    #     # easy!
    #     return getmac.get_mac_address()


if platform == 'android':
    device_bluetooth_core = AndroidBluetoothConnectivity
elif platform == 'win':
    device_bluetooth_core = WindowsBluetoothConnectivity


class BluetoothCore(device_bluetooth_core):

    flag_functions = {}

    def __init__(self, service=None):
        """ last_paired_device_address is used for resetting connection """
        self.paired_device_name = None
        self.paired_devices = None
        self.last_paired_device_address = None
        self.recv_stream, self.send_stream = None, None

        self.on_receive_byte = None

        #self.flag_functions = {}
        self.active_flag_function = None
        self.argument_buffer = []
        self.required_argument_count = None
        self.multibyte_processing = None

        #global RECEIVE_THREAD_RUNNING
        #RECEIVE_THREAD_RUNNING = None

        #global POLL_CONNECTION
        #POLL_CONNECTION = False

        super(BluetoothCore, self).__init__()

    def get_paired_devices(self):
        return super(BluetoothCore, self).get_paired_devices()

    def close_streams(self):
        super(BluetoothCore, self).close_streams()

    def open_streams(self, address):
        return super(BluetoothCore, self).open_streams(address)

    def send_byte(self, data):
        # if not data == 15:
        #     print('********>', data)
        super(BluetoothCore, self).send_byte(data)

    def read_byte(self):
        return super(BluetoothCore, self).read_byte()

    def connect(self, address=None):
        error = None
        if address:
            #connection = self.open_streams(address)

            try:
                #print('try this')
                self.close_streams()
                connection = self.open_streams(address)
                #print('how did it go?')
            except Exception as e:
                error = e
                connection = False

            if connection:
                global POLL_CONNECTION
                POLL_CONNECTION = False
                self.successful_connection(address)
                self.run_read()
                self.on_connection()
            else:
                if error:
                    pass
                    #print("couldnt connect to address {} because of error {}".format(address, error))
                else:
                    pass
                    #print("couldnt connect to address {}".format(address))

        else:
            raise Exception("No address provided ... so how exactly should this program know what to connect to")

    def successful_connection(self, address):
        self.last_paired_device_address = address
        if self.paired_devices:
            self.paired_device_name = self.paired_devices[address]
            print('you are connected to device {}'.format(self.paired_device_name))

    @run_in_thread
    def run_read(self):
        global RECEIVE_THREAD_RUNNING
        if RECEIVE_THREAD_RUNNING:
            return
        RECEIVE_THREAD_RUNNING = True
        while True:
            if RECEIVE_THREAD_RUNNING:
                byte = self.read_byte()
                if byte is not None:
                    self.process_byte(byte)
            else:
                break

    # def process_byte(self, byte):
    #     print('BYTE {} UNPROCESSED. this method should be overwritten'.format(byte))

    def disconnect(self):
        #  close thread
        global RECEIVE_THREAD_RUNNING
        RECEIVE_THREAD_RUNNING = False

        print('CLOSING DOWN RECEIVE_THREAD')

        #  close streams
        self.close_streams()

    def reset(self):
        if self.send_stream:
            self.send_stream.flush()

    @run_in_thread
    def poll_connection(self, address):

        if self.send_stream:
            print('disconnecting so it can poll')
            self.disconnect()

        global POLL_CONNECTION

        if POLL_CONNECTION:
            print('CONNECTION ALREADY POLLING')
            return False

        POLL_CONNECTION = True

        while POLL_CONNECTION:

            print('POLL CONNECTION', POLL_CONNECTION, address, 'hey hey')

            # if not POLL_CONNECTION:
            #     break
            self.connect(address=address)
            #print('connection attempted, sleeping for', CONNECT_WAIT_TIME)
            sleep(CONNECT_WAIT_TIME)
            #print('ok wakey wakey. POLL_CONNECTION =', POLL_CONNECTION)

    def stop_poll_connection(self):

        global POLL_CONNECTION
        POLL_CONNECTION = False

    def restart_poll_connection(self, address):
        self.stop_poll_connection()
        self.poll_connection(address)
