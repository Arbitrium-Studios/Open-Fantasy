import json
import os

class Settings:
    defaultSettings = {
        "music": True,
        "sfx": True,
        "toon-chat-sounds": True,
        "smooth-animations": False,
        "show-fps": False,
        "want-laff-meter-over-head": False,
        "accepting-new-friends": False,
        "windowed-mode": True,
        "display-mode": "windowed", # For later update on how TTFan handles Display modes (which will hopefully include Borderless Mode)
        "rich-presence": False,
        "language": "english",
        "want-sleep": True,
    }

    def __init__(self):
        self.__settings = {}
        usersDir = 'users'
        preferencesFile = 'preferences.json'
        if not os.path.exists(f'{usersDir}'):
            os.mkdir(f'{usersDir}')
        self.__filename = f'{usersDir}/{preferencesFile}'

    def doSavedSettingsExist(self):
        return os.path.exists(self.__filename)

    def readSettings(self):
        if not self.doSavedSettingsExist():
            self.__settings = {}
            return

        try:
            with open(self.__filename, 'r') as f:
                self.__settings = json.load(f)
        except BaseException:
            self.__settings = {}

    def writeSettings(self):
        with open(self.__filename, 'w+') as f:
            json.dump(self.__settings, f, indent=4)

    def updateSetting(self, setting, value):
        self.__settings[setting] = value

    def getSetting(self, setting, default=None):
        return self.__settings.get(setting, default)
