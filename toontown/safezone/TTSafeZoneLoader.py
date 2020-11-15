from toontown.safezone import SafeZoneLoader
from toontown.safezone import TTPlayground
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from panda3d.core import DecalEffect, TextEncoder, CollisionNode
from toontown.suit import Suit, SuitDNA
from otp.nametag.NametagConstants import CFSpeech, CFTimeout


class TTSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        # should use an index for the crates... NAH
        self.crate1 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate2 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate3 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate4 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate5 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate6 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate7 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate8 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate9 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate10 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate11 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate12 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate13 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate14 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate15 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate16 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate17 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate18 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate19 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate20 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate21 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate22 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.crate23 = loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.toontrop = loader.loadModel('phase_4/models/neighborhoods/toontropolis')
        self.tropthall = loader.loadModel('phase_4/models/modules/toonhall')
        self.troplib = loader.loadModel('phase_4/models/modules/library')
        self.tropbank = loader.loadModel('phase_4/models/modules/bank')
        self.trophq = loader.loadModel('phase_3.5/models/modules/hqTT')
        self.gagshop = loader.loadModel('phase_4/models/modules/gagShop_TT')
        self.clothes = loader.loadModel('phase_4/models/modules/clothshopTT')
        self.petshop = loader.loadModel('phase_4/models/modules/PetShopExterior_TT')
        self.parkour = Sequence(Parallel(LerpPosInterval(self.crate17, 8, (87, 16, 30)),
                                         LerpPosInterval(self.crate17, 8, (87, 16, 15)),
                                         LerpPosInterval(self.crate18, 8, (87, 8, 15)),
                                         LerpPosInterval(self.crate18, 8, (87, 8, 30)),
                                         LerpPosInterval(self.crate19, 8, (87, 0, 30)),
                                         LerpPosInterval(self.crate19, 8, (87, 0, 15)),
                                         LerpPosInterval(self.crate20, 8, (87, -8, 15)),
                                         LerpPosInterval(self.crate20, 8, (87, -8, 30)),
                                         LerpPosInterval(self.crate21, 8, (87, -16, 30)),
                                         LerpPosInterval(self.crate21, 8, (87, -16, 15)),
                                         LerpPosInterval(self.crate22, 8, (87, -24, 15)),
                                         LerpPosInterval(self.crate22, 8, (87, -24, 30)),
                                         ),
                                )
        self.parkour.loop()
        self.dna = SuitDNA.SuitDNA()
        self.suit = Suit.Suit()
        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg',
                                            'phase_4/audio/sfx/SZ_TC_bird2.ogg',
                                            'phase_4/audio/sfx/SZ_TC_bird3.ogg'])
        self.wall = base.loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.wall2 = base.loader.loadModel('phase_9/models/cogHQ/woodCrateB')
        self.bossroom = loader.loadModel('phase_10/models/cashbotHQ/ZONE18a')
        self.playgroundClass = TTPlayground.TTPlayground
        self.musicFile = 'phase_4/audio/bgm/TC_nbrhood.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
        self.dnaFile = 'phase_4/dna/toontown_central_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_4/dna/storage_TT_sz.pdna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        bank = self.geom.find('**/*toon_landmark_TT_bank_DNARoot')
        library = self.geom.find('**/library/square_drop_shadow')
        door_trigger = bank.find('**/door_trigger*')
        door_trigger.setY(door_trigger.getY() - 1.5)
        library.find('**/building_front').setY(0.3)
        library.find('**/front_entrance_flag').setY(0.1)

        self.toontrop.reparentTo(self.geom)
        self.toontrop.setPos(0, 0, 150)
        self.tropthall.reparentTo(self.geom)
        self.tropthall.setPosHpr(-117, -126, 145.899, -540, 0, 0)
        self.troplib.reparentTo(self.geom)
        self.troplib.setPosHpr(-50, -86, 146, -498.469, 0, 0)
        self.tropbank.reparentTo(self.geom)
        self.tropbank.setPosHpr(-195, -109, 146.188, -569.414, 0, 0)
        self.trophq.reparentTo(self.geom)
        self.trophq.setPos(68, 8, 158.717)
        self.gagshop.reparentTo(self.geom)
        self.gagshop.setPosHpr(-3, 35, 159.072, -109, 0, 0)
        self.clothes.reparentTo(self.geom)
        self.clothes.setPosHprScale(17, -43, 158.858, -227.220, 0, 0, 1.2, 1, 1)
        self.petshop.reparentTo(self.geom)
        self.petshop.setPosHprScale(128, -55, 158, -500.300, 0, 2, 2, 2, 2)
        self.crate1.setPosHprScale(114, 125, 2.525, -925, 0, 0, 0.7, 0.7, 0.7)
        self.crate1.reparentTo(self.geom)
        self.crate2.setPosHprScale(109, 118, 4, -597, 0, 0, 0.7, 0.7, 0.7)
        self.crate2.reparentTo(self.geom)
        self.crate3.setPosHprScale(98, 111, 6, -607, 0, 0, 0.7, 0.7, 0.7)
        self.crate3.reparentTo(self.geom)
        self.crate4.setPosHprScale(87, 107, 8, -629, 0, 0, 0.7, 0.7, 0.7)
        self.crate4.reparentTo(self.geom)
        self.crate5.setPosHprScale(75, 107, 8, -629, 0, 0, 0.7, 0.7, 0.7)
        self.crate5.reparentTo(self.geom)
        self.crate6.setPosHprScale(64, 108, 10, -234, 0, 0, 0.7, 0.7, 0.7)
        self.crate6.reparentTo(self.geom)
        self.crate7.setPosHprScale(53, 99, 12, -193, 0, 0, 0.7, 0.7, 0.7)
        self.crate7.reparentTo(self.geom)
        self.crate8.setPosHprScale(52, 88, 14, 141, 0, 0, 0.7, 0.7, 0.7)
        self.crate8.reparentTo(self.geom)
        self.crate9.setPosHprScale(42, 76, 16, -180, 0, 0, 0.7, 0.7, 0.7)
        self.crate9.reparentTo(self.geom)
        self.crate10.setPosHprScale(41, 60, 18, -154, 0, 0, 0.7, 0.7, 0.7)
        self.crate10.reparentTo(self.geom)
        self.crate11.setPosHprScale(46, 49, 20, -166, 0, 0, 0.7, 0.7, 0.7)
        self.crate11.reparentTo(self.geom)
        self.crate12.setPosHprScale(49, 34, 22, -132, 0, 0, 0.7, 0.7, 0.7)
        self.crate12.reparentTo(self.geom)
        self.crate13.setPosHprScale(62, 28, 18, -75, 0, 0, 0.7, 0.7, 0.7)
        self.crate13.reparentTo(self.geom)
        self.crate14.setPosHprScale(70, 31, 22, -91, 0, 0, 0.7, 0.7, 0.7)
        self.crate14.reparentTo(self.geom)
        self.crate15.setPosHprScale(79, 27, 22, -91, 45, 0, 0.7, 0.7, 0.7)
        self.crate15.reparentTo(self.geom)
        self.crate16.setPosHprScale(82, 27, 20, -91, 0, 0, 0.7, 0.7, 0.7)
        self.crate16.reparentTo(self.geom)
        self.crate17.setPos(87, 16, 30)
        self.crate17.reparentTo(self.geom)
        self.crate18.setPos(87, 8, 15)
        self.crate18.reparentTo(self.geom)
        self.crate19.setPos(87, 0, 30)
        self.crate19.reparentTo(self.geom)
        self.crate20.setPos(87, -8, 15)
        self.crate20.reparentTo(self.geom)
        self.crate21.setPos(87, -16, 30)
        self.crate21.reparentTo(self.geom)
        self.crate22.setPos(87, -24, 15)
        self.crate22.reparentTo(self.geom)
        self.crate23.setPosHprScale(87, -35, 27, -90, 0, 0, 0.7, 0.7, 0.7)
        self.crate23.reparentTo(self.geom)
        self.bossroom.reparentTo(render),
        self.bossroom.setPosHprScale(2000, 2000, 4, -180, 0, 0, 10, 0.8, 1),
        self.wall.setPosHprScale(1982, 2017.4, 4.025, 180, 0, 0, 27, 0.001, 2.73),
        self.wall.reparentTo(render),
        self.wall2.setPosHprScale(1760.1, 1999.5, 4, 90, 0, 0, 2.3, 0.001, 2.80)
        self.wall2.reparentTo(render),

        self.dna.newSuit('tbc')
        self.suit.setDNA(self.dna)
        self.suit.reparentTo(render)
        self.suit.loop('neutral')
        self.suit.setPosHpr(138.435, 67.946, 2.525, -305, 0, 0)
        self.suit.initializeBodyCollisions('suitCollisions')
        self.accept('entersuitCollisions', self.enter_bosscog)
        return

    def enter_bosscog(self, collId):
        self.music = base.loadMusic('phase_12/audio/bgm/BossBot_CEO_v2.ogg')
        base.playMusic(self.music, looping=1, volume=2)
        base.localAvatar.setPosHpr(1774.979, 1999.318, 4.0, 270, 0, 0),
        self.suit.setPosHpr(2192.691, 1999.5, 4.025, 90, 0, 0)
        self.boss_fight = Sequence(PosInterval(self.crate1, (2177, 2014.5, 4.025)),
                                   PosInterval(self.crate2, (2177, 2008.5, 4.025)),
                                   PosInterval(self.crate3, (2177, 2002.5, 4.025)),
                                   PosInterval(self.crate4, (2177, 1996.5, 4.025)),
                                   PosInterval(self.crate5, (2177, 1990.5, 4.025)),
                                   PosInterval(self.crate6, (2177, 1984.5, 4.025)),
                                   HprInterval(self.crate1, (0, 0, 0)),
                                   HprInterval(self.crate2, (0, 0, 0)),
                                   HprInterval(self.crate3, (0, 0, 0)),
                                   HprInterval(self.crate4, (0, 0, 0)),
                                   HprInterval(self.crate5, (0, 0, 0)),
                                   HprInterval(self.crate6, (0, 0, 0)),
                                   Parallel(LerpPosInterval(self.crate1, 2, (1810, 2014.5, 4.025)),
                                            LerpPosInterval(self.crate3, 2, (1810, 2002.5, 4.025)),
                                            LerpPosInterval(self.crate5, 2, (1810, 1990.5, 4.025))),
                                   Parallel(LerpPosInterval(self.crate2, 2, (1810, 2008.5, 4.025)),
                                            LerpPosInterval(self.crate4, 2, (1810, 1996.5, 4.025)),
                                            LerpPosInterval(self.crate6, 2, (1810, 1984.5, 4.025))),
                                   Parallel(LerpPosInterval(self.crate1, 2, (2177, 2014.5, 4.025)),
                                            LerpPosInterval(self.crate3, 2, (2177, 2002.5, 4.025)),
                                            LerpPosInterval(self.crate5, 2, (2177, 1990.5, 4.025))),
                                   Parallel(LerpPosInterval(self.crate2, 2, (2177, 2008.5, 4.025)),
                                            LerpPosInterval(self.crate4, 2, (2177, 1996.5, 4.025)),
                                            LerpPosInterval(self.crate6, 2, (2177, 1984.5, 4.025))),
                                   )
        self.boss_fight.loop()
        #self.suit.initializeBodyCollisions('crateCollisions')
        #self.accept('entercrateCollisions', self.enter_endboss)
        #return

        self.suit.initializeBodyCollisions('suitCollisions')
        self.accept('entersuitCollisions', self.enter_endboss)
        return

        #def enter_crate(self, collId):
        #    base.localAvatar.setPos(0, 0, 0),
        #return

        #self.suit.initializeBodyCollisions('suitCollisions')
        #self.accept('entersuitCollisions', self.enter_endboss)
        #return

    def enter_endboss(self, collId):
        self.ttcmusic = base.loadMusic('phase_4/audio/bgm/TC_nbrhood')
        base.playMusic(self.ttcmusic, looping=1, volume=2)
        self.suit.setPosHpr(138.435, 67.946, 2.525, -305, 0, 0)
        base.localAvatar.setPosHpr(129.685,  82.496,  2.525, 35, 0, 0)
        self.suit.initializeBodyCollisions('suitCollisions')
        self.accept('entersuitCollisions', self.enter_bosscog)
        return

    def unload(self):
        del self.toontrop
        del self.tropthall
        del self.troplib
        del self.tropbank
        del self.trophq
        del self.gagshop
        del self.clothes
        del self.petshop
        del self.crate1
        del self.crate2
        del self.crate3
        del self.crate4
        del self.crate5
        del self.crate6
        del self.crate7
        del self.crate8
        del self.crate9
        del self.crate10
        del self.crate11
        del self.crate12
        del self.crate13
        del self.crate14
        del self.crate15
        del self.crate16
        del self.crate17
        del self.crate18
        del self.crate19
        del self.crate20
        del self.crate21
        del self.crate22
        del self.crate23
        del self.bossroom
        self.suit.cleanup()
        del self.suit
