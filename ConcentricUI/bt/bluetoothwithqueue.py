

from ConcentricUI.utilities.clearablequeue import ClearableQueue
from ConcentricUI.utilities.runinthread import run_in_thread

class BluetoothQueue(object):

    def __init__(self):
        #super(BluetoothWithQueue, self).__init__()

        self.queue = ClearableQueue()
        self.run_bluetooth_queue()

    def queue_byte(self, byte_list):

        if not type(byte_list) in (list, tuple):
            byte_list = [byte_list]

        for byte in byte_list:
            self.queue.put(byte)

    def queue_integer(self, integer=0, prepend_byte_count=False, prepend_flag=None):

        byte_list = self.process_integer(integer, prepend_byte_count)

        if prepend_flag is not None:
            byte_list = [prepend_flag] + byte_list

        self.queue_byte(byte_list)

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
