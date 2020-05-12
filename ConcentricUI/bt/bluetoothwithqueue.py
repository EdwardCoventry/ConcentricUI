
from ConcentricUI.utilities.clearablequeue import ClearableQueue
from ConcentricUI.utilities.runinthread import run_in_thread

class BluetoothQueue(object):

    def __init__(self):
        #super(BluetoothWithQueue, self).__init__()

        self.queue = ClearableQueue()
        self.run_bluetooth_queue()

    def queue_flag(self, flag):
        self.queue_byte(flag)

    def queue_byte(self, byte_list, prepend_flag=None):

        if not (byte_list or prepend_flag):
            print('not queuing anything..... {} {]'.format(byte_list, prepend_flag))
            return

        if not byte_list or byte_list == [None]:
            byte_list = []
        elif not type(byte_list) in (list, tuple):
            byte_list = [byte_list]

        if prepend_flag is not None:
            byte_list = [prepend_flag] + byte_list

        with self.queue.lock():
            for byte in byte_list:
                self.queue.put(byte)

    def queue_integer(self, integer=0, prepend_byte_count=False, prepend_flag=None):

        byte_list = self.process_integer(integer, prepend_byte_count)

        self.queue_byte(byte_list, prepend_flag=prepend_flag)

    # def send_integer(self, integer=0, prepend_byte_count=False):
    #
    #     byte_list = self.process_integer(integer, prepend_byte_count)
    #     for byte in byte_list:
    #         self.send_byte(byte)


    @run_in_thread
    def run_bluetooth_queue(self):
        while True:
            byte = self.queue.get()
            self.send_byte(byte)
