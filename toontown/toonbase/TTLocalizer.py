from direct.directnotify import DirectNotifyGlobal
from panda3d.core import ConfigVariableString, ConfigVariableBool
import os, sys, importlib

categoryName = 'TTLocalizer'

class LanguageManager:
    notify = DirectNotifyGlobal.directNotify.newCategory(categoryName)
    def __init__(self):
        self.TOONTOWN_DIR = 'toontown'
        self.TOONBASE_DIR = 'toonbase'
        self.TT_LOCALIZER_NAME = categoryName
        self.defaultLanguage = ConfigVariableString('default-language', 'english').value
        self.want_language_selection = ConfigVariableBool('want-language-selection', True).value

    def chosenLanguage(self):
        from otp.settings.Settings import Settings
        self.settings = Settings()
        self.ignoreUserOptions = ConfigVariableBool('ignore-user-options', False).value
        if self.want_language_selection or not self.ignoreUserOptions:
            self.settings.readSettings()
            self.chosenLanguage = self.settings.getSetting(setting='language')
            language = self.chosenLanguage
        else:
            language = f'{self.defaultLanguage}'
        return language

    def loadLocalizer(self):
        language = LanguageManager.chosenLanguage(self)
        if language is None:
            language = self.defaultLanguage or 'english'

        if language == self.defaultLanguage:
            language = f'{language}'.title()
            TT_LOCALIZER_LANG_FILE = f'{self.TT_LOCALIZER_NAME}{language}.py'
        else:
            language = f'{language}'.title()
            TT_LOCALIZER_LANG_FILE = f'{self.TT_LOCALIZER_NAME}_{language}.py'

        TT_LOCALIZER_LANG_PATH = os.path.join(self.TOONTOWN_DIR, self.TOONBASE_DIR, TT_LOCALIZER_LANG_FILE)
        lang_localizer_path_for_python = TT_LOCALIZER_LANG_PATH.replace(os.sep, '.')
        localizer_file_name = TT_LOCALIZER_LANG_FILE.replace("_", ' ')
        pyFileExtension = '.py'
        endsWithCheckQuotated = f'"{pyFileExtension}"'
        if lang_localizer_path_for_python.endswith(pyFileExtension):
            suffixless_file_name = lang_localizer_path_for_python.replace(pyFileExtension, '')
            _languageModule = suffixless_file_name
        else:
            _languageModule = lang_localizer_path_for_python

        try:
            if os.path.exists(TT_LOCALIZER_LANG_PATH):
                language = f'{language}'.title()
                self.notify.info('Running in language: {}'.format(language))

                lang_module = importlib.import_module(_languageModule)

                allowed_keys = getattr(lang_module, '__all__', [k for k in dir(lang_module) if not k.startswith('_')])

                for key in allowed_keys:
                    globals()[key] = getattr(lang_module, key)
                return language
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            self.notify.error(f'The "{localizer_file_name}" does NOT exist at "{TT_LOCALIZER_LANG_PATH}".')
            return sys.exit(1)
        except Exception as e:
            partial_reason = f'Unable to load the "{localizer_file_name}" file cuz of the following reason'
            self.notify.error(f'{partial_reason}:\n\n{e}\n')
            return sys.exit(1)

LanguageManagerObj = LanguageManager()

def getLanguage():
    language = LanguageManagerObj.chosenLanguage()
    return language

LanguageManagerObj.loadLocalizer()
