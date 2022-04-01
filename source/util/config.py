import os
import json


class Config:
    """
    Stores key value pairs read from a *.json file.
    """
    def __init__(self, json_file: str):
        self._file = ''
        self._dict = {}

        if os.path.exists(json_file):
            self._file = json_file

        self.read()

    def read(self):
        if not self._file:
            return

        handle = open(self._file, 'r', encoding='utf-8')
        self._dict = json.load(handle)
        handle.close()

    def get(self, key: str):
        if key in self._dict:
            return self._dict[key]
        return None

    def set(self, key: str, value):
        self._dict[key] = value

    def get_or_set(self, key: str, default):
        result = self.get(key)

        if not result:
            self.set(key, default)
            return default
        return result
