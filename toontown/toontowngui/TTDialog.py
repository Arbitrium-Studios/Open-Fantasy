from otp.otpgui.OTPDialog import *
from direct.interval.IntervalGlobal import *
from panda3d.core import Vec3

class TTDialog(OTPDialog):

    def __init__(self, parent=None, style=NoButtons, **kw):
        self.path = 'phase_3/models/gui/dialog_box_buttons_gui'
        OTPDialog.__init__(self, parent, style, **kw)
        self.initialiseoptions(TTDialog)
        Sequence(
            LerpScaleInterval(self, .2, Vec3(1.1, 1.1, 1.1), Vec3(0, 0, 0), blendType='easeInOut'),
            LerpScaleInterval(self, .09, Vec3(1, 1, 1), Vec3(1.1, 1.1, .1), blendType='easeInOut')).start()


class TTGlobalDialog(GlobalDialog):

    def __init__(self, message='', doneEvent=None, style=NoButtons,
                 okButtonText=OTPLocalizer.DialogOK, cancelButtonText=OTPLocalizer.DialogCancel, **kw):
        self.path = 'phase_3/models/gui/dialog_box_buttons_gui'
        GlobalDialog.__init__(
            self,
            message,
            doneEvent,
            style,
            okButtonText,
            cancelButtonText,
            **kw)
        self.initialiseoptions(TTGlobalDialog)
        Sequence(
            LerpScaleInterval(self, .2, Vec3(1.1, 1.1, 1.1), Vec3(0, 0, 0), blendType='easeInOut'),
            LerpScaleInterval(self, .09, Vec3(1, 1, 1), Vec3(1.1, 1.1, 1.1), blendType='easeInOut')).start()
