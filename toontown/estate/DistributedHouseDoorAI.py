""" DistributedHouseDoorAI module:  a child of the DistributedDoorAI class """


from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *

from direct.directnotify import DirectNotifyGlobal

from toontown.building.DistributedDoorAI import DistributedDoorAI


class DistributedHouseDoorAI(DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHouseDoorAI')
