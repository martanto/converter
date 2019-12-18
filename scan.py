import os
from settings import settings

class Scan():
    def __init__(self, directory=settings['directory'], filter='MAN', type=None):
        self._directory = directory
        self._files = []
        self._filter = filter

    def set_filter(self, filter):
        self._filter = filter
        return self

    def get_filter(self, filter):
        return self._filter

    def set_directory(self, directory):
        self._directory = directory
        return self

    def get_directory(self):
        return self._directory

    def get_files(self):
        for root,directories,files in os.walk(self._directory):
            for file in files:
                if self._filter in file:
                    self._files.append(os.path.join(root, file))
        return self._files
        