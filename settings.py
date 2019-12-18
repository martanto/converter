import json
import datetime

class Settings:
    def __init__(self, file_setting='settings.json'):
        self._file_setting = file_setting

    def get_settings(self):
        with open(self._file_setting) as file_settings:
            return json.load(file_settings)

settings = Settings().get_settings()