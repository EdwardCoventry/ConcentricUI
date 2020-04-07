from json import loads
from os import getenv, path
from time import time

from kivy.config import ConfigParser

class ConfigWrapper(ConfigParser):
    # def __init__(self):
    #     user_data_dir = getenv('PYTHON_SERVICE_ARGUMENT')
    #     self.config_copy_path = path.join(user_data_dir, 'config_copy.pydict')
    #     self.store = DictStore(self.config_copy_path)

    def __init__(self, route_mode):

        self.directory = getenv('PYTHON_SERVICE_ARGUMENT')

        config_name = '{}'.format(route_mode)
        config_file_name = '{}.ini'.format(config_name)
        config_file_path = path.join(self.directory, config_file_name)
        #self.read(config_file_path)

        #ConfigParser(name=config_name)
        # user_data_dir = loads(getenv('PYTHON_SERVICE_ARGUMENT'))[0]
        #
        # config_copy_file_name = '{}_config_copy.pydict'.format(route_mode)
        # config_copy_path = path.join(user_data_dir, config_copy_file_name)

        super(ConfigWrapper, self).__init__(name=config_name) #config_copy_path)
        #
        # super.__init__(config_copy_path)
        # self.store = DictStore(self.config_copy_path)

    # def getint(self, section, key):
    #     return int(self.get(section, key))
    #
    # def getfloat(self, section, key):
    #     return float(self.get(section, key))
    #
    # def getstr(self, section, key):
    #     return str(self.get(section, key))
    #
    # def getbool(self, section, key):
    #     str_bool = self.get(section, key)
    #
    #     if str_bool in ('1', True):
    #         return True
    #     else:
    #         return False
