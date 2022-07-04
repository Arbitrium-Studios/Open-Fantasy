from panda3d.core import *
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal
from . import Walk
from otp.otpbase import OTPGlobals


class PublicWalk(Walk.Walk):
    notify = DirectNotifyGlobal.directNotify.newCategory('PublicWalk')

    def __init__(self, parentFSM, doneEvent):
        Walk.Walk.__init__(self, doneEvent)
        self.parentFSM = parentFSM
        self.previousFOV = None
        self.isSprinting = 0

    def load(self):
        Walk.Walk.load(self)

    def unload(self):
        Walk.Walk.unload(self)
        del self.parentFSM

    def enter(self, slowWalk=0):
        Walk.Walk.enter(self, slowWalk)
        base.localAvatar.book.showButton()
        self.accept(StickerBookHotkey, self.__handleStickerBookEntry)
        self.accept('enterStickerBook', self.__handleStickerBookEntry)
        self.accept(OptionsPageHotkey, self.__handleOptionsEntry)
        base.localAvatar.laffMeter.start()
        base.localAvatar.beginAllowPies()
        # switch to this when we implement keymapping for the controls
        # self.accept(base.SPRINT, self.startSprint)
        # self.accept(f'{base.SPRINT}-up', self.stopSprint)
        self.accept('shift', self.startSprint)
        self.accept('shift-up', self.stopSprint)

    def exit(self):
        Walk.Walk.exit(self)
        base.localAvatar.book.hideButton()
        self.ignore(StickerBookHotkey)
        self.ignore('enterStickerBook')
        self.ignore(OptionsPageHotkey)
        base.localAvatar.laffMeter.stop()
        base.localAvatar.endAllowPies()
        # switch to this when we implement keymapping for the controls
        # self.ignore(base.SPRINT)
        # self.ignore(f'{base.SPRINT}-up')
        self.ignore('shift')
        self.ignore('shift-up')

    def startSprint(self):
        if hasattr(base, 'localAvatar'):
            if base.localAvatar.getHp() <= 0:
                return
            else:
                self.previousFOV = base.genFOV

                base.localAvatar.currentSpeed = OTPGlobals.ToonForwardSprintSpeed
                base.localAvatar.currentReverseSpeed = OTPGlobals.ToonReverseSprintSpeed
                base.localAvatar.controlManager.setSpeeds(
                    OTPGlobals.ToonForwardSprintSpeed, OTPGlobals.ToonJumpForce, OTPGlobals.ToonReverseSprintSpeed, OTPGlobals.ToonRotateSpeed)
                self.isSprinting = 1
                base.localAvatar.lerpCameraFov(self.previousFOV + 20, 0.5)

        else:
            if self.isSprinting == 1:
                self.stopSprint()

    def stopSprint(self):
        if hasattr(base, 'localAvatar'):
            base.localAvatar.currentSpeed = OTPGlobals.ToonForwardSpeed
            base.localAvatar.currentReverseSpeed = OTPGlobals.ToonReverseSpeed
            base.localAvatar.controlManager.setSpeeds(
                OTPGlobals.ToonForwardSpeed, OTPGlobals.ToonJumpForce, OTPGlobals.ToonReverseSpeed, OTPGlobals.ToonRotateSpeed)
            self.isSprinting = 0
            base.localAvatar.lerpCameraFov(self.previousFOV, 1.0)

    def __handleStickerBookEntry(self):
        currentState = base.localAvatar.animFSM.getCurrentState().getName()
        if currentState == 'jumpAirborne':
            return
        if base.localAvatar.book.isObscured():
            return
        else:
            doneStatus = {}
            doneStatus['mode'] = 'StickerBook'
            messenger.send(self.doneEvent, [doneStatus])
            return

    def __handleOptionsEntry(self):
        currentState = base.localAvatar.animFSM.getCurrentState().getName()
        if currentState == 'jumpAirborne':
            return
        if base.localAvatar.book.isObscured():
            return
        else:
            doneStatus = {}
            doneStatus['mode'] = 'Options'
            messenger.send(self.doneEvent, [doneStatus])
            return
