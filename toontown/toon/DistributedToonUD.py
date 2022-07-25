
from otp.ai.AIBaseGlobal import *
from panda3d.core import *
from otp.otpbase import OTPGlobals

from direct.distributed.DistributedObjectUD import DistributedObjectUD
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
from toontown.catalog import CatalogItemTypes
from toontown.catalog import CatalogClothingItem
from toontown.toonbase import ToontownGlobals
from . import ToonDNA

class DistributedToonUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonUD')

    def setMaxFishTank(self, todo0):
        pass

    def setFishTank(self, todo0, todo1, todo2):
        pass

    def setFishingRod(self, todo0):
        pass
    
    def setMaxFishingRod(self, todo0):
        pass
