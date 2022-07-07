from panda3d.core import Vec4, TransparencyAttrib, Point3, VBase3, VBase4, TextNode, CardMaker
from direct.interval.IntervalGlobal import *
from toontown.toon import Toon, ToonDNA
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToonBase

class Credits:

    def __init__(self):
        #setup
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
DTM1218
ToonJoey for letting us use his Project: Bikehorn assets for HD textures
Nora for creating the Credits Button.

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

    def startCredits(self):
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
        if self.creditsSequence:
            self.creditsSequence.finish()
            self.creditsSequence = None
        if self.text:
            self.text.destroy()
            self.text = None
        if self.screenCover:
            self.screenCover.removeNode()
            self.screenCover = None
