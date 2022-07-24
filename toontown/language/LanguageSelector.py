from direct.gui.DirectGui import OnscreenImage, DirectLabel, DirectButton
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toontowngui import TTDialog
import os

class LanguageSelector:

    def __init__(self, leaveFunction):
        self.title = None
        self.current = None
        self.available = None
        self.english = None
        self.french = None
        self.portuguese = None
        self.german = None
        self.backButton = None
        self.confirmDialog = None
        self.leaveFunction = leaveFunction

    def create(self):
        self.background = OnscreenImage(parent=render2d, image="phase_3.5/maps/blackboardEmpty.jpg")
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        self.shuffleUp = self.gui.find('**/tt_t_gui_mat_shuffleUp')
        self.shuffleDown = self.gui.find('**/tt_t_gui_mat_shuffleDown')

        self.title = DirectLabel(aspect2d, relief=None, text=TTLocalizer.LanguageSelectorTitle,
                     text_fg=(0, 1, 0, 1), text_scale=0.15, text_font=ToontownGlobals.getSuitFont(),
                     pos=(0, 0, 0.70), text_shadow=(0, 0.392, 0, 1))

        self.current = DirectLabel(aspect2d, relief=None, text=TTLocalizer.LanguageSelectorCurrent % settings['language'],
                       text_fg=(0, 1, 0, 1), text_scale=0.09, text_font=ToontownGlobals.getSuitFont(),
                       pos=(0, 0, 0.55), text_shadow=(0, 0.392, 0, 1))

        self.available = DirectLabel(aspect2d, relief=None, text=TTLocalizer.LanguageSelectorAvailable,
                         text_fg=(1, 0, 0, 1), text_scale=0.09, text_font=ToontownGlobals.getSuitFont(),
                         pos=(0, 0, 0), text_shadow=(0.545, 0, 0, 1))

        self.english = DirectButton(aspect2d, relief=None, text='English',
                       text_fg=(1, 0.549, 0, 1), text_scale=0.09, text_font=ToontownGlobals.getSuitFont(),
                       pos=(0, 0, -0.15), text_shadow=(1, 0.27, 0, 1), command=self.switchLanguage, extraArgs=['English'])

        self.french = DirectButton(aspect2d, relief=None, text='French',
                      text_fg=(1, 0.549, 0, 1), text_scale=0.09, text_font=ToontownGlobals.getSuitFont(),
                      pos=(0, 0, -0.25), text_shadow=(1, 0.27, 0, 1), command=self.switchLanguage, extraArgs=['French'])

        self.portuguese = DirectButton(aspect2d, relief=None, text='Portuguese',
                      text_fg=(1, 0.549, 0, 1), text_scale=0.09, text_font=ToontownGlobals.getSuitFont(),
                      pos=(0, 0, -0.35), text_shadow=(1, 0.27, 0, 1), command=self.switchLanguage, extraArgs=['Portuguese'])

        self.german = DirectButton(aspect2d, relief=None, text='German',
                      text_fg=(1, 0.549, 0, 1), text_scale=0.09, text_font=ToontownGlobals.getSuitFont(),
                      pos=(0, 0, -0.45), text_shadow=(1, 0.27, 0, 1), command=self.switchLanguage, extraArgs=['German'])

        self.backButton = DirectButton(aspect2d, relief=None, image=(self.shuffleUp, self.shuffleDown),
                          text=TTLocalizer.LanguageSelectorBack, text_font=ToontownGlobals.getInterfaceFont(),
                          text_scale=0.11, text_pos=(0, -0.02), pos=(0, 0, -0.75), text_fg=(1, 1, 1, 1),
                          text_shadow=(0, 0, 0, 1), command=self.destroy)

    def destroy(self):
        for element in [self.background, self.title, self.current, self.available, self.english, self.french, self.portuguese, self.german, self.backButton, self.confirmDialog]:
            if element:
                element.destroy()
                element = None

        self.leaveFunction()

    def switchLanguage(self, language):
        if language == settings['language']:
            self.confirmDialog = TTDialog.TTDialog(style=TTDialog.Acknowledge, text=TTLocalizer.LanguageSelectorSameLanguage, command=self.cleanupDialog)
        else:
            self.confirmDialog = TTDialog.TTDialog(style=TTDialog.YesNo, text=TTLocalizer.LanguageSelectorConfirm % language, command=self.confirmSwitchLanguage, extraArgs=[language])
        self.confirmDialog.show()

    def confirmSwitchLanguage(self, value, language):
        if value > 0:
            settings['language'] = language
            os._exit(1)
        else:
            self.cleanupDialog()

    def cleanupDialog(self, value=0):
        self.confirmDialog.cleanup()
