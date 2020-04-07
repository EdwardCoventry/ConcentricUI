from kivy.storage.dictstore import DictStore


class ExtendedDictStore(DictStore):

    def sync(self):
        self._is_changed = True
        self.store_sync()

    def load(self):
        self.store_load()
