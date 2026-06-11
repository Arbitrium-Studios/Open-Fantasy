from direct.directnotify import DirectNotifyGlobal
from panda3d.core import ConfigVariableString, ConfigVariableBool
import os, sys, importlib

categoryName = f'OTPLocalizer'

class LanguageManager:
    notify = DirectNotifyGlobal.directNotify.newCategory(categoryName)
    def __init__(self):
        self.OTP_DIR = 'otp'
        self.OTPBASE_DIR = 'otpbase'
        self.OTP_LOCALIZER_NAME = categoryName
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
        if language == self.defaultLanguage:
            languageAdjusted = f'{language}'.title()
            OTP_LOCALIZER_LANG_FILE = f'{self.OTP_LOCALIZER_NAME}{languageAdjusted}.py'
        else:
            languageAdjusted = f'{language}'.title()
            OTP_LOCALIZER_LANG_FILE = f'{self.OTP_LOCALIZER_NAME}_{languageAdjusted}.py'

        OTP_LOCALIZER_LANG_PATH = os.path.join(self.OTP_DIR, self.OTPBASE_DIR, OTP_LOCALIZER_LANG_FILE)
        lang_localizer_path_for_python = OTP_LOCALIZER_LANG_PATH.replace(os.sep, '.')
        lang_localizer_path_for_python_quotated = f'"{lang_localizer_path_for_python}"'
        lang_localizer_path_for_python_str_quotated = f'"lang_localizer_path_for_python"'
        localizer_file_name = f'{OTP_LOCALIZER_LANG_FILE}'
        localizer_file_name_str = localizer_file_name.replace("_", ' ')
        localizer_file_name_quotated = f'"{localizer_file_name_str}"'
        localizer_path_quotated = f'"{OTP_LOCALIZER_LANG_PATH}"'
        pyFileExtension = '.py'
        endsWithCheckQuotated = f'"{pyFileExtension}"'
        if lang_localizer_path_for_python.endswith(pyFileExtension):
            suffixless_file_name = lang_localizer_path_for_python.replace(pyFileExtension, '')
            _languageModule = suffixless_file_name
        else:
            _languageModule = lang_localizer_path_for_python

        try:
            if os.path.exists(OTP_LOCALIZER_LANG_PATH):
                language = f'{language}'.title()
                self.notify.info('{}: Running in language: {}'.format(self.OTP_LOCALIZER_NAME, language))

                lang_module = importlib.import_module(_languageModule)

                allowed_keys = getattr(lang_module, '__all__', [k for k in dir(lang_module) if not k.startswith('_')])

                for key in allowed_keys:
                    globals()[key] = getattr(lang_module, key)
                return language
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            self.notify.error(f'The {localizer_file_name_quotated} does NOT exist at {localizer_path_quotated}.\n')
            return sys.exit(1)
        except Exception as e:
            self.notify.error(f'Unable to load the {localizer_file_name_quotated} file cuz of the following reason:\n\n{e}\n')
            return sys.exit(1)

LanguageManagerObj = LanguageManager()

def getLanguage():
    language = LanguageManagerObj.chosenLanguage()
    return language

LanguageManagerObj.loadLocalizer()
