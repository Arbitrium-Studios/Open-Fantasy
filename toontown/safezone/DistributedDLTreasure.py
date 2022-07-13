from . import DistributedSZTreasure


class DistributedDLTreasure(DistributedSZTreasure.DistributedSZTreasure):

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = 'user/resources/default/phase_8/models/props/zzz_treasure'
        self.grabSoundPath = 'user/resources/default/phase_4/audio/sfx/SZ_DD_treasure.ogg'
