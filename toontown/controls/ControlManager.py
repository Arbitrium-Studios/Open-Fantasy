from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

from toontown.toonbase import ToontownGlobals

import string


class ControlManager(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ControlManager')

    def __init__(self):
        DirectObject.__init__(self)
        self.changing = False
        self.disableChat = 1
        self.disabledHotkeys = []
        self.activeHotkeys = []
        self.changedHotkeys = {ToontownGlobals.Movement: [],
                               ToontownGlobals.Interaction: [],
                               ToontownGlobals.Debug: [],
                               ToontownGlobals.Misc: []}
        self.disableAlphaNumericHotkeys = False
        self.reloadHotkeys(True)

    def reloadHotkeys(self, realtime=False):
        self.ignoreAll()
        disableChat = 1
        activeHotkeys = []
        for category in ToontownGlobals.Hotkeys:
            controlCategory = base.settings.getOption('controls', category, {})
            if controlCategory == {}:
                continue
            for key in controlCategory.keys():
                hotkey = controlCategory.get(key)
                alphaNumeric = self.isAlphaNumericHotkey(hotkey)
                if disableChat and alphaNumeric:
                    disableChat = 0
                if ToontownGlobals.AllHotkeys[ToontownGlobals.Hotkeys.index(category)].get(key) != hotkey:
                    changedHotkeys = self.changedHotkeys.get(category)
                    changedHotkeys.append(key)
                    self.changedHotkeys[ToontownGlobals.Hotkeys.index(category)] = changedHotkeys
                activeHotkeys.append(hotkey)
                self.accept(hotkey, self.hotkeyPressed, extraArgs=[self.getHotkeyName(category, key), hotkey, key])
                self.accept(hotkey + '-up', self.hotkeyPressed, extraArgs=[self.getHotkeyName(category, key, True), hotkey, key])

        self.activeHotkeys = activeHotkeys

        for category in ToontownGlobals.Hotkeys:
            controlCategory = base.settings.getOption('controls', category, {})
            if controlCategory == {}:
                continue
            for key in controlCategory.keys():
                hotkey = controlCategory.get(key)
                for bonus in ('shift', 'control', 'alt'):
                    failSafeKey = bonus + ToontownGlobals.Separater + hotkey
                    if not hotkey.startswith(str(key)) and failSafeKey not in activeHotkeys:
                        self.accept(failSafeKey, self.hotkeyPressed, extraArgs=[self.getHotkeyName(category, key), hotkey, key])
                        self.accept(failSafeKey + '-up', self.hotkeyPressed, extraArgs=[self.getHotkeyName(category, key, True), hotkey, key])

        self.disableChat = disableChat
        if hasattr(base, 'localAvatar') and hasattr(base.localAvatar, 'chatMgr') and base.localAvatar.chatMgr:
            base.localAvatar.chatMgr.setBackgroundFocus(disableChat, realtime)
            if not disableChat:
                base.localAvatar.chatMgr.chatLog.enableHotkey()
            else:
                base.localAvatar.chatMgr.chatLog.disableHotkey()

    def getHotkeyName(self, category, id, released=False):
        hotkey = 'hotkey-' + category + '-' + str(id)
        if released:
            hotkey += '-up'
        return hotkey

    def setChanging(self, state):
        self.changing = state

    def getChanging(self):
        return self.changing

    def hotkeyPressed(self, hotkeyName, hotkey, key, event=None):
        if not self.getChanging() and int(key) not in self.disabledHotkeys:
            if self.disableAlphaNumericHotkeys:
                if 'enter' in hotkey:
                    messenger.send('exitChat')
                    return
                elif not self.isAlphaNumericHotkey(hotkey):
                    messenger.send(hotkeyName)
                elif hotkeyName.endswith('-up'):
                    messenger.send(hotkeyName)
                else:
                    return
            messenger.send(hotkeyName)

    def getControlName(self, name, label=False):
        if ToontownGlobals.Separater in name:
            name = name.replace(ToontownGlobals.Separater, ' + ')

        for key in ToontownGlobals.SpecialKeys.keys():
            if key in name:
                value = ToontownGlobals.SpecialKeys.get(key)
                name = name.replace(key, value)
                break

        name = name.title()

        if label:
            name += ' Key'
            if '+' in name:
                name += 's'

        return name

    def convertHotkeyString(self, dialog, activator):
        for x in range(dialog.count(activator)):
            split = dialog.split(activator, 1)
            first = split[0][:-1]
            info = split[1]
            category = int(info[:2])
            index = int(info[2:4])
            categoryName = ToontownGlobals.Hotkeys[category]
            controlCategory = base.settings.getOption('controls', categoryName, {})
            hotkey = self.getControlName(controlCategory.get(str(index)), True)
            dialog = first + hotkey + info[4:]

        return dialog

    def isAlphaNumericHotkey(self, hotkey):
        for prefix in ('shift', 'control', 'alt'):
            if prefix in hotkey:
                hotkey = hotkey.replace(prefix, '')
                if ToontownGlobals.Separater in hotkey:
                    hotkey = hotkey.replace(ToontownGlobals.Separater, '')
                else:
                    return False

        if len(hotkey) > 1:
            if hotkey == 'space':
                return True
            return False

        characters = string.printable
        if hotkey in characters:
            return True

        return False

    def getChatDisabled(self):
        return self.disableChat

    def addDisabledHotkey(self, hotkey):
        if hotkey not in self.disabledHotkeys:
            self.disabledHotkeys.append(hotkey)

    def removeDisabledHotkey(self, hotkey):
        if hotkey in self.disabledHotkeys:
            self.disabledHotkeys.remove(hotkey)

    def getKeyInUse(self, hotkey):
        for key in self.activeHotkeys:
            if hotkey in key:
                return True
        return False
