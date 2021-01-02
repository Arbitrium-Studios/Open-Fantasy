from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from toontown.cogdominium.DistCogdoCraneObject import DistCogdoCraneObject
from toontown.cogdominium import CogdoCraneGameConsts as GameConsts

class DistCogdoCraneMoneyBag(DistCogdoCraneObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistCogdoCraneMoneyBag')
    grabPos = (0, 0, GameConsts.Settings.MoneyBagGrabHeight.get())
    craneFrictionCoef = 0.2
    craneSlideSpeed = 11
    craneRotateSpeed = 16
    wantsWatchDrift = 0

    def __init__(self, cr):
        DistCogdoCraneObject.__init__(self, cr)
        NodePath.__init__(self, 'object')
        self.index = None
        self.flyToMagnetSfx = loader.loadSfx('phase_5/audio/sfx/TL_rake_throw_only.ogg')
        self.hitMagnetSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_safe.ogg')
        self.toMagnetSoundInterval = Parallel(SoundInterval(self.flyToMagnetSfx, duration=ToontownGlobals.CashbotBossToMagnetTime, node=self), Sequence(Wait(ToontownGlobals.CashbotBossToMagnetTime - 0.02), SoundInterval(self.hitMagnetSfx, duration=1.0, node=self)))
        self.hitFloorSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_bigweight_miss.ogg')
        self.hitFloorSoundInterval = SoundInterval(self.hitFloorSfx, node=self)
        return
    
    def DistCogDoCollHit
        self.cogColl = %s 
        shortChange = 0
        pennyPincher = 1
        tightwad = 2
        beanCounter = 3
        numberCruncher = 4
        moneyBag = 5
    if suit = a,b,c
       a = 'suit_col'
       b = 'suit_col'
       c = 'suit_col'
        
#check for cog coll depending on suit type
     def levelGlobal
       grabCogID = ""
         reparent(level)
         level = '
             1, 2, 3 = 1, 1.5 
             4, 5, 6 = 2, 2.5
             7, 8 = 3, 3.5'
      def hitCenter
    suit_col walk "15"
    meter = ""
    if CogID reparent meter = +1
       elif grabCogId = 5
            meter = +3
    meter_finish = 10
    
    self.grabCogId generate "propeller"
    properller = 'phase'
    self.cogId setPos(x, y, +5)
    
    return generate
    
    meter_tint = LerpColorInterval(self.meter, 5, (5, 1, 1, 1)),
    meter_tint = SetColorInterval(self.meter, , (5, 1, 1, 1)),
    def announceGenerate(self):
        DistCogdoCraneObject.announceGenerate(self)
        self.name = 'moneyBag-%s' % self.doId
        self.setName(self.name)
        self.craneGame.moneyBag.copyTo(self)
        self.shadow = NodePath('notAShadow')
        self.collisionNode.setName('moneyBag')
        cs = CollisionSphere(0, 0, 4, 4)
        self.collisionNode.addSolid(cs)
        self.craneGame.moneyBags[self.index] = self
        self.setupPhysics('moneyBag')
        self.resetToInitialPosition()

    def disable(self):
        del self.craneGame.moneyBags[self.index]
        DistCogdoCraneObject.disable(self)

    def hideShadows(self):
        self.shadow.hide()

    def showShadows(self):
        self.shadow.show()

    def getMinImpact(self):
        if self.craneGame.heldObject:
            return ToontownGlobals.CashbotBossSafeKnockImpact
        else:
            return ToontownGlobals.CashbotBossSafeNewImpact

    def resetToInitialPosition(self):
        posHpr = GameConsts.MoneyBagPosHprs[self.index]
        self.setPosHpr(*posHpr)
        self.physicsObject.setVelocity(0, 0, 0)

    def fellOut(self):
        self.deactivatePhysics()
        self.d_requestInitial()

    def setIndex(self, index):
        self.index = index

    def setObjectState(self, state, avId, craneId):
        if state == 'I':
            self.demand('Initial')
        else:
            DistCogdoCraneObject.setObjectState(self, state, avId, craneId)

    def d_requestInitial(self):
        self.sendUpdate('requestInitial')

    def enterInitial(self):
        self.resetToInitialPosition()
        self.showShadows()

    def exitInitial(self):
        pass

    if __dev__:

        def _handleMoneyBagGrabHeightChanged(self, height):
            grabPos = DistCogdoCraneMoneyBag.grabPos
            DistCogdoCraneMoneyBag.grabPos = (grabPos[0], grabPos[1], height)
