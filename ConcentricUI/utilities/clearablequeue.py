from queue import Queue
from threading import Lock


class LockableQueue(Queue):

    def __init__(self, *args, **kwargs):

        self.lock = Lock

        super(LockableQueue, self).__init__(*args, **kwargs)

    # def lock(self):
    #     self.queue_lock.acquire()
    #
    # def unlock(self):
    #     self.queue_lock.release()

class ClearableQueue(LockableQueue):

    def clear(self):
        try:
            while True:
                self.get_nowait()
        except:
            pass

class DumpableQueue(ClearableQueue):
    def dump(self):
        queue_dump = []
        try:
            while True:
                queue_dump.append(self.get_nowait())
        except:
            pass
        return queue_dump
