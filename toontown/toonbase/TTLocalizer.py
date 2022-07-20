"""
This module determines what language to run the game in
and imports the appropriate language module.
Import this module, not the individual language modules
to use in the game.
"""

# Do not import panda modules because it is not downloaded until Phase 3
# This file is in phase 2
from panda3d.core import *
import string
import types
from direct.showbase import DConfig
try:
    # Client
    # The Launcher will define config in the builtin namespace
    # before importing this file
    language = DConfig.GetString('language', 'english')
    checkLanguage = DConfig.GetBool('check-language', 0)
except:
    # AI
    language = simbase.config.GetString("language", "english")
    checkLanguage = simbase.config.GetBool("check-language", 0)

# Ask what language we are running in. Returns a string.
def getLanguage():
    return language

print(("TTLocalizer: Running in language: %s" % (language)))
if language == 'english':
    _languageModule = "toontown.toonbase.TTLocalizer" + str.capitalize(language)
else:
    checkLanguage = 1 
    _languageModule = "toontown.toonbase.TTLocalizer_" + language

print(("from " + _languageModule + " import *"))
exec("from " + _languageModule + " import *")

if checkLanguage:
    l = {}
    g = {}
    englishModule = __import__("toontown.toonbase.TTLocalizerEnglish", g, l)
    foreignModule = __import__(_languageModule, g, l)
    for key, val in list(englishModule.__dict__.items()):
        if key not in foreignModule.__dict__:
            print(("WARNING: Foreign module: %s missing key: %s" % (_languageModule, key)))
            # Add the english version to our local namespace so we do not crash
            locals()[key] = val
        else:
            # The key is in both files, but if it is a dictionary we
            # should go one step further and make sure the individual
            # elements also match.
            if isinstance(val, dict):
                fval = foreignModule.__dict__.get(key)
                for dkey, dval in list(val.items()):
                    if dkey not in fval:
                        print(("WARNING: Foreign module: %s missing key: %s.%s" % (_languageModule, key, dkey)))
                        fval[dkey] = dval
                for dkey in list(fval.keys()):
                    if dkey not in val:
                        print(("WARNING: Foreign module: %s extra key: %s.%s" % (_languageModule, key, dkey)))


    for key in list(foreignModule.__dict__.keys()):
        if key not in englishModule.__dict__:
            print(("WARNING: Foreign module: %s extra key: %s" % (_languageModule, key)))
