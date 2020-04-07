from queue import Queue

class ClearableQueue(Queue):
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
