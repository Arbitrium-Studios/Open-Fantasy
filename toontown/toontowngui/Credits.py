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
\1limeText\1Credits:\2

\1limeText\1The Auteurs of Life (Project Leaders):\2

- Co-Director Gracie "THE PLAYER ZER0" Lovelight
- Co-Director Pizza Taco Burger

\1limeText\1The Architects of Realities (Programmers):\2

- Professor Control
- DarthMDev aka darthanonymous aka MichaelGDev48
- Gracie "THE PLAYER ZER0" Lovelight
- SomethingRandom0768 for beginning to develop the Custom Control Support and adding Linux support.
- (Retired) TrueBlueDogemon on Discord for implementing various Quality of Life features including Multiple SOS Cards.
- (Retired) HunterBoppen for helping to fixing district resets, security vulnerabilities, and more
- (Retired) CloudCityDev for helping with security patches

\1limeText\1The Artisans of Nature (Artists):\2

- Gracie "THE PLAYER ZER0" Lovelight
- Milo Charming Magician aka CyndaneraX
- (Retired) AiGenics
- (Retired) Jardin
- (Retired) April

\1limeText\1The Animators of Life (Animators):\2

- Milo Charming Magician aka CyndaneraX

\1limeText\1The Sculptors of Creation (Modelers):\2

- Gracie "THE PLAYER ZER0" Lovelight
- (Retired) SirDapperPenguin

\1limeText\1The Conductors of Harmony (Musicians):\2

- Milo Charming Magician aka CyndaneraX

\1limeText\1The Scribes of Fate (Writers):\2

- Gracie "THE PLAYER ZER0" Lovelight
- Pizza Taco Burger

\1limeText\1The Patrons' Assistants (Customer Support):\2

- Gracie "THE PLAYER ZER0" Lovelight
- (Retired) Rouge

\1limeText\1Allies of Continuance (Contributors):\2

- Battery on Discord for helping me fix a Tuple error!
- J3 on Discord for helping to patch one of those pesky bugs!
- leothegreat2003#4524 for helping me find the bug that caused the Streets to not work and incorrect NPC locations!
- Wizzerinus for helping fix various bugs in the orbital camera
- TechieBlort for the Doodle Accuracy code 

\1limeText\1Special Thanks to:\2

- Open-Toontown for creating the source code Toontown Fantasy is based in!
- DTM1218 for letting me use parts of Declashified to improve the game!
- Toontown Galaxy team for letting us use their Panda3D & Orbital Camera
- Princess Rainbow, Cuddles Crinklemuffin, the Magnificent Eleven, and so many others for inspiring the stories!
- Satire6 for releasing Pandora & Anesidora to the public!
- ToonJoey for letting us use Project: Bikehorn as a basis for our HD Textures
- Flameout56 for allowing me to use the Toontown HD resources to further update the game's resources.
- The Panda3D Team for continuously maintaining the engine
- Toontown Rewritten for reviving the spirit of Toontown and its community!
- Disney Virtual Reality Studios and Schell Games for creating this ever-green video game!
- Jesse Schell for pitching Toontown Online to Disney and fighting for its return!

\1limeText\1And YOU for playing the game!\2

        '''
        self.text = OnscreenText(text = self.extremelylargecredits, style = 3, fg = (1, 1, 1, 1), align = TextNode.ACenter, scale = 0.08, wordwrap = 30, parent = aspect2d)
        self.text.setPos(0, -1)
        self.text.setColorScale(1, 1, 1, 0)
        self.logo = OnscreenImage(image = 'phase_3/maps/toontown-logo.png',
                                  scale = (0.6 * (4.0 / 3.0), 0.5, 0.5 / (4.0 / 3.0)))
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        self.logo.reparentTo(self.text)
        self.logo.setPos(0, 0, 0)
        self.logo.setColorScale(1, 1, 1, 1)
        self.startCredits()
        base.transitions.fadeScreen(0)
        # base.accept('space', self.removeCredits) # This works however I'm commenting this out because I don't think the "Space Bar" should be the button to exit it.
        base.accept('escape', self.removeCredits)

    def startCredits(self):
        self.creditsSequence = Sequence(
        LerpColorScaleInterval(self.screenCover, 1, Vec4(1, 1, 1, 1), startColorScale = Vec4(1, 1, 1, 0)),
        LerpColorScaleInterval(self.text, 1, Vec4(1, 1, 1, 1), startColorScale = Vec4(1, 1, 1, 0)),
        Wait(1),
        self.text.posInterval(40, Point3(0, 0, 6.906)),
        Wait(1),
        LerpColorScaleInterval(self.screenCover, 1, Vec4(1, 1, 1, 0), startColorScale = Vec4(1, 1, 1, 1)),
        Func(self.removeCredits)
        ).start()

    def removeCredits(self):
        # base.ignore('space') # This works however I'm commenting this out because I don't think the "Space Bar" should be the button to exit it.
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
