"""ZoneEntityAI module: contains the ZoneEntityAI class"""

from . import ZoneEntityBase

class ZoneEntityAI(ZoneEntityBase.ZoneEntityBase):
    def __init__(self, level, entId):
        ZoneEntityBase.ZoneEntityBase.__init__(self, level, entId)

        # allocate a network zoneId for this zone
        # there is error checking in air.allocateZone
        self.setZoneId(self.level.air.allocateZone())
        
    def destroy(self):
        if not self.isUberZone():
            self.level.air.deallocateZone(self.getZoneId())
        ZoneEntityBase.ZoneEntityBase.destroy(self)
