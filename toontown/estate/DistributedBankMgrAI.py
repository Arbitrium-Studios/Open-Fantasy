
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBankMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBankMgrAI")

    def transferMoney(self, todo0):
        pass

