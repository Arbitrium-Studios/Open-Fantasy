from .CatalogSurfaceItem import *
WTTextureName = 0
WTColor = 1
WTBorderList = 2
WTBasePrice = 3
BDTextureName = 0
BDColor = 1
All = (1000,
       1010,
       1020,
       1030,
       1040,
       1050,
       1060,
       1070)
WallpaperTypes = {1000: ('user/resources/default/phase_5.5/maps/flat_wallpaper1.jpg',
                         CTFlatColor,
                         (0, 1000),
                         180),
                  1100: ('user/resources/default/phase_5.5/maps/big_stripes1.jpg',
                         CTWhite,
                         (0, 1010),
                         180),
                  1110: ('user/resources/default/phase_5.5/maps/big_stripes2.jpg',
                         CTWhite,
                         (0, 1040),
                         180),
                  1120: ('user/resources/default/phase_5.5/maps/big_stripes3.jpg',
                         CTWhite,
                         (0, 1030),
                         180),
                  1130: ('user/resources/default/phase_5.5/maps/big_stripes4.jpg',
                         CTWhite,
                         (0, 1010),
                         180),
                  1140: ('user/resources/default/phase_5.5/maps/big_stripes5.jpg',
                         CTWhite,
                         (0, 1020),
                         180),
                  1150: ('user/resources/default/phase_5.5/maps/big_stripes6.jpg',
                         CTWhite,
                         (0, 1020),
                         180),
                  1200: ('user/resources/default/phase_5.5/maps/stripeB1.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1210: ('user/resources/default/phase_5.5/maps/stripeB2.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1220: ('user/resources/default/phase_5.5/maps/stripeB3.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1230: ('user/resources/default/phase_5.5/maps/stripeB4.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1240: ('user/resources/default/phase_3.5/maps/stripeB5.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1250: ('user/resources/default/phase_5.5/maps/stripeB6.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1260: ('user/resources/default/phase_5.5/maps/stripeB7.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1300: ('user/resources/default/phase_5.5/maps/squiggle1.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1310: ('user/resources/default/phase_5.5/maps/squiggle2.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1320: ('user/resources/default/phase_5.5/maps/squiggle3.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1330: ('user/resources/default/phase_5.5/maps/squiggle4.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1340: ('user/resources/default/phase_5.5/maps/squiggle5.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1350: ('user/resources/default/phase_5.5/maps/squiggle6.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1400: ('user/resources/default/phase_5.5/maps/stripes_cyan.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1410: ('user/resources/default/phase_5.5/maps/stripes_green.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1420: ('user/resources/default/phase_5.5/maps/stripes_magenta.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1430: ('user/resources/default/phase_5.5/maps/two_stripes1.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1440: ('user/resources/default/phase_5.5/maps/two_stripes2.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1450: ('user/resources/default/phase_5.5/maps/two_stripes3.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1500: ('user/resources/default/phase_5.5/maps/leaves1.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1510: ('user/resources/default/phase_5.5/maps/leaves2.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1520: ('user/resources/default/phase_5.5/maps/leaves3.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1600: ('user/resources/default/phase_5.5/maps/diamonds2_cherries.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1610: ('user/resources/default/phase_5.5/maps/diamonds3_cherries.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1620: ('user/resources/default/phase_5.5/maps/diamonds3_cherry.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1630: ('user/resources/default/phase_5.5/maps/diamonds4_cherries.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1640: ('user/resources/default/phase_5.5/maps/diamonds4_cherry.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1650: ('user/resources/default/phase_5.5/maps/diamonds5_cherries.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1660: ('user/resources/default/phase_5.5/maps/diamonds6_cherry.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1700: ('user/resources/default/phase_5.5/maps/moon1.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1710: ('user/resources/default/phase_5.5/maps/moon2.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1720: ('user/resources/default/phase_5.5/maps/moon3.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1730: ('user/resources/default/phase_5.5/maps/moon4.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1740: ('user/resources/default/phase_5.5/maps/moon5.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1750: ('user/resources/default/phase_5.5/maps/moon6.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1760: ('user/resources/default/phase_5.5/maps/moon7.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1800: ('user/resources/default/phase_5.5/maps/stars1.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1810: ('user/resources/default/phase_5.5/maps/stars2.jpg',
                         (CT_BLUE2, CT_PINK2, CT_RED),
                         (0,),
                         180),
                  1820: ('user/resources/default/phase_5.5/maps/stars3.jpg',
                         (CT_BLUE2,
                          CT_PINK2,
                          CT_RED,
                          CT_WHITE),
                         (0,),
                         180),
                  1830: ('user/resources/default/phase_5.5/maps/stars4.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1840: ('user/resources/default/phase_5.5/maps/stars5.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1850: ('user/resources/default/phase_5.5/maps/stars6.jpg',
                         CTWhite,
                         (0,),
                         180),
                  1860: ('user/resources/default/phase_5.5/maps/stars7.jpg',
                         (CT_BEIGE2, CT_WHITE),
                         (0,),
                         180),
                  1900: ('user/resources/default/phase_5.5/maps/wall_paper_flower1.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1910: ('user/resources/default/phase_5.5/maps/wall_paper_flower2.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1920: ('user/resources/default/phase_5.5/maps/wall_paper_flower3.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1930: ('user/resources/default/phase_5.5/maps/wall_paper_flower4.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1940: ('user/resources/default/phase_5.5/maps/wall_paper_flower5.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  1950: ('user/resources/default/phase_5.5/maps/wall_paper_flower6.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  2000: ('user/resources/default/phase_5.5/maps/flat_wallpaper1.jpg',
                         (CT_BEIGE, CT_BEIGE2, CT_RED),
                         (1050,),
                         180),
                  2010: ('user/resources/default/phase_5.5/maps/flat_wallpaper1.jpg',
                         (CT_BLUE2, CT_PINK2),
                         (1060,),
                         180),
                  2020: ('user/resources/default/phase_5.5/maps/flat_wallpaper1.jpg',
                         (CT_BEIGE2,
                          CT_BLUE2,
                          CT_PINK2,
                          CT_BEIGE,
                          CT_RED),
                         (1070,),
                         180),
                  2100: ('user/resources/default/phase_5.5/maps/big_stripes1.jpg',
                         CTWhite,
                         (1050,),
                         180),
                  2110: ('user/resources/default/phase_5.5/maps/big_stripes2.jpg',
                         CTWhite,
                         (1050,),
                         180),
                  2120: ('user/resources/default/phase_5.5/maps/big_stripes3.jpg',
                         CTWhite,
                         (1060,),
                         180),
                  2130: ('user/resources/default/phase_5.5/maps/big_stripes3.jpg',
                         CTWhite,
                         (1070,),
                         180),
                  2140: ('user/resources/default/phase_5.5/maps/big_stripes6.jpg',
                         CTWhite,
                         (1070,),
                         180),
                  2200: ('user/resources/default/phase_5.5/maps/wall_paper_car.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  2210: ('user/resources/default/phase_5.5/maps/wall_paper_car_neutral.jpg',
                         CTFlatColor,
                         (0, 1000),
                         180),
                  2300: ('user/resources/default/phase_5.5/maps/wall_paper_football_neutral.jpg',
                         CTFlatColor,
                         (0, 1080),
                         180),
                  2400: ('user/resources/default/phase_5.5/maps/wall_paper_clouds.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  2500: ('user/resources/default/phase_5.5/maps/wall_paper_vine_neutral.jpg',
                         CTFlatColorAll,
                         (0, 1090),
                         180),
                  2600: ('user/resources/default/phase_5.5/maps/basket.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  2610: ('user/resources/default/phase_5.5/maps/basket_neutral.jpg',
                         CTFlatColor,
                         (0, 1000),
                         180),
                  2700: ('user/resources/default/phase_5.5/maps/doll.jpg',
                         CTWhite,
                         (0, 1000, 1110),
                         180),
                  2710: ('user/resources/default/phase_5.5/maps/doll_neutral.jpg',
                         CTFlatColor,
                         (0, 1100, 1110),
                         180),
                  2800: ('user/resources/default/phase_5.5/maps/littleFlowers.jpg',
                         CTWhite,
                         (0, 1000),
                         180),
                  2810: ('user/resources/default/phase_5.5/maps/littleFlowers_neutral.jpg',
                         CTFlatColor,
                         (0, 1000),
                         180),
                  2900: ('user/resources/default/phase_5.5/maps/UWwallPaperAngelFish.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  2910: ('user/resources/default/phase_5.5/maps/UWwallPaperAngelFishColor.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  2920: ('user/resources/default/phase_5.5/maps/UWwallPaperBubbles.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  2930: ('user/resources/default/phase_5.5/maps/UWwallPaperBubbles2.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  2940: ('user/resources/default/phase_5.5/maps/UWwallPaperGreenFish.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  2950: ('user/resources/default/phase_5.5/maps/UWwallPaperRedFish.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  2960: ('user/resources/default/phase_5.5/maps/UWwallPaperSea_horse.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  2970: ('user/resources/default/phase_5.5/maps/UWwallPaperShells.jpg',
                         CTWhite,
                         (0, 1140, 1150),
                         180),
                  2980: ('user/resources/default/phase_5.5/maps/UWwaterFloor1.jpg',
                         (CT_WHITE, CT_PALE_GREEN, CT_LIGHT_BLUE),
                         (0,),
                         180),
                  3000: ('user/resources/default/phase_5.5/maps/UWwallPaperBubbles.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  3100: ('user/resources/default/phase_5.5/maps/UWwallPaperBubbles2.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  3200: ('user/resources/default/phase_5.5/maps/UWwallPaperGreenFish.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  3300: ('user/resources/default/phase_5.5/maps/UWwallPaperRedFish.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  3400: ('user/resources/default/phase_5.5/maps/UWwallPaperSea_horse.jpg',
                         CTWhite,
                         (0, 1120, 1160),
                         180),
                  3500: ('user/resources/default/phase_5.5/maps/UWwallPaperShells.jpg',
                         (CT_WHITE, CT_SEA_GREEN, CT_LIGHT_BLUE),
                         (0, 1140, 1150),
                         180),
                  3600: ('user/resources/default/phase_5.5/maps/UWwaterFloor1.jpg',
                         (CT_WHITE, CT_PALE_GREEN, CT_LIGHT_BLUE),
                         (0,),
                         180),
                  3700: ('user/resources/default/phase_5.5/maps/WesternBootWallpaper1.jpg',
                         CTWhite,
                         (0, 1170, 1180),
                         180),
                  3800: ('user/resources/default/phase_5.5/maps/WesternCactusWallpaper1.jpg',
                         CTWhite,
                         (0, 1170, 1180),
                         180),
                  3900: ('user/resources/default/phase_5.5/maps/WesternHatWallpaper1.jpg',
                         CTWhite,
                         (0, 1170, 1180),
                         180),
                  10100: ('user/resources/default/phase_5.5/maps/cats1.jpg',
                          CTWhite,
                          (0, 10010, 10020),
                          400),
                  10200: ('user/resources/default/phase_5.5/maps/bats2.jpg',
                          CTWhite,
                          (0, 10010, 10020),
                          400),
                  11000: ('user/resources/default/phase_5.5/maps/wall_paper_snowflakes.jpg',
                          CTWhite,
                          (0, 11000, 11010),
                          400),
                  11100: ('user/resources/default/phase_5.5/maps/wall_paper_hollyleaf.jpg',
                          CTWhite,
                          (0, 11000, 11010),
                          400),
                  11200: ('user/resources/default/phase_5.5/maps/wall_paper_snowman.jpg',
                          CTWhite,
                          (0, 11000, 11010),
                          400),
                  12000: ('user/resources/default/phase_5.5/maps/VdayWall1.jpg',
                          CTWhite,
                          (0,
                           12000,
                           12010,
                           12020),
                          400),
                  12100: ('user/resources/default/phase_5.5/maps/VdayWall2.jpg',
                          CTWhite,
                          (0,
                           12000,
                           12010,
                           12020),
                          400),
                  12200: ('user/resources/default/phase_5.5/maps/VdayWall3.jpg',
                          CTWhite,
                          (0,
                           12000,
                           12010,
                           12020),
                          400),
                  12300: ('user/resources/default/phase_5.5/maps/VdayWall4.jpg',
                          CTWhite,
                          (0,
                           12000,
                           12010,
                           12020),
                          400),
                  13000: ('user/resources/default/phase_5.5/maps/StPatWallpaper1.jpg',
                          CTWhite,
                          (0, 13000),
                          400),
                  13100: ('user/resources/default/phase_5.5/maps/StPatWallpaper2.jpg',
                          CTWhite,
                          (0, 13000),
                          400),
                  13200: ('user/resources/default/phase_5.5/maps/StPatWallpaper3.jpg',
                          CTWhite,
                          (0, 13000),
                          400),
                  13300: ('user/resources/default/phase_5.5/maps/StPatWallpaper4.jpg',
                          CTWhite,
                          (0, 13000),
                          400)}
WallpaperGroups = {1100: (1100,
                          1110,
                          1120,
                          1130,
                          1140,
                          1150),
                   1200: (1200,
                          1210,
                          1220,
                          1230,
                          1240,
                          1250,
                          1260),
                   1300: (1300,
                          1310,
                          1320,
                          1330,
                          1340,
                          1350),
                   1400: (1400,
                          1410,
                          1420,
                          1430,
                          1440,
                          1450),
                   1500: (1500, 1510, 1520),
                   1600: (1600,
                          1610,
                          1620,
                          1630,
                          1640,
                          1650,
                          1660),
                   1700: (1700,
                          1710,
                          1720,
                          1730,
                          1740,
                          1750,
                          1760),
                   1800: (1800,
                          1810,
                          1820,
                          1830,
                          1840,
                          1850,
                          1860),
                   1900: (1900,
                          1910,
                          1920,
                          1930,
                          1940,
                          1950),
                   2000: (2000, 2010, 2020),
                   2100: (2100,
                          2110,
                          2120,
                          2130,
                          2140),
                   2200: (2200, 2210),
                   2600: (2600, 2610),
                   2700: (2700, 2710),
                   2800: (2800, 2810),
                   2900: (2900, 2910)}
BorderTypes = {1000: ('user/resources/default/phase_5.5/maps/bd_grey_border1.jpg', CTFlatColorDark),
               1010: ('user/resources/default/phase_5.5/maps/diamonds_border2.jpg', CTWhite),
               1020: ('user/resources/default/phase_5.5/maps/diamonds_border2ch.jpg', CTWhite),
               1030: ('user/resources/default/phase_5.5/maps/diamonds_border3ch.jpg', CTWhite),
               1040: ('user/resources/default/phase_5.5/maps/diamonds_border4ch.jpg', CTWhite),
               1050: ('user/resources/default/phase_5.5/maps/flower_border2.jpg', CTWhite),
               1060: ('user/resources/default/phase_5.5/maps/flower_border5.jpg', CTWhite),
               1070: ('user/resources/default/phase_5.5/maps/flower_border6.jpg', CTWhite),
               1080: ('user/resources/default/phase_5.5/maps/football_border_neutral.jpg', CTFlatColorDark),
               1090: ('user/resources/default/phase_5.5/maps/vine_border1.jpg', CTFlatColorDark),
               1100: ('user/resources/default/phase_5.5/maps/doll_board.jpg', CTWhite),
               1110: ('user/resources/default/phase_5.5/maps/doll_board_neutral.jpg', CTFlatColorDark),
               1120: ('user/resources/default/phase_5.5/maps/UWwallPaperPlantBorder.jpg', CTWhite),
               1130: ('user/resources/default/phase_5.5/maps/UWwallPaperSea_horseBorder.jpg', CTWhite),
               1140: ('user/resources/default/phase_5.5/maps/UWwallPaperShellBorder1.jpg', CTWhite),
               1150: ('user/resources/default/phase_5.5/maps/UWwallPaperShellBorder2.jpg', CTWhite),
               1160: ('user/resources/default/phase_5.5/maps/UWwallPaperWaveBorder.jpg', CTWhite),
               1170: ('user/resources/default/phase_5.5/maps/WesternSkullBorder.jpg', CTWhite),
               1180: ('user/resources/default/phase_5.5/maps/WesternStarBorder.jpg', CTWhite),
               10010: ('user/resources/default/phase_5.5/maps/border_ScarryMoon1.jpg', CTWhite),
               10020: ('user/resources/default/phase_5.5/maps/border_candy1.jpg', CTWhite),
               11000: ('user/resources/default/phase_5.5/maps/flakes_border.jpg', CTWhite),
               11010: ('user/resources/default/phase_5.5/maps/hollyleaf_border.jpg', CTWhite),
               12000: ('user/resources/default/phase_5.5/maps/Vborder1a.jpg', CTWhite),
               12010: ('user/resources/default/phase_5.5/maps/Vborder1b.jpg', CTWhite),
               12020: ('user/resources/default/phase_5.5/maps/Vborder2b.jpg', CTWhite),
               13000: ('user/resources/default/phase_5.5/maps/StPatBorder1.jpg', CTWhite)}


class CatalogWallpaperItem(CatalogSurfaceItem):

    def makeNewItem(self, patternIndex, colorIndex=None,
                    borderIndex=0, borderColorIndex=0):
        self.patternIndex = patternIndex
        self.colorIndex = colorIndex
        self.borderIndex = borderIndex
        self.borderColorIndex = borderColorIndex
        CatalogSurfaceItem.makeNewItem(self)

    def needsCustomize(self):
        return self.colorIndex is None or self.borderIndex is None

    def getTypeName(self):
        return TTLocalizer.SurfaceNames[STWallpaper]

    def getName(self):
        name = TTLocalizer.WallpaperNames.get(self.patternIndex)
        if name is None:
            century = self.patternIndex - self.patternIndex % 100
            name = TTLocalizer.WallpaperNames.get(century)
        if name:
            return name
        return self.getTypeName()

    def getSurfaceType(self):
        return STWallpaper

    def getPicture(self, avatar):
        frame = self.makeFrame()
        sample = loader.loadModel('user/resources/default/phase_5.5/models/estate/wallpaper_sample')
        a = sample.find('**/a')
        b = sample.find('**/b')
        c = sample.find('**/c')
        a.setTexture(self.loadTexture(), 1)
        a.setColorScale(*self.getColor())
        b.setTexture(self.loadTexture(), 1)
        b.setColorScale(*self.getColor())
        c.setTexture(self.loadBorderTexture(), 1)
        c.setColorScale(*self.getBorderColor())
        sample.reparentTo(frame)
        self.hasPicture = True
        return (frame, None)

    def output(self, store=-1):
        return 'CatalogWallpaperItem(%s, %s, %s, %s%s)' % (self.patternIndex,
                                                           self.colorIndex,
                                                           self.borderIndex,
                                                           self.borderColorIndex,
                                                           self.formatOptionalData(store))

    def getFilename(self):
        return WallpaperTypes[self.patternIndex][WTTextureName]

    def compareTo(self, other):
        if self.patternIndex != other.patternIndex:
            century = self.patternIndex - self.patternIndex % 100
            otherCentury = other.patternIndex - other.patternIndex % 100
            return century - otherCentury
        return 0

    def getHashContents(self):
        century = self.patternIndex - self.patternIndex % 100
        return century

    def getBasePrice(self):
        return WallpaperTypes[self.patternIndex][WTBasePrice]

    def loadTexture(self):
        from pandac.PandaModules import Texture
        filename = WallpaperTypes[self.patternIndex][WTTextureName]
        texture = loader.loadTexture(filename)
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        return texture

    def getColor(self):
        if self.colorIndex is None:
            colorIndex = 0
        else:
            colorIndex = self.colorIndex
        colors = WallpaperTypes[self.patternIndex][WTColor]
        if colorIndex < len(colors):
            return colors[colorIndex]
        else:
            print('Warning: colorIndex > len(colors). Returning white.')
            return CT_WHITE
        return

    def loadBorderTexture(self):
        from pandac.PandaModules import Texture
        if self.borderIndex is None or self.borderIndex == 0:
            return self.loadTexture()
        borderInfo = BorderTypes[self.borderIndex]
        filename = borderInfo[BDTextureName]
        texture = loader.loadTexture(filename)
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        return texture

    def getBorderColor(self):
        if self.borderIndex is None or self.borderIndex == 0:
            return self.getColor()
        else:
            colors = BorderTypes[self.borderIndex][BDColor]
        if self.borderColorIndex < len(colors):
            return colors[self.borderColorIndex]
        else:
            return CT_WHITE
        return

    def decodeDatagram(self, di, versionNumber, store):
        CatalogAtticItem.CatalogAtticItem.decodeDatagram(
            self, di, versionNumber, store)
        self.colorIndex = None
        if store & CatalogItem.Customization:
            self.borderIndex = 0
        else:
            self.borderIndex = None
        self.borderColorIndex = 0
        if versionNumber < 3:
            self.patternIndex = di.getUint8()
            self.colorIndex = di.getUint8()
        elif versionNumber == 3:
            self.patternIndex = di.getUint16()
            self.colorIndex = di.getUint8()
        else:
            self.patternIndex = di.getUint16()
            if store & CatalogItem.Customization:
                self.colorIndex = di.getUint8()
                self.borderIndex = di.getUint16()
                self.borderColorIndex = di.getUint8()
        wtype = WallpaperTypes[self.patternIndex]
        return

    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.patternIndex)
        if store & CatalogItem.Customization:
            dg.addUint8(self.colorIndex)
            dg.addUint16(self.borderIndex)
            dg.addUint8(self.borderColorIndex)


def getWallpapers(*typeList):
    list = []
    for type in typeList:
        list.append(CatalogWallpaperItem(type))

    return list


def getAllWallpapers(*typeList):
    list = []
    for type in typeList:
        group = WallpaperGroups.get(type, [type])
        for index in group:
            borderKeys = WallpaperTypes[index][WTBorderList]
            for borderKey in borderKeys:
                borderData = BorderTypes.get(borderKey)
                if borderData:
                    numBorderColors = len(borderData[BDColor])
                else:
                    numBorderColors = 1
                for borderColorIndex in range(numBorderColors):
                    colors = WallpaperTypes[index][WTColor]
                    for n in range(len(colors)):
                        list.append(
                            CatalogWallpaperItem(
                                index, n, borderKey, borderColorIndex))

    return list


def getWallpaperRange(fromIndex, toIndex, *otherRanges):
    list = []
    froms = [fromIndex]
    tos = [toIndex]
    i = 0
    while i < len(otherRanges):
        froms.append(otherRanges[i])
        tos.append(otherRanges[i + 1])
        i += 2

    for patternIndex in list(WallpaperTypes.keys()):
        for fromIndex, toIndex in zip(froms, tos):
            if patternIndex >= fromIndex and patternIndex <= toIndex:
                borderKeys = WallpaperTypes[patternIndex][WTBorderList]
                for borderKey in borderKeys:
                    borderData = BorderTypes.get(borderKey)
                    if borderData:
                        numBorderColors = len(borderData[BDColor])
                    else:
                        numBorderColors = 1
                    for borderColorIndex in range(numBorderColors):
                        colors = WallpaperTypes[patternIndex][WTColor]
                        for n in range(len(colors)):
                            list.append(
                                CatalogWallpaperItem(
                                    patternIndex,
                                    n,
                                    borderKey,
                                    borderColorIndex))

    return list
