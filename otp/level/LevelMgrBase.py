"""LevelMgrBase module: contains the LevelMgrBase class"""

from . import Entity

class LevelMgrBase(Entity.Entity):
    """This class contains LevelMgr code shared by the AI and client"""
    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)

    def destroy(self):
        Entity.Entity.destroy(self)
        self.ignoreAll()
