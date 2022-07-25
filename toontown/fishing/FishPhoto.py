
#from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
#from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from . import FishGlobals

class DirectRegion(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory("DirectRegion")

    def __init__(self, parent=aspect2d):
        assert self.notify.debugStateCall(self)
        NodePath.__init__(self)
        self.assign(parent.attachNewNode("DirectRegion"))
    
    def destroy(self):
        assert self.notify.debugStateCall(self)
        self.unload()

    def setBounds(self, *bounds):
        """
        bounds are floats: left, right, top, bottom
        """
        assert self.notify.debugStateCall(self)
        assert len(bounds) == 4
        self.bounds=bounds
        
    def setColor(self, *colors):
        """
        colors are floats: red, green, blue, alpha
        """
        assert self.notify.debugStateCall(self)
        assert len(colors) == 4
        self.color=colors

    def show(self):
        assert self.notify.debugStateCall(self)
    
    def hide(self):
        assert self.notify.debugStateCall(self)

    def load(self):
        assert self.notify.debugStateCall(self)
        if not hasattr(self, "cRender"):
            # Create a separate reality for the fish to swim in:
            self.cRender = NodePath('fishSwimRender')
            # It gets its own camera
            self.fishSwimCamera = self.cRender.attachNewNode('fishSwimCamera')
            self.cCamNode = Camera('fishSwimCam')
            self.cLens = PerspectiveLens()
            self.cLens.setFov(40,40)
            self.cLens.setNear(0.1)
            self.cLens.setFar(100.0)
            self.cCamNode.setLens(self.cLens)
            self.cCamNode.setScene(self.cRender)
            self.fishSwimCam = self.fishSwimCamera.attachNewNode(self.cCamNode)

            cm = CardMaker('displayRegionCard')
            
            assert hasattr(self, "bounds")
            cm.setFrame(*self.bounds)
            
            self.card = card = self.attachNewNode(cm.generate())
            assert hasattr(self, "color")
            card.setColor(*self.color)
            
            newBounds=card.getTightBounds()
            ll=render2d.getRelativePoint(card, newBounds[0])
            ur=render2d.getRelativePoint(card, newBounds[1])
            newBounds=[ll.getX(), ur.getX(), ll.getZ(), ur.getZ()]
            # scale the -1.0..2.0 range to 0.0..1.0:
            newBounds=[max(0.0, min(1.0, (x+1.0)/2.0)) for x in newBounds]

            self.cDr = base.win.makeDisplayRegion(*newBounds)
            self.cDr.setSort(10)
            self.cDr.setClearColor(card.getColor())
            self.cDr.setClearDepthActive(1)
            self.cDr.setClearColorActive(1)
            self.cDr.setCamera(self.fishSwimCam)
        return self.cRender

    def unload(self):
        assert self.notify.debugStateCall(self)
        if hasattr(self, "cRender"):
            base.win.removeDisplayRegion(self.cDr)
            del self.cRender
            del self.fishSwimCamera
            del self.cCamNode
            del self.cLens
            del self.fishSwimCam
            del self.cDr

class FishPhoto(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory("FishPhoto")

    # special methods
    def __init__(self, fish=None, parent=aspect2d):
        assert self.notify.debugStateCall(self)
        NodePath.__init__(self)
        self.assign(parent.attachNewNode("FishPhoto"))
        self.fish = fish
        self.actor = None
        self.sound = None
        self.soundTrack = None
        self.track = None
        self.fishFrame = None
        
    def destroy(self):
        assert self.notify.debugStateCall(self)
        self.hide()
        if hasattr(self, "background"):
            del self.background
        self.fish = None
        del self.soundTrack
        del self.track
        
    def update(self, fish):
        assert self.notify.debugStateCall(self)
        self.fish = fish

    def setSwimBounds(self, *bounds):
        """
        bounds are floats: left, right, top, bottom
        """
        assert len(bounds) == 4
        self.swimBounds=bounds
        
    def setSwimColor(self, *colors):
        """
        colors are floats: red, green, blue, alpha
        """
        assert len(colors) == 4
        self.swimColor=colors

    def load(self):
        assert self.notify.debugStateCall(self)
    
    def makeFishFrame(self, actor):
        assert self.notify.debugStateCall(self)
        # NOTE: this may need to go in FishBase eventually
        actor.setDepthTest(1)
        actor.setDepthWrite(1)

        # scale the actor to the frame
        if not hasattr(self, "fishDisplayRegion"):
            self.fishDisplayRegion = DirectRegion(parent=self)
            self.fishDisplayRegion.setBounds(*self.swimBounds)
            self.fishDisplayRegion.setColor(*self.swimColor)
        frame = self.fishDisplayRegion.load()
        pitch = frame.attachNewNode('pitch')
        rotate = pitch.attachNewNode('rotate')
        scale = rotate.attachNewNode('scale')
        actor.reparentTo(scale)
        # Translate actor to the center.
        bMin,bMax = actor.getTightBounds()
        center = (bMin + bMax)/2.0
        actor.setPos(-center[0], -center[1], -center[2])
        genus = self.fish.getGenus()
        fishInfo = FishGlobals.FishFileDict.get(genus, FishGlobals.FishFileDict[-1])
        fishPos = fishInfo[5]
        if fishPos:
            actor.setPos(fishPos[0], fishPos[1], fishPos[2])
        scale.setScale(fishInfo[6])
        rotate.setH(fishInfo[7])
        pitch.setP(fishInfo[8])
        pitch.setY(2)

        return frame

    def show(self, showBackground=0):
        assert self.notify.debugStateCall(self)
        # if we are browsing fish we must be awake
        messenger.send('wakeup')
        if self.fishFrame:
            self.actor.cleanup()
            if hasattr(self, "fishDisplayRegion"):
                self.fishDisplayRegion.unload()
            self.hide()
        self.actor = self.fish.getActor()
        self.actor.setTwoSided(1)
        self.fishFrame = self.makeFishFrame(self.actor)

        if showBackground:
            if not hasattr(self, "background"):
                background = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
                background = background.find("**/Fish_BG")
                self.background = background
            self.background.setPos(0, 15, 0)
            self.background.setScale(11)
            self.background.reparentTo(self.fishFrame)
        self.sound, loop, delay, playRate = self.fish.getSound()
        if playRate is not None:
            # make a track to play the anim and sound
            self.actor.setPlayRate(playRate, "intro")
            self.actor.setPlayRate(playRate, "swim")
        introDuration = self.actor.getDuration("intro")
        track = Parallel(
            Sequence(
                Func(self.actor.play, "intro"),
                Wait(introDuration),
                Func(self.actor.loop, "swim")))
        # if we have a sound, make a track to loop it
        if self.sound:
            soundTrack = Sequence(
                Wait(delay),
                Func(self.sound.play))
            if loop:
                duration = max(introDuration, self.sound.length())
                soundTrack.append(Wait(duration - delay))
                track.append(Func(soundTrack.loop))
                #soundTrack.setLoop(1)
                #track.append(soundTrack)
                self.soundTrack = soundTrack
            else:
                track.append(soundTrack)

        self.track = track
        self.track.start()

    def hide(self):
        assert self.notify.debugStateCall(self)
        if hasattr(self, "fishDisplayRegion"):
            self.fishDisplayRegion.unload()
        if self.actor:
            self.actor.stop()
        if self.sound:
            self.sound.stop()
            self.sound = None
        if self.soundTrack:
            self.soundTrack.pause()
            self.soundTrack = None
        if self.track:
            self.track.pause()
            self.track = None
