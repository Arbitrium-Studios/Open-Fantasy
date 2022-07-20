from toontown.parties.DistributedPartyCogActivity import DistributedPartyCogActivity


class DistributedPartyWinterCogActivity(DistributedPartyCogActivity):

    def __init__(self, cr):
        DistributedPartyCogActivity.__init__(
            self, cr, '../../user/default/resources/default/phase_13/models/parties/tt_m_ara_pty_cogPieArenaWinter')
