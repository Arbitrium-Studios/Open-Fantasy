from panda3d.core import Vec4, TransparencyAttrib, Point3, VBase3, VBase4, TextNode, CardMaker
from direct.interval.IntervalGlobal import *
from toontown.toon import Toon, ToonDNA
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToonBase
from direct.task import Task
from panda3d.core import AudioSound
from direct.showbase.DirectObject import DirectObject

class Credits(DirectObject):

    def __init__(self):
        #setup
        # self.base = base
        self.fade_out_and_in("fade_task")

        # Load the first music track
        self.track1 = base.loader.loadMusic("phase_3/audio/bgm/tt_theme.ogg")

        # Load the second music track
        self.track2 = base.loader.loadMusic("phase_9/audio/bgm/CogHQ_finale.ogg")

        # Set the volume for the first track
        self.track1.setVolume(1.0)

        # Play the first track
        self.track1.play()

        # Set up event handling
        self.accept('fade_task', self.fade_out_and_in)

        # Schedule the fade-out and fade-in task
        taskMgr.add(self.fade_task, "fade_task")
        self.creditsSequence = None
        self.text = None
        self.roleText = None
        cm = CardMaker('screen-cover')
        cm.setFrameFullscreenQuad()
        self.screenCover = aspect2d.attachNewNode(cm.generate())
        self.screenCover.show()
        self.screenCover.setScale(100)
        self.screenCover.setColor((0, 0, 0, 0.8))
        self.screenCover.setTransparency(1)

        #run
        self.extremelylargecredits = '''
\1limeText\1Credits\2
\1limeText\1Management Team\2
Gracie | Director/Owner
Pizza Taco Burger | Co-Owner
\1limeText\1Technical Team\2
The Professor | Developer
Something Random | Developer
Sighost | Developer
THE PLAYER ZER0 aka Gracie T. Lovelight | Developer
\1limeText\1Creative Team\2
SirDapperPenguin | 3D Modeler
Jardin | Artist
April | Artist
AiGenics | Story Writer
THE PLAYER ZER0 aka Gracie T. Lovelight | Story Writer
Pizza Taco Burger | Storyline Writer
\1limeText\1Contributors\2
Battery on Discord for helping me fix the Tuple error!
DarthM on Discord for various features including Credits, Genderless Toons, etc.
TrueBlueDogemon on Discord for implementing various Quality of Life features including Multiple SOS Cards.
Rocket for helping me implement Wide-Screen Support
DTM1218
ToonJoey for letting us use his Project: Bikehorn assets for HD textures

\1limeText\1Special Thanks To\2
Satire6 for releasing Pandora & Anesidora to the public!
Toontown Rewritten for reviving the spirit of Toontown and its community!
Disney Virtual Reality Studios and Schell Games for creating this ever-green video game!
Jesse Schell for fighting for Toontown Online's Official Return

\1limeText\Thanks for everything!\2
        '''
        self.text = OnscreenText(text = self.extremelylargecredits, style = 3, fg = (1, 1, 1, 1), align = TextNode.ACenter, scale = 0.08, wordwrap = 30, parent = aspect2d)
        self.text.setPos(0, -1)
        self.text.setColorScale(1, 1, 1, 0)
        self.logo = OnscreenImage(image = 'phase_3/maps/toontown-logo.png',
                                  scale = (0.8 * (4.0 / 3.0), 0.8, 0.8 / (4.0 / 3.0)))
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        self.logo.reparentTo(self.text)
        self.logo.setPos(0, 0, 0)
        self.logo.setColorScale(1, 1, 1, 1)
        self.startCredits()
        base.transitions.fadeScreen(0)
        base.accept('space', self.removeCredits)
        base.accept('escape', self.removeCredits)

    def fade_out_and_in(self, task):
        self.fade_out_and_in(track1, track2)
        # Check if the first track is still playing
        if self.track1.status() == AudioSound.PLAYING:
            # Gradually decrease the volume of the first track
            current_volume = self.track1.getVolume()
            if current_volume > 0.01:
                self.track1.setVolume(current_volume - 0.01)
            else:
                # Stop the first track when volume is low
                self.track1.stop()
                self.track1.setVolume(1.0)

                # Play the second track
                self.track2.play()

        # Check if the second track is still playing
        if self.track2.status() == AudioSound.PLAYING:
            # Gradually increase the volume of the second track
            current_volume = self.track2.getVolume()
            if current_volume < 1.0:
                self.track2.setVolume(current_volume + 0.01)

        # Return task.cont to keep the task running
        return Task.cont

    def startCredits(self):
        self.fade_task.start()
        self.creditsSequence = Sequence(
        LerpColorScaleInterval(self.screenCover, 1, Vec4(1, 1, 1, 1), startColorScale = Vec4(1, 1, 1, 0)),
        LerpColorScaleInterval(self.text, 1, Vec4(1, 1, 1, 1), startColorScale = Vec4(1, 1, 1, 0)),
        Wait(1),
        self.text.posInterval(35, Point3(0, 0, 6)),
        Wait(1),
        LerpColorScaleInterval(self.screenCover, 1, Vec4(1, 1, 1, 0), startColorScale = Vec4(1, 1, 1, 1)),
        Func(self.removeCredits)
        ).start()

    def removeCredits(self):
        base.ignore('space')
        base.ignore('escape')
        base.transitions.noFade()
        self.fade_task.destroy()
        if self.creditsSequence:
            self.creditsSequence.finish()
            self.creditsSequence = None
        if self.text:
            self.text.destroy()
            self.text = None
        if self.screenCover:
            self.screenCover.removeNode()
            self.screenCover = None
