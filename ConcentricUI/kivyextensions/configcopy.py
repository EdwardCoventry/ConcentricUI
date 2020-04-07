from json import loads
from os import getenv, path
from time import time

from service import servicecommon

from kivy.storage.dictstore import DictStore

class ConfigCopy(DictStore):

    new_update_time = 0

    @staticmethod
    def update_update_time():
        return
        print('tttttttthis is great! update update time called.. lets hope it all works')
        ConfigCopy.new_update_time = time()

    def update_value(self, section_name, key, value):
        section = self.get(section_name)
        section[key] = value
        self.put(section_name, **section)
        #
        # print(section_name, key, value)
        #
        # print('oooooooo', self.getint(section_name, key))

        if section_name == 'polling':
            if key == 'ui':
                servicecommon.sensors.start_spatial_orientation_sender()

            elif key == 'phone':
                servicecommon.sensors.start_spatial_orientation_reader()


    def __init__(self, route_mode, user_data_dir):

        self.last_update_time = time()

        config_copy_file_name = '{}_copy.pydict'.format(route_mode)
        config_copy_path = path.join(user_data_dir, config_copy_file_name)

        super(ConfigCopy, self).__init__(config_copy_path)

        self.store_load()

        print('ooooooooooo', config_copy_path, dict(self._data))

    def get_from_type(self, section, key, key_type):

        # if ConfigCopy.new_update_time > self.last_update_time:
        #     print(
        #         '!!!!!!!!!!!!!!!!!!!!!!!!!!!!this is very very important because the config has just been updated!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #     self.last_update_time = ConfigCopy.new_update_time
        #     self.store_load()

        #print('vvvvvvvvv', self.store_get('polling'))

        value = self.store_get(section)[key]
        if key_type:
            return key_type(value)
        else:
            return value

    # def get(self, section, key):
    #     return self.get_from_type(section, key, key_type=None)

    def getint(self, section, key):
        return self.get_from_type(section, key, key_type=int)

    def getfloat(self, section, key):
        return self.get_from_type(section, key, key_type=float)

    def getstr(self, section, key):
        return self.get_from_type(section, key, key_type=str)

    def getbool(self, section, key):
        str_bool = self.get_from_type(section, key, key_type=str)

        if str_bool in ('1', True):
            return True
        else:
            return False
