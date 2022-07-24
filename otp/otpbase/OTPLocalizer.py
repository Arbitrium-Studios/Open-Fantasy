from otp.otpbase.OTPLocalizerEnglish import *
from panda3d.core import *
import string
import types

try:
    language = settings['language']
except:
    language = 'English'

print('OTPLocalizer: Running in language: %s' % language)
from otp.otpbase.OTPLocalizerEnglish import *

if language != 'English':
    l = {}
    g = {}
    module = 'otp.otpbase.OTPLocalizer' + language
    englishModule = __import__('otp.otpbase.OTPLocalizerEnglish', g, l)
    foreignModule = __import__(module, g, l)
    for key, val in englishModule.__dict__.items():
        if key not in foreignModule.__dict__:
            print('WARNING: Foreign module: %s missing key: %s' % (module, key))
            locals()[key] = val
        elif isinstance(val, types.DictType):
            fval = foreignModule.__dict__.get(key)
            for dkey, dval in val.items():
                if dkey not in fval:
                    print('WARNING: Foreign module: %s missing key: %s.%s' % (module, key, dkey))
                    fval[dkey] = dval

            for dkey in fval.keys():
                if dkey not in val:
                    print('WARNING: Foreign module: %s extra key: %s.%s' % (module, key, dkey))

    for key in foreignModule.__dict__.keys():
        if key not in englishModule.__dict__:
            print('WARNING: Foreign module: %s extra key: %s' % (module, key))

print('OTPLocalizer: Running in language: %s' % language)
if language == 'english':
    _languageModule = 'otp.otpbase.OTPLocalizer' + language.capitalize()
else:
    checkLanguage = 1
    _languageModule = 'otp.otpbase.OTPLocalizer' + language
print('from ' + _languageModule + ' import *')
if checkLanguage:
    l = {}
    g = {}
    englishModule = __import__('otp.otpbase.OTPLocalizerEnglish', g, l)
    foreignModule = __import__(_languageModule, g, l)
    for key, val in list(englishModule.__dict__.items()):
        if key not in foreignModule.__dict__:
            print(
                'WARNING: Foreign module: %s missing key: %s' %
                (_languageModule, key))
            locals()[key] = val
        elif isinstance(val, dict):
            fval = foreignModule.__dict__.get(key)
            for dkey, dval in list(val.items()):
                if dkey not in fval:
                    print(
                        'WARNING: Foreign module: %s missing key: %s.%s' %
                        (_languageModule, key, dkey))
                    fval[dkey] = dval

            for dkey in list(fval.keys()):
                if dkey not in val:
                    print(
                        'WARNING: Foreign module: %s extra key: %s.%s' %
                        (_languageModule, key, dkey))

    for key in list(foreignModule.__dict__.keys()):
        if key not in englishModule.__dict__:
            print(
                'WARNING: Foreign module: %s extra key: %s' %
                (_languageModule, key))
