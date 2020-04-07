
import os

from kivy.config import ConfigParser
from kivy.compat import PY2, string_types

try:
    from ConfigParser import ConfigParser as PythonConfigParser
except ImportError:
    from configparser import RawConfigParser as PythonConfigParser


def read(self, filenames, encoding=None):
    """Read and parse a filename or an iterable of filenames.

    Files that cannot be opened are silently ignored; this is
    designed so that you can specify an iterable of potential
    configuration file locations (e.g. current directory, user's
    home directory, systemwide directory), and all existing
    configuration files in the iterable will be read.  A single
    filename may also be given.

    Return list of successfully read files.
    """
    if isinstance(filenames, (str, bytes, os.PathLike)):
        filenames = [filenames]
    read_ok = []
    for filename in filenames:
        try:
            with open(filename, encoding=encoding) as fp:
                self._read(fp, filename)
        except Exception as e:
            continue
        if isinstance(filename, os.PathLike):
            filename = os.fspath(filename)
        read_ok.append(filename)
    return read_ok

PythonConfigParser.read = read


class ExtendedConfigParser(ConfigParser):


    def read(self, filename):
        '''Read only one filename. In contrast to the original ConfigParser of
        Python, this one is able to read only one file at a time. The last
        read file will be used for the :meth:`write` method.

        .. versionchanged:: 1.9.0
            :meth:`read` now calls the callbacks if read changed any values.

        '''
        if not isinstance(filename, string_types):
            raise Exception('Only one filename is accepted ({})'.format(
                string_types.__name__))
        self.filename = filename
        # If we try to open directly the configuration file in utf-8,
        # we correctly get the unicode value by default.
        # But, when we try to save it again, all the values we didn't changed
        # are still unicode, and then the PythonConfigParser internal do
        # a str() conversion -> fail.
        # Instead we currently to the conversion to utf-8 when value are
        # "get()", but we internally store them in ascii.
        # with codecs.open(filename, 'r', encoding='utf-8') as f:
        #    self.readfp(f)
        old_vals = {sect: {k: v for k, v in self.items(sect)} for sect in
                    self.sections()}
        PythonConfigParser.read(self, filename)

        # when reading new file, sections/keys are only increased, not removed
        f = self._do_callbacks
        for section in self.sections():
            if section not in old_vals:  # new section
                for k, v in self.items(section):
                    f(section, k, v)
                continue

            old_keys = old_vals[section]
            for k, v in self.items(section):  # just update new/changed keys
                if k not in old_keys or v != old_keys[k]:
                    f(section, k, v)

