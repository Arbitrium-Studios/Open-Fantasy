from . import DistributedSZTreasure


class DistributedETreasure(DistributedSZTreasure.DistributedSZTreasure):

    def __init__(self, cr):
        DistributedSZTreasure.DistributedSZTreasure.__init__(self, cr)
        self.modelPath = '../../user/default/resources/default/phase_4/models/props/icecream'
        self.grabSoundPath = '../../user/default/resources/default/phase_4/audio/sfx/SZ_DD_treasure.ogg'
