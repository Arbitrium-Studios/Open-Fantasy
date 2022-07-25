from panda3d.core import *
from . import CatalogAtticItem
from . import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer


WVTModelName = 0
WVTBasePrice = 1
WVTSkyName = 2
WindowViewTypes = {10: ('phase_5.5/models/estate/Garden1', 900, None),
 20: ('phase_5.5/models/estate/GardenA', 900, None),
 30: ('phase_5.5/models/estate/GardenB', 900, None),
 40: ('phase_5.5/models/estate/cityView', 900, None),
 50: ('phase_5.5/models/estate/westernView', 900, None),
 60: ('phase_5.5/models/estate/underwaterView', 900, None),
 70: ('phase_5.5/models/estate/tropicView', 900, None),
 80: ('phase_5.5/models/estate/spaceView', 900, None),
 90: ('phase_5.5/models/estate/PoolView', 900, None),
 100: ('phase_5.5/models/estate/SnowView', 900, None),
 110: ('phase_5.5/models/estate/FarmView', 900, None),
 120: ('phase_5.5/models/estate/IndianView', 900, None),
 130: ('phase_5.5/models/estate/WesternMainStreetView', 900, None)}

class CatalogWindowItem(CatalogAtticItem.CatalogAtticItem):
    """CatalogWindowItem

    # This represents a view to hang outside a window in a house.
    
    """
    
    def makeNewItem(self, windowType, placement = None):
        self.windowType = windowType
        self.placement = placement
        CatalogAtticItem.CatalogAtticItem.makeNewItem(self)

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def getTypeName(self):
        return TTLocalizer.WindowViewTypeName

    def getName(self):
        return TTLocalizer.WindowViewNames.get(self.windowType)

    def recordPurchase(self, avatar, optional):
        house, retcode = self.getHouseInfo(avatar)
        if retcode >= 0:
            house.addWindow(self)
        return retcode

    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 4 * 60  # 4 hours.
    
    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.
        frame = self.makeFrame()
        model = self.loadModel()

        # This 3-d model will be drawn in the 2-d scene.
        model.setDepthTest(1)
        model.setDepthWrite(1)

        # Set up clipping planes to cut off the parts of the view that
        # would extend beyond the frame.
        clipperLeft = PlaneNode('clipper')
        clipperRight = PlaneNode('clipper')
        clipperTop = PlaneNode('clipper')
        clipperBottom = PlaneNode('clipper')
        clipperLeft.setPlane(Plane(Vec3(1, 0, 0), Point3(-1, 0, 0)))
        clipperRight.setPlane(Plane(Vec3(-1, 0, 0), Point3(1, 0, 0)))
        clipperTop.setPlane(Plane(Vec3(0, 0, -1), Point3(0, 0, 1)))
        clipperBottom.setPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -1)))
        model.setClipPlane(frame.attachNewNode(clipperLeft))
        model.setClipPlane(frame.attachNewNode(clipperRight))
        model.setClipPlane(frame.attachNewNode(clipperTop))
        model.setClipPlane(frame.attachNewNode(clipperBottom))

        # Fix draw order of background
        bgName = WindowViewTypes[self.windowType][WVTSkyName]
        if bgName:
            bgNodePath = model.find("**/" + bgName)
            if not bgNodePath.isEmpty():
                # Put it at the front of the list to be drawn first
                bgNodePath.reparentTo(model, -1)
        
        # Get rid of the window frame that is in the model
        windowFrame = model.find("**/frame")
        if not windowFrame.isEmpty():
            windowFrame.removeNode()
            
        model.setPos(0,2,0)
        model.setScale(0.4)
        model.reparentTo(frame)

        assert (not self.hasPicture)
        self.hasPicture=True

        return (frame, None)

    def output(self, store = -1):
        return 'CatalogWindowItem(%s%s)' % (self.windowType, self.formatOptionalData(store))

    def getFilename(self):
        type = WindowViewTypes[self.windowType]
        return type[WVTModelName]

    def formatOptionalData(self, store = -1):
        result = CatalogAtticItem.CatalogAtticItem.formatOptionalData(self, store)
        if store & CatalogItem.WindowPlacement and self.placement != None:
            result += ', placement = %s' % self.placement
        return result

    def compareTo(self, other):
        return self.windowType - other.windowType

    def getHashContents(self):
        return self.windowType

    def getBasePrice(self):
        return WindowViewTypes[self.windowType][WVTBasePrice]

    def loadModel(self):
        type = WindowViewTypes[self.windowType]
        model = loader.loadModel(type[WVTModelName])

        return model

    def decodeDatagram(self, di, versionNumber, store):
        CatalogAtticItem.CatalogAtticItem.decodeDatagram(self, di, versionNumber, store)
        self.placement = None
        if store & CatalogItem.WindowPlacement:
            self.placement = di.getUint8()
        self.windowType = di.getUint8()

        # The following will generate an exception if
        # self.windowType is invalid.
        wvtype = WindowViewTypes[self.windowType]

    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        if store & CatalogItem.WindowPlacement:
            dg.addUint8(self.placement)
        dg.addUint8(self.windowType)
