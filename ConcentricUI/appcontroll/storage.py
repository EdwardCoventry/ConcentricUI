from os import mkdir, path

from kivy.app import App
from kivy.storage.dictstore import DictStore

class ExtendedDictStore(DictStore):

    def sync(self):
        self._is_changed = True
        self.store_sync()

    def load(self):
        self.store_load()

class BackupDictStore(ExtendedDictStore):

    def __init__(self, filename, original=None, **kwargs):
        self.filename = filename
        self._data = original._data

        self._is_changed = True
        self.store_sync()

        super(DictStore, self).__init__(**kwargs)

class Storage(object):

    def __init__(self):

        if App.get_running_app():
            #  first try and get user_data_dir from the app
            self.user_data_dir = App.get_running_app().user_data_dir
        else:
            #  if that fails then youre in the service. get user_data_dir from service common
            from service import servicecommon
            self.user_data_dir = servicecommon.user_data_dir

        self.store_references = {}

    def get_store_reference(self, store_name):
        if store_name in self.store_references:
            return self.store_references[store_name]
        else:
            store, backup_store = self.get_store_with_backup(store_name)
            self.store_references[store_name] = store

        # if not store.count():
        #     print("its empty!")
        #     if store_name == 'quick_save':
        #         #  set defaults
        #         store['last'] = {'gps_location': (51.471667, -0.071861)}

        return store


    def get_store(self, store_name, subfolder='stores', as_backup=False, from_backup=False):
    
    
        print('GET STORE NAME', store_name, subfolder)
    
    
        #  remove .pydict
        if store_name.endswith('.pydict'):
            store_name.strip('.pydict')
    
        #  add _backup if its a backup
        if from_backup:
            store_name += '_backup'
    
        #  always add .pydict (as it was removed if it existed)
        store_name += '.pydict'
    
        if not subfolder:
            #  get the path (straightforward)
            store_path = path.join(self.user_data_dir, store_name)
        else:
            #  get the subfolder's path
            folder_path = path.join(self.user_data_dir, subfolder)
            try:
                #  try to make the subfolder
                mkdir(folder_path)
            except:
                #  if it already exists then simply print the line bellow and do nothing else
                print('i guess its already made')
    
            #  get the store's path
            store_path = path.join(folder_path, store_name)
    
        #  return the correct storage type
        if as_backup is True:
            #  if as_backup is simply True, then try to get the store with the same name
            #  this is a little inefficient but who cares really
            store = self.get_store(store_name, subfolder)
            return BackupDictStore(store_path, store)
        elif as_backup:
            #  if as_backup is specified then backup from the specified store
            return BackupDictStore(store_path, as_backup)
        else:  # if not as backup...., just open a normal store
            return ExtendedDictStore(store_path)
    
    
    def get_store_with_backup(self, store_name, subfolder=None):
        # this wont get it again if it changed... but why would it ever change
        try:
            #  this is if it works:
            #  get the store, and back it up as the backup store
            store = self.get_store(store_name, subfolder)
            backup_store = self.get_store(store_name, subfolder, from_backup=True, as_backup=store)
    
        except:
            #  fixme except the specific error
            #  if it doesnt work it is most likely because the store was corrupt
            #  in this case set the store to be the backup store
            backup_store = self.get_store(store_name, subfolder, from_backup=True, as_backup=False)
            store = self.get_store(store_name, subfolder, from_backup=False, as_backup=backup_store)
    
        return store, backup_store
