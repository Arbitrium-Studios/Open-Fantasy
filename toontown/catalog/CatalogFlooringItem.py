from .CatalogSurfaceItem import *
FTTextureName = 0
FTColor = 1
FTBasePrice = 2
FlooringTypes = {1000: ('user/resources/default/phase_5.5/maps/floor_wood_neutral.jpg', CTBasicWoodColorOnWhite, 150),
                 1010: ('user/resources/default/phase_5.5/maps/flooring_carpetA_neutral.jpg', CTFlatColorDark, 150),
                 1020: ('user/resources/default/phase_4/maps/flooring_tile_neutral.jpg', CTFlatColorDark, 150),
                 1030: ('user/resources/default/phase_5.5/maps/flooring_tileB2.jpg', None, 150),
                 1040: ('user/resources/default/phase_4/maps/grass.jpg', None, 150),
                 1050: ('user/resources/default/phase_4/maps/floor_tile_brick_diagonal2.jpg', None, 150),
                 1060: ('user/resources/default/phase_4/maps/floor_tile_brick_diagonal.jpg', None, 150),
                 1070: ('user/resources/default/phase_4/maps/plazz_tile.jpg', None, 150),
                 1080: ('user/resources/default/phase_4/maps/sidewalk.jpg', CTFlatColorDark, 150),
                 1090: ('user/resources/default/phase_3.5/maps/boardwalk_floor.jpg', None, 150),
                 1100: ('user/resources/default/phase_3.5/maps/dustroad.jpg', None, 150),
                 1110: ('user/resources/default/phase_5.5/maps/floor_woodtile_neutral.jpg', CTBasicWoodColorOnWhite, 150),
                 1120: ('user/resources/default/phase_5.5/maps/floor_tile_neutral.jpg', CTBasicWoodColorOnWhite + CTFlatColorDark, 150),
                 1130: ('user/resources/default/phase_5.5/maps/floor_tile_honeycomb_neutral.jpg', CTBasicWoodColorOnWhite, 150),
                 1140: ('user/resources/default/phase_5.5/maps/UWwaterFloor1.jpg', None, 150),
                 1150: ('user/resources/default/phase_5.5/maps/UWtileFloor4.jpg', None, 150),
                 1160: ('user/resources/default/phase_5.5/maps/UWtileFloor3.jpg', None, 150),
                 1170: ('user/resources/default/phase_5.5/maps/UWtileFloor2.jpg', None, 150),
                 1180: ('user/resources/default/phase_5.5/maps/UWtileFloor1.jpg', None, 150),
                 1190: ('user/resources/default/phase_5.5/maps/UWsandyFloor1.jpg', None, 150),
                 10000: ('user/resources/default/phase_5.5/maps/floor_icecube.jpg', CTWhite, 225),
                 10010: ('user/resources/default/phase_5.5/maps/floor_snow.jpg', CTWhite, 225),
                 11000: ('user/resources/default/phase_5.5/maps/StPatsFloor1.jpg', CTWhite, 225),
                 11010: ('user/resources/default/phase_5.5/maps/StPatsFloor2.jpg', CTWhite, 225)}


class CatalogFlooringItem(CatalogSurfaceItem):

    def makeNewItem(self, patternIndex, colorIndex=None):
        self.patternIndex = patternIndex
        self.colorIndex = colorIndex
        CatalogSurfaceItem.makeNewItem(self)

    def needsCustomize(self):
        return self.colorIndex is None

    def getTypeName(self):
        return TTLocalizer.SurfaceNames[STFlooring]

    def getName(self):
        name = TTLocalizer.FlooringNames.get(self.patternIndex)
        if name:
            return name
        return self.getTypeName()

    def getSurfaceType(self):
        return STFlooring

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
        c.setTexture(self.loadTexture(), 1)
        c.setColorScale(*self.getColor())
        sample.reparentTo(frame)
        self.hasPicture = True
        return (frame, None)

    def output(self, store=-1):
        return 'CatalogFlooringItem(%s, %s%s)' % (
            self.patternIndex, self.colorIndex, self.formatOptionalData(store))

    def getFilename(self):
        return FlooringTypes[self.patternIndex][FTTextureName]

    def compareTo(self, other):
        if self.patternIndex != other.patternIndex:
            return self.patternIndex - other.patternIndex
        return 0

    def getHashContents(self):
        return self.patternIndex

    def getBasePrice(self):
        return FlooringTypes[self.patternIndex][FTBasePrice]

    def loadTexture(self):
        from pandac.PandaModules import Texture
        filename = FlooringTypes[self.patternIndex][FTTextureName]
        texture = loader.loadTexture(filename)
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        return texture

    def getColor(self):
        if self.colorIndex is None:
            colorIndex = 0
        else:
            colorIndex = self.colorIndex
        colors = FlooringTypes[self.patternIndex][FTColor]
        if colors:
            if colorIndex < len(colors):
                return colors[colorIndex]
            else:
                print('Warning: colorIndex not in colors. Returning white.')
                return CT_WHITE
        else:
            return CT_WHITE
        return

    def decodeDatagram(self, di, versionNumber, store):
        CatalogAtticItem.CatalogAtticItem.decodeDatagram(
            self, di, versionNumber, store)
        if versionNumber < 3:
            self.patternIndex = di.getUint8()
        else:
            self.patternIndex = di.getUint16()
        if versionNumber < 4 or store & CatalogItem.Customization:
            self.colorIndex = di.getUint8()
        else:
            self.colorIndex = None
        wtype = FlooringTypes[self.patternIndex]
        return

    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.patternIndex)
        if store & CatalogItem.Customization:
            dg.addUint8(self.colorIndex)


def getFloorings(*indexList):
    list = []
    for index in indexList:
        list.append(CatalogFlooringItem(index))

    return list


def getAllFloorings(*indexList):
    list = []
    for index in indexList:
        colors = FlooringTypes[index][FTColor]
        if colors:
            for n in range(len(colors)):
                list.append(CatalogFlooringItem(index, n))

        else:
            list.append(CatalogFlooringItem(index, 0))

    return list


def getFlooringRange(fromIndex, toIndex, *otherRanges):
    list = []
    froms = [fromIndex]
    tos = [toIndex]
    i = 0
    while i < len(otherRanges):
        froms.append(otherRanges[i])
        tos.append(otherRanges[i + 1])
        i += 2

    for patternIndex in list(FlooringTypes.keys()):
        for fromIndex, toIndex in zip(froms, tos):
            if patternIndex >= fromIndex and patternIndex <= toIndex:
                colors = FlooringTypes[patternIndex][FTColor]
                if colors:
                    for n in range(len(colors)):
                        list.append(CatalogFlooringItem(patternIndex, n))

                else:
                    list.append(CatalogFlooringItem(patternIndex, 0))

    return list
