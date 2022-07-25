from direct.interval.IntervalGlobal import *
from . import CatalogAtticItem
from . import CatalogItem
import random, glob
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from panda3d.core import *
FTModelName = 0
FTColor = 1
FTColorOptions = 2
FTBasePrice = 3
FTFlags = 4
FTScale = 5

FLBank = 1
FLCloset = 2
FLRug = 4
FLPainting = 8
FLOnTable = 16
FLIsTable = 32
FLBillboard = 64
FLPhone = 128
FLCrate = 256
FLChair = 512
FLTV = 1024
FLTrunk = 2048
FLBoysOnly = 4096
FLGirlsOnly = 8192
furnitureColors = [
  (0.792, 0.353, 0.29, 1.0),
  (0.176, 0.592, 0.439, 1.0),
  (0.439, 0.424, 0.682, 1.0),
  (0.325, 0.58, 0.835, 1.0),
  (0.753, 0.345, 0.557, 1.0),
  (0.992, 0.843, 0.392, 1.0)
]
woodColors = [
  (0.933, 0.773, 0.569, 1.0),
  (0.9333, 0.6785, 0.055, 1.0),
  (0.545, 0.451, 0.333, 1.0),
  (0.541, 0.0, 0.0, 1.0),
  (0.5451, 0.2706, 0.0745, 1.0),
  (0.5451, 0.4118, 0.4118, 1.0)
]
BankToMoney = {
 1300: 10000,
 1310: 15000,
 1320: 20000,
 1330: 25000,
 1340: 30000
}
MoneyToBank = {}
for bankId, maxMoney in list(BankToMoney.items()):
    MoneyToBank[maxMoney] = bankId
MaxBankId = 1340

MaxBankId = 1340
ClosetToClothes = {
 500: 10,
 502: 15,
 504: 20,
 506: 25,
 508: 50,
 510: 10,
 512: 15,
 514: 20,
 516: 25,
 518: 50
}
ClothesToCloset = {}
for closetId, maxClothes in list(ClosetToClothes.items()):
    if not maxClothes in ClothesToCloset:
        ClothesToCloset[maxClothes] = (closetId,)
    else:
        ClothesToCloset[maxClothes] += (closetId,)
MaxClosetIds = (508, 518)

TvToPosScale = {
 1530: ((-1.15, -0.5, 1.1), (2.5, 1.7, 1.4)),
 1531: ((-2.3, -0.2, 2.522), (5, 3.75, 3.187)),
 1532: ((-7, -0.2, 2.8), (15, 10, 7.8))
}

ChairToPosHpr = {
 100: ((0, -3.9, 0.88), (180, 0, 0), (0, -4.9, 0), -3.0),
 105: ((0, -3.9, 0.88), (180, 0, 0), (0, -4.9, 0), -3.0),
 110: ((0, -1.6, 0.5), (180, 0, 0), (0, -2.6, 0), 0.0),
 120: ((0, -1.6, 0.5), (180, 0, 0), (0, -2.6, 0), 0.0),
 130: ((0, -2.8, 0.5), (180, 0, 0), (0, -3.8, 0), -2.0),
 140: ((0, -1.6, 0.5), (180, 0, 0), (0, -2.6, 0), 0.0),
 145: ((0, -2.1, 0.2), (180, 0, 0), (0, -3.1, 0), 0.0),
 160: ((-1.7, 0, 0.9), (90, 0, 0), (-2.7, 0, 0), 0.0),
 170: ((0, 1.8, 0.4), (0, 0, 0), (0, 2.8, 0), 0.0),
 700: ((0, -1.2, 0.5), (180, 0, 0), (0, -2.2, 0), 0.0),
 705: ((0, -1.2, 0.5), (180, 0, 0), (0, -2.2, 0), 0.0),
 710: ((0, -1.1, 0.4), (180, 0, 0), (0, -2.1, 0), 0.0),
 715: ((0, -1.1, 0.4), (180, 0, 0), (0, -2.1, 0), 0.0),
 720: ((0, -2.7, 0.2), (180, 0, 0), (0, -3.7, 0), -3.0)
}

FurnitureTypes = {
 100: ('phase_5.5/models/estate/chairA',  # Model
       None,                              # Color
       None,                              # Color Options
       80,                                # Base Price
       FLChair),                          # Flags
                                          # Scale
 105: ('phase_5.5/models/estate/chairAdesat',
       None,
       {0: (('**/cushion*', furnitureColors[0]), ('**/arm*', furnitureColors[0])),
        1: (('**/cushion*', furnitureColors[1]), ('**/arm*', furnitureColors[1])),
        2: (('**/cushion*', furnitureColors[2]), ('**/arm*', furnitureColors[2])),
        3: (('**/cushion*', furnitureColors[3]), ('**/arm*', furnitureColors[3])),
        4: (('**/cushion*', furnitureColors[4]), ('**/arm*', furnitureColors[4])),
        5: (('**/cushion*', furnitureColors[5]), ('**/arm*', furnitureColors[5]))},
       160,
       FLChair),
 110: ('phase_3.5/models/modules/chair',
       None,
       None,
       40,
       FLChair),
 120: ('phase_5.5/models/estate/deskChair',
       None,
       None,
       60,
       FLChair),
 130: ('phase_5.5/models/estate/BugRoomChair',
       None,
       None,
       160,
       FLChair),
 140: ('phase_5.5/models/estate/UWlobsterChair',
       None,
       None,
       200,
       FLChair),
 145: ('phase_5.5/models/estate/UWlifeSaverChair',
       None,
       None,
       200,
       FLChair),
 150: ('phase_5.5/models/estate/West_saddleStool2',
       None,
       None,
       160),
 160: ('phase_5.5/models/estate/West_nativeChair',
       None,
       None,
       160,
       FLChair),
 170: ('phase_5.5/models/estate/cupcakeChair',
       None,
       None,
       240,
       FLChair),
 200: ('phase_5.5/models/estate/regular_bed',
       None,
       None,
       400),
 205: ('phase_5.5/models/estate/regular_bed_desat',
       None,
       {0: (('**/bar*', woodColors[0]),
            ('**/post*', woodColors[0]),
            ('**/*support', woodColors[0]),
            ('**/top', woodColors[0]),
            ('**/bottom', woodColors[0]),
            ('**/pPlane*', woodColors[0])),
        1: (('**/bar*', woodColors[1]),
            ('**/post*', woodColors[1]),
            ('**/*support', woodColors[1]),
            ('**/top', woodColors[1]),
            ('**/bottom', woodColors[1]),
            ('**/pPlane*', woodColors[1])),
        2: (('**/bar*', woodColors[2]),
            ('**/post*', woodColors[2]),
            ('**/*support', woodColors[2]),
            ('**/top', woodColors[2]),
            ('**/bottom', woodColors[2]),
            ('**/pPlane*', woodColors[2])),
        3: (('**/bar*', woodColors[3]),
            ('**/post*', woodColors[3]),
            ('**/*support', woodColors[3]),
            ('**/top', woodColors[3]),
            ('**/bottom', woodColors[3]),
            ('**/pPlane*', woodColors[3])),
        4: (('**/bar*', woodColors[4]),
            ('**/post*', woodColors[4]),
            ('**/*support', woodColors[4]),
            ('**/top', woodColors[4]),
            ('**/bottom', woodColors[4]),
            ('**/pPlane*', woodColors[4])),
        5: (('**/bar*', woodColors[5]),
            ('**/post*', woodColors[5]),
            ('**/*support', woodColors[5]),
            ('**/top', woodColors[5]),
            ('**/bottom', woodColors[5]),
            ('**/pPlane*', woodColors[5]))},
       800),
 210: ('phase_5.5/models/estate/girly_bed',
       None,
       None,
       450,
       FLGirlsOnly),
 220: ('phase_5.5/models/estate/bathtub_bed',
       None,
       None,
       550),
 230: ('phase_5.5/models/estate/bugRoomBed',
       None,
       None,
       600),
 240: ('phase_5.5/models/estate/UWBoatBed',
       None,
       None,
       600),
 250: ('phase_5.5/models/estate/West_cactusHammoc',
       None,
       None,
       550),
 260: ('phase_5.5/models/estate/icecreamBed',
       None,
       None,
       700),
 270: ('phase_5.5/models/estate/trolley_bed',
       None,
       None,
       1200,
       None,
       None,
       0.25),
 300: ('phase_5.5/models/estate/Piano',
       None,
       None,
       1000,
       FLIsTable),
 310: ('phase_5.5/models/estate/Organ',
       None,
       None,
       2500),
 400: ('phase_5.5/models/estate/FireplaceSq',
       None,
       None,
       800),
 410: ('phase_5.5/models/estate/FireplaceGirlee',
       None,
       None,
       800,
       FLGirlsOnly),
 420: ('phase_5.5/models/estate/FireplaceRound',
       None,
       None,
       800),
 430: ('phase_5.5/models/estate/bugRoomFireplace',
       None,
       None,
       800),
 440: ('phase_5.5/models/estate/CarmelAppleFireplace',
       None,
       None,
       800),
 450: ('phase_5.5/models/estate/fireplace_coral',
       None,
       None,
       950),
 460: ('phase_5.5/models/estate/tt_m_prp_int_fireplace_coral',
       None,
       None,
       1250,
       None,
       None,
       0.5),
 470: ('phase_5.5/models/estate/tt_m_prp_int_fireplace_square',
       None,
       None,
       1100,
       None,
       None,
       0.5),
 480: ('phase_5.5/models/estate/tt_m_prp_int_fireplace_round',
       None,
       None,
       1100,
       None,
       None,
       0.5),
 490: ('phase_5.5/models/estate/tt_m_prp_int_fireplace_girlee',
       None,
       None,
       1100,
       FLGirlsOnly,
       None,
       0.5),
 491: ('phase_5.5/models/estate/tt_m_prp_int_fireplace_bugRoom',
       None,
       None,
       1100,
       None,
       None,
       0.5),
 492: ('phase_5.5/models/estate/tt_m_prp_int_fireplace_caramelApple',
       None,
       None,
       1100,
       None,
       None,
       0.5),
 500: ('phase_5.5/models/estate/closetBoy',
       None,
       None,
       500,
       FLCloset,
       0.85),
 502: ('phase_5.5/models/estate/closetBoy',
       None,
       None,
       500,
       FLCloset,
       1.0),
 504: ('phase_5.5/models/estate/closetBoy',
       None,
       None,
       500,
       FLCloset,
       1.15),
 506: ('phase_5.5/models/estate/closetBoy',
       None,
       None,
       500,
       FLCloset,
       1.3),
 508: ('phase_5.5/models/estate/closetBoy',
       None,
       None,
       500,
       FLCloset,
       1.3),
 510: ('phase_5.5/models/estate/closetGirl',
       None,
       None,
       500,
       FLCloset,
       0.85),
 512: ('phase_5.5/models/estate/closetGirl',
       None,
       None,
       500,
       FLCloset,
       1.0),
 514: ('phase_5.5/models/estate/closetGirl',
       None,
       None,
       500,
       FLCloset,
       1.15),
 516: ('phase_5.5/models/estate/closetGirl',
       None,
       None,
       500,
       FLCloset,
       1.3),
 518: ('phase_5.5/models/estate/closetGirl',
       None,
       None,
       500,
       FLCloset,
       1.3),
 600: ('phase_3.5/models/modules/lamp_short',
       None,
       None,
       45,
       FLOnTable),
 610: ('phase_3.5/models/modules/lamp_tall',
       None,
       None,
       45),
 620: ('phase_5.5/models/estate/lampA',
       None,
       None,
       35,
       FLOnTable),
 625: ('phase_5.5/models/estate/lampADesat',
       None,
       {0: (('**/top', furnitureColors[0]),),
        1: (('**/top', furnitureColors[1]),),
        2: (('**/top', furnitureColors[2]),),
        3: (('**/top', furnitureColors[3]),),
        4: (('**/top', furnitureColors[4]),),
        5: (('**/top', furnitureColors[5]),)},
       70,
       FLOnTable),
 630: ('phase_5.5/models/estate/bugRoomDaisyLamp1',
       None,
       None,
       55),
 640: ('phase_5.5/models/estate/bugRoomDaisyLamp2',
       None,
       None,
       55),
 650: ('phase_5.5/models/estate/UWlamp_jellyfish',
       None,
       None,
       55,
       FLOnTable),
 660: ('phase_5.5/models/estate/UWlamps_jellyfishB',
       None,
       None,
       55,
       FLOnTable),
 670: ('phase_5.5/models/estate/West_cowboyLamp',
       None,
       None,
       55,
       FLOnTable),
 680: ('phase_5.5/models/estate/tt_m_ara_int_candlestick',
       None,
       {0: (('**/candlestick/candlestick', (1.0,
              1.0,
              1.0,
              1.0)),),
        1: (('**/candlestick/candlestick', furnitureColors[1]),),
        2: (('**/candlestick/candlestick', furnitureColors[2]),),
        3: (('**/candlestick/candlestick', furnitureColors[3]),),
        4: (('**/candlestick/candlestick', furnitureColors[4]),),
        5: (('**/candlestick/candlestick', furnitureColors[5]),),
        6: (('**/candlestick/candlestick', furnitureColors[0]),)},
       20,
       FLOnTable),
 681: ('phase_5.5/models/estate/tt_m_ara_int_candlestickLit',
       None,
       {0: (('**/candlestick/candlestick', (1.0,
              1.0,
              1.0,
              1.0)),),
        1: (('**/candlestickLit/candlestick', furnitureColors[1]),),
        2: (('**/candlestickLit/candlestick', furnitureColors[2]),),
        3: (('**/candlestickLit/candlestick', furnitureColors[3]),),
        4: (('**/candlestickLit/candlestick', furnitureColors[4]),),
        5: (('**/candlestickLit/candlestick', furnitureColors[5]),),
        6: (('**/candlestickLit/candlestick', furnitureColors[0]),)},
       25,
       FLOnTable),
 700: ('phase_3.5/models/modules/couch_1person',
       None,
       None,
       230,
       FLChair),
 705: ('phase_5.5/models/estate/couch_1personDesat',
       None,
       {0: (('**/*couch', furnitureColors[0]),),
        1: (('**/*couch', furnitureColors[1]),),
        2: (('**/*couch', furnitureColors[2]),),
        3: (('**/*couch', furnitureColors[3]),),
        4: (('**/*couch', furnitureColors[4]),),
        5: (('**/*couch', furnitureColors[5]),)},
       460,
       FLChair),
 710: ('phase_3.5/models/modules/couch_2person',
       None,
       None,
       230,
       FLChair),
 715: ('phase_5.5/models/estate/couch_2personDesat',
       None,
       {0: (('**/*couch', furnitureColors[0]),),
        1: (('**/*couch', furnitureColors[1]),),
        2: (('**/*couch', furnitureColors[2]),),
        3: (('**/*couch', furnitureColors[3]),),
        4: (('**/*couch', furnitureColors[4]),),
        5: (('**/*couch', furnitureColors[5]),)},
       460,
       FLChair),
 720: ('phase_5.5/models/estate/West_HayCouch',
       None,
       None,
       420,
       FLChair),
 730: ('phase_5.5/models/estate/twinkieCouch',
       None,
       None,
       480),
 800: ('phase_3.5/models/modules/desk_only_wo_phone',
       None,
       None,
       65,
       FLIsTable),
 810: ('phase_5.5/models/estate/BugRoomDesk',
       None,
       None,
       125,
       FLIsTable),
 900: ('phase_3.5/models/modules/umbrella_stand',
       None,
       None,
       30),
 910: ('phase_3.5/models/modules/coatrack',
       None,
       None,
       75),
 920: ('phase_3.5/models/modules/paper_trashcan',
       None,
       None,
       30),
 930: ('phase_5.5/models/estate/BugRoomRedMushroomPot',
       None,
       None,
       60),
 940: ('phase_5.5/models/estate/BugRoomYellowMushroomPot',
       None,
       None,
       60),
 950: ('phase_5.5/models/estate/UWcoralClothRack',
       None,
       None,
       75),
 960: ('phase_5.5/models/estate/west_barrelStand',
       None,
       None,
       75),
 970: ('phase_5.5/models/estate/West_fatCactus',
       None,
       None,
       75),
 980: ('phase_5.5/models/estate/West_Tepee',
       None,
       None,
       150),
 990: ('phase_5.5/models/estate/gag_fan',
       None,
       None,
       500,
       None,
       None,
       0.5),
 1000: ('phase_3.5/models/modules/rug',
        None,
        None,
        75,
        FLRug),
 1010: ('phase_5.5/models/estate/rugA',
        None,
        None,
        75,
        FLRug),
 1015: ('phase_5.5/models/estate/rugADesat',
        None,
        {0: (('**/pPlane*', furnitureColors[0]),),
         1: (('**/pPlane*', furnitureColors[1]),),
         2: (('**/pPlane*', furnitureColors[2]),),
         3: (('**/pPlane*', furnitureColors[3]),),
         4: (('**/pPlane*', furnitureColors[4]),),
         5: (('**/pPlane*', furnitureColors[5]),)},
        150,
        FLRug),
 1020: ('phase_5.5/models/estate/rugB',
        None,
        None,
        75,
        FLRug,
        2.5),
 1030: ('phase_5.5/models/estate/bugRoomLeafMat',
        None,
        None,
        75,
        FLRug),
 1040: ('phase_5.5/models/estate/tt_m_ara_int_presents',
        None,
        None,
        300),
 1050: ('phase_5.5/models/estate/tt_m_ara_int_sled',
        None,
        None,
        400),
 1100: ('phase_5.5/models/estate/cabinetRwood',
        None,
        None,
        825),
 1110: ('phase_5.5/models/estate/cabinetYwood',
        None,
        None,
        825),
 1120: ('phase_3.5/models/modules/bookcase',
        None,
        None,
        650,
        FLIsTable),
 1130: ('phase_3.5/models/modules/bookcase_low',
        None,
        None,
        650,
        FLIsTable),
 1140: ('phase_5.5/models/estate/icecreamChest',
        None,
        None,
        750),
 1200: ('phase_3.5/models/modules/ending_table',
        None,
        None,
        60,
        FLIsTable),
 1210: ('phase_5.5/models/estate/table_radio',
        None,
        None,
        60,
        FLIsTable,
        50.0),
 1215: ('phase_5.5/models/estate/table_radioDesat',
        None,
        {0: (('**/RADIOTABLE_*', woodColors[0]),),
         1: (('**/RADIOTABLE_*', woodColors[1]),),
         2: (('**/RADIOTABLE_*', woodColors[2]),),
         3: (('**/RADIOTABLE_*', woodColors[3]),),
         4: (('**/RADIOTABLE_*', woodColors[4]),),
         5: (('**/RADIOTABLE_*', woodColors[5]),)},
        120,
        FLIsTable,
        50.0),
 1220: ('phase_5.5/models/estate/coffeetableSq',
        None,
        None,
        180,
        FLIsTable),
 1230: ('phase_5.5/models/estate/coffeetableSq_BW',
        None,
        None,
        180,
        FLIsTable),
 1240: ('phase_5.5/models/estate/UWtable',
        None,
        None,
        180,
        FLIsTable),
 1250: ('phase_5.5/models/estate/cookieTableA',
        None,
        None,
        220,
        FLIsTable),
 1260: ('phase_5.5/models/estate/TABLE_Bedroom_Desat',
        None,
        {0: (('**/Bedroom_Table', woodColors[0]),),
         1: (('**/Bedroom_Table', woodColors[1]),),
         2: (('**/Bedroom_Table', woodColors[2]),),
         3: (('**/Bedroom_Table', woodColors[3]),),
         4: (('**/Bedroom_Table', woodColors[4]),),
         5: (('**/Bedroom_Table', woodColors[5]),)},
        220,
        FLIsTable),
 1300: ('phase_5.5/models/estate/jellybeanBank',
        None,
        None,
        5000,
        FLBank,
        1.0),
 1310: ('phase_5.5/models/estate/jellybeanBank',
        None,
        None,
        7500,
        FLBank,
        1.0),
 1320: ('phase_5.5/models/estate/jellybeanBank',
        None,
        None,
        10000,
        FLBank,
        1.0),
 1330: ('phase_5.5/models/estate/jellybeanBank',
        None,
        None,
        12500,
        FLBank,
        1.0),
 1340: ('phase_5.5/models/estate/jellybeanBank',
        None,
        None,
        15000,
        FLBank,
        1.0),
 1399: ('phase_5.5/models/estate/prop_phone-mod',
        None,
        None,
        0,
        FLPhone),
 1400: ('phase_5.5/models/estate/cezanne_toon',
        None,
        None,
        425,
        FLPainting,
        2.0),
 1410: ('phase_5.5/models/estate/flowers',
        None,
        None,
        425,
        FLPainting,
        2.0),
 1420: ('phase_5.5/models/estate/modernistMickey',
        None,
        None,
        425,
        FLPainting,
        2.0),
 1430: ('phase_5.5/models/estate/rembrandt_toon',
        None,
        None,
        425,
        FLPainting,
        2.0),
 1440: ('phase_5.5/models/estate/landscape',
        None,
        None,
        425,
        FLPainting,
        100.0),
 1441: ('phase_5.5/models/estate/whistler-horse',
        None,
        None,
        425,
        FLPainting,
        2.0),
 1442: ('phase_5.5/models/estate/degasHorseStar',
        None,
        None,
        425,
        FLPainting,
        2.5),
 1443: ('phase_5.5/models/estate/MagPie',
        None,
        None,
        425,
        FLPainting,
        2.0),
 1450: ('phase_5.5/models/estate/tt_m_prp_int_painting_valentine',
        None,
        None,
        425,
        FLPainting),
 1500: ('phase_5.5/models/estate/RADIO_A',
        None,
        None,
        25,
        FLOnTable,
        15.0),
 1510: ('phase_5.5/models/estate/RADIO_B',
        None,
        None,
        25,
        FLOnTable,
        15.0),
 1520: ('phase_5.5/models/estate/radio_c',
        None,
        None,
        25,
        FLOnTable,
        15.0),
 1530: ('phase_5.5/models/estate/bugRoomTV',
        None,
        None,
        675,
        FLTV),
 1531: ('phase_5.5/models/estate/bugRoomTV_50inch',
        None,
        None,
        1250,
        FLTV),
 1532: ('phase_5.5/models/estate/bugRoomTV_100inch',
        None,
        None,
        5000,
        FLTV),		
 1600: ('phase_5.5/models/estate/vaseA_short',
        None,
        None,
        120,
        FLOnTable),
 1610: ('phase_5.5/models/estate/vaseA_tall',
        None,
        None,
        120,
        FLOnTable),
 1620: ('phase_5.5/models/estate/vaseB_short',
        None,
        None,
        120,
        FLOnTable),
 1630: ('phase_5.5/models/estate/vaseB_tall',
        None,
        None,
        120,
        FLOnTable),
 1640: ('phase_5.5/models/estate/vaseC_short',
        None,
        None,
        120,
        FLOnTable),
 1650: ('phase_5.5/models/estate/vaseD_short',
        None,
        None,
        120,
        FLOnTable),
 1660: ('phase_5.5/models/estate/UWcoralVase',
        None,
        None,
        120,
        FLOnTable | FLBillboard),
 1661: ('phase_5.5/models/estate/UWshellVase',
        None,
        None,
        120,
        FLOnTable | FLBillboard),
 1670: ('phase_5.5/models/estate/tt_m_prp_int_roseVase_valentine',
        None,
        None,
        200,
        FLOnTable),
 1680: ('phase_5.5/models/estate/tt_m_prp_int_roseWatercan_valentine',
        None,
        None,
        200,
        FLOnTable),
 1700: ('phase_5.5/models/estate/popcornCart',
        None,
        None,
        400),
 1710: ('phase_5.5/models/estate/bugRoomLadyBug',
        None,
        None,
        260),
 1720: ('phase_5.5/models/estate/UWfountain',
        None,
        None,
        450),
 1725: ('phase_5.5/models/estate/UWOceanDryer',
        None,
        None,
        400),
 1800: ('phase_5.5/models/estate/UWskullBowl',
        None,
        None,
        120,
        FLOnTable),
 1810: ('phase_5.5/models/estate/UWlizardBowl',
        None,
        None,
        120,
        FLOnTable),
 1900: ('phase_5.5/models/estate/UWswordFish',
        None,
        None,
        425,
        FLPainting,
        0.5),
 1910: ('phase_5.5/models/estate/UWhammerhead',
        None,
        None,
        425,
        FLPainting),
 1920: ('phase_5.5/models/estate/West_hangingHorns',
        None,
        None,
        475,
        FLPainting),
 1930: ('phase_5.5/models/estate/West_Sombrero',
        None,
        None,
        425,
        FLPainting),
 1940: ('phase_5.5/models/estate/West_fancySombrero',
        None,
        None,
        450,
        FLPainting),
 1950: ('phase_5.5/models/estate/West_CoyotePawdecor',
        None,
        None,
        475,
        FLPainting),
 1960: ('phase_5.5/models/estate/West_Horseshoe',
        None,
        None,
        475,
        FLPainting),
 1970: ('phase_5.5/models/estate/West_bisonPortrait',
        None,
        None,
        475,
        FLPainting),
 2000: ('phase_5.5/models/estate/candySwingSet',
        None,
        None,
        300),
 2010: ('phase_5.5/models/estate/cakeSlide',
        None,
        None,
        200),
 3000: ('phase_5.5/models/estate/BanannaSplitShower',
        None,
        None,
        400),
 4000: ('phase_5.5/models/estate/tt_m_ara_est_accessoryTrunkBoy',
        None,
        None,
        0,
        FLTrunk,
        0.9),
 4010: ('phase_5.5/models/estate/tt_m_ara_est_accessoryTrunkGirl',
        None,
        None,
        0,
        FLTrunk,
        0.9),
 10000: ('phase_4/models/estate/pumpkin_short',
         None,
         None,
         200,
         FLOnTable),
 10010: ('phase_4/models/estate/pumpkin_tall',
         None,
         None,
         250,
         FLOnTable),
 10020: ('phase_5.5/models/estate/tt_m_prp_int_winter_tree',
         None,
         None,
         500,
         None,
         None,
         0.1),
 10030: ('phase_5.5/models/estate/tt_m_prp_int_winter_wreath',
         None,
         None,
         200,
         FLPainting),
 10040: ('phase_10/models/cashbotHQ/CBWoodCrate',
         None,
         None,
         0,
         FLCrate,
         0.5)
}

class CatalogFurnitureItem(CatalogAtticItem.CatalogAtticItem):
    """CatalogFurnitureItem

    This represents a piece of furniture that the player may purchase
    and store in his house or possibly in his lawn.  Each item of
    furniture corresponds to a particular model file (possibly with
    some pieces hidden and/or texture swapped); there may also be a
    number of user-customizable options for a given piece of furniture
    (e.g. changing colors).

    """
    
    def makeNewItem(self, furnitureType, colorOption = None, posHpr = None):
        self.furnitureType = furnitureType
        self.colorOption = colorOption
        self.posHpr = posHpr
        
        CatalogAtticItem.CatalogAtticItem.makeNewItem(self)

    def needsCustomize(self):
        return self.colorOption == None and FurnitureTypes[self.furnitureType][FTColorOptions] != None

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def replacesExisting(self):
        return self.getFlags() & (FLCloset | FLBank) != 0

    def hasExisting(self):
        # If replacesExisting returns true, this returns true if an
        # item of this class is already owned by the avatar, false
        # otherwise.  If replacesExisting returns false, this is
        # undefined.

        # We always have a closet and bank.
        return 1

    def getYourOldDesc(self):
        # If replacesExisting returns true, this returns the name of
        # the already existing object, in sentence construct: "your
        # old ...".  If replacesExisting returns false, this is undefined.
        
        if (self.getFlags() & FLCloset):
            return TTLocalizer.FurnitureYourOldCloset
        elif (self.getFlags() & FLBank):
            return TTLocalizer.FurnitureYourOldBank
        else:
            return None

    def notOfferedTo(self, avatar):
        if self.getFlags() & FLCloset:
            decade = self.furnitureType - self.furnitureType % 10
            forBoys = decade == 500
            if avatar.getStyle().getGender() == 'm':
                return not forBoys
            else:
                return forBoys
        if self.forBoysOnly():
            if avatar.getStyle().getGender() == 'm':
                return 0
            else:
                return 1
        elif self.forGirlsOnly():
            if avatar.getStyle().getGender() == 'f':
                return 0
            else:
                return 1
        return 0

    def forBoysOnly(self):
        return self.getFlags() & FLBoysOnly > 0

    def forGirlsOnly(self):
        return self.getFlags() & FLGirlsOnly > 0

    def isDeletable(self):
        # Returns true if the item can be deleted from the attic,
        # false otherwise.
        return (self.getFlags() & (FLBank | FLCloset | FLTrunk | FLPhone)) == 0


    def getMaxBankMoney(self):
        # This special method is only defined for bank type items,
        # and returns the capacity of the bank in jellybeans.
        return BankToMoney.get(self.furnitureType)

    def getMaxClothes(self):
        return ClosetToClothes[self.furnitureType]

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        if self.getFlags() & FLBank:
            # No point in buying an equal or smaller bank.
            if self.getMaxBankMoney() <= avatar.getMaxBankMoney():
                return 1

            # Also if this particular bank is on order, we don't need
            # another one.
            if self in avatar.onOrder or self in avatar.mailboxContents:
                return 1

        if self.getFlags() & FLCloset:
            # No point in buying an equal or smaller wardrobe.
            if self.getMaxClothes() <= avatar.getMaxClothes():
                return 1

            # Also if this particular wardrobe is on order, we don't need
            # another one.
            if self in avatar.onOrder or self in avatar.mailboxContents:
                return 1
        return 0

    def getTypeName(self):
        flags = self.getFlags()
        if flags & FLPainting:
            return TTLocalizer.PaintingTypeName
        else:
            return TTLocalizer.FurnitureTypeName

    def getName(self):
        return TTLocalizer.FurnitureNames[self.furnitureType]

    def getFlags(self):
        # Returns the special flag word associated with this furniture
        # item.  This controls special properties of the item, and is
        # one or more of the bits defined above with the symbols FL*.
        defn = FurnitureTypes[self.furnitureType]
        if FTFlags < len(defn):
            flag = defn[FTFlags]
            if flag == None:
                return 0
            else:
                return flag
        else:
            return 0
            
    def isGift(self):
        if self.getEmblemPrices():
            return 0
        if self.getFlags() & (FLCloset | FLBank):
            return 0
        else:
            return 1

    def recordPurchase(self, avatar, optional):
        # Updates the appropriate field on the avatar to indicate the
        # purchase (or delivery).  This makes the item available to
        # use by the avatar.  This method is only called on the AI side.
        house, retcode = self.getHouseInfo(avatar)
        if retcode >= 0:
            house.addAtticItem(self)
            if (self.getFlags() & FLBank):
                # A special case: if we just bought a new bank, change
                # our maximum bank money accordingly.  This property
                # is stored on the toon.
                avatar.b_setMaxBankMoney(self.getMaxBankMoney())
            if (self.getFlags() & FLCloset):
                if avatar.getMaxClothes() > self.getMaxClothes():
                    return ToontownGlobals.P_AlreadyOwnBiggerCloset
                # Another special case: if we just bought a new
                # wardrobe, change our maximum clothing items
                # accordingly.  This property is also stored on the
                # toon.
                avatar.b_setMaxClothes(self.getMaxClothes())
            if self.getFlags() & FLBank:
                avatar.b_setMaxBankMoney(self.getMaxBankMoney())
            house.addAtticItem(self)
        return retcode

    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 24 * 60  # 24 hours.

    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.
        model = self.loadModel()
        spin = 1

        flags = self.getFlags()
        if flags & FLRug:
            spin = 0
            model.setP(90)
        elif flags & FLPainting:
            spin = 0
        elif flags & FLBillboard:
            spin = 0
        model.setBin('unsorted', 0, 1)

##        assert (not self.hasPicture)
        self.hasPicture=True
        
        return self.makeFrameModel(model, spin)

    def output(self, store = -1):
        return 'CatalogFurnitureItem(%s%s)' % (self.furnitureType, self.formatOptionalData(store))

    def getFilename(self):
        type = FurnitureTypes[self.furnitureType]
        return type[FTModelName]

    def compareTo(self, other):
        return self.furnitureType - other.furnitureType

    def getHashContents(self):
        return self.furnitureType

    def getBasePrice(self):
        return FurnitureTypes[self.furnitureType][FTBasePrice]

    def loadModel(self):
        type = FurnitureTypes[self.furnitureType]
        model = loader.loadModel(type[FTModelName])
        self.applyColor(model, type[FTColor])
        if type[FTColorOptions] != None:
            if self.colorOption == None:
                option = random.choice(list(type[FTColorOptions].values()))
            else:
                # Use the user's specified color option.
                option = type[FTColorOptions].get(self.colorOption)
            
            self.applyColor(model, option)

        if (FTScale < len(type)):
            scale = type[FTScale]
            if not scale == None:
                model.setScale(scale)
                model.flattenLight()

        return model

    def decodeDatagram(self, di, versionNumber, store):
        CatalogAtticItem.CatalogAtticItem.decodeDatagram(self, di, versionNumber, store)
        self.furnitureType = di.getInt16()
        self.colorOption = None

        # The following will raise an exception if self.furnitureType
        # is not valid.
        type = FurnitureTypes[self.furnitureType]

        if type[FTColorOptions]:
            if store & CatalogItem.Customization:
                self.colorOption = di.getUint8()

                # The following will raise an exception if
                # self.colorOption is not valid.
                option = type[FTColorOptions][self.colorOption]
        
    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        dg.addInt16(self.furnitureType)
        if FurnitureTypes[self.furnitureType][FTColorOptions]:
            if store & CatalogItem.Customization:
                dg.addUint8(self.colorOption)
        

def nextAvailableBank(avatar, duplicateItems):
    bankId = MoneyToBank.get(avatar.getMaxBankMoney())
    if bankId == None or bankId == MaxBankId:
        # No more banks for this avatar.
        return None

    bankId += 10
    item = CatalogFurnitureItem(bankId)

    # But if this bank is already on order, don't offer the same bank
    # again.  Skip to the next one instead.
    while item in avatar.onOrder or \
          item in avatar.mailboxContents:
        bankId += 10
        if bankId > MaxBankId:
            return None
        item = CatalogFurnitureItem(bankId)

    def getAcceptItemErrorText(self, retcode):
        if retcode == ToontownGlobals.P_AlreadyOwnBiggerCloset:
            return TTLocalizer.CatalogAcceptClosetError
        return CatalogAtticItem.CatalogAtticItem.getAcceptItemErrorText(self, retcode)

def getAllBanks():
    _list = []
    for bankId in list(BankToMoney.keys()):
        _list.append(CatalogFurnitureItem(bankId))
    return _list

def nextAvailableCloset(avatar, duplicateItems):
    # detemine which closet index in the tuple to use
    if avatar.getStyle().getGender() == 'm':
        index = 0
    else:
        index = 1
    # handle a race a condition - dist toon ai cleaned up?
    if not hasattr(avatar, "maxClothes"):
        return None
    closetIds = ClothesToCloset.get(avatar.getMaxClothes())
    closetIds = list(closetIds)
    closetIds.sort()
    closetId = closetIds[index]
    if closetId == None or closetId == MaxClosetIds[index]:
        return
    closetId += 2
    item = CatalogFurnitureItem(closetId)

    # But if this closet is already on order, don't offer the same bank
    # again.  Skip to the next one instead.
    while item in avatar.onOrder or \
          item in avatar.mailboxContents:
        closetId += 2
        if closetId > MaxClosetIds[index]:
            return None
        item = CatalogFurnitureItem(closetId)

    return item

def nextAvailableBank(avatar, duplicateItems):
    if not avatar.getMaxBankMoney() in MoneyToBank:
        return CatalogFurnitureItem(1300)

    currentBank = MoneyToBank[avatar.getMaxBankMoney()]

    if currentBank == MaxBankId:
        return

    return CatalogFurnitureItem(currentBank + 10)

def get50ItemCloset(avatar, duplicateItems):
    if avatar.getStyle().getGender() == 'm':
        index = 0
    else:
        index = 1
    closetId = MaxClosetIds[index]
    item = CatalogFurnitureItem(closetId)
    if item in avatar.onOrder or item in avatar.mailboxContents:
        return None
    return item


def getMaxClosets():
    list = []
    for closetId in MaxClosetIds:
        list.append(CatalogFurnitureItem(closetId))

    return list


def getAllClosets():
    _list = []
    for closetId in list(ClosetToClothes.keys()):
        _list.append(CatalogFurnitureItem(closetId))

    return _list

def getAllBanks():
    _list = []

    for bankId in list(BankToMoney.keys()):
        _list.append(CatalogFurnitureItem(bankId))

    return _list

def getAllFurnitures(index):
    _list = []
    colors = FurnitureTypes[index][FTColorOptions]
    for n in range(len(colors)):
        _list.append(CatalogFurnitureItem(index, n))
    return _list
