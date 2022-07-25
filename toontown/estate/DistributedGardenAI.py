from otp.ai.AIBase import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObjectAI
from . import DistributedHouseAI
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task
import random
import pickle
from . import HouseGlobals

class DistributedGardenAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenAI")

    def sendNewProp(self, todo0, todo1, todo2, todo3):
        pass

