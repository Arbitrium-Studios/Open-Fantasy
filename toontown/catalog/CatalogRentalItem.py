from . import CatalogItem
import time
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *
from toontown.toontowngui import TTDialog

class CatalogRentalItem(CatalogItem.CatalogItem):
    """CatalogRentalItem

    This is an item that goes away after a period of time.

    """

    def makeNewItem(self, typeIndex, duration, cost):
        self.typeIndex = typeIndex
        self.duration = duration # duration is in minutes
        self.cost = cost
        # this will need to be persistant (db?)
        CatalogItem.CatalogItem.makeNewItem(self)
        
    def getDuration(self):
        return self.duration
    # TODO: who will check for expired items? CatalogManagerAI?
    
    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        return 0
        
    def reachedPurchaseLimit(self, avatar):
        return self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1
        
    def getTypeName(self):
        # Returns the name of the general type of item.
        return TTLocalizer.RentalTypeName
        
        
    def getName(self):
        hours = int(self.duration / 60)
        if self.typeIndex == ToontownGlobals.RentalCannon:
            return '%s %s %s %s' % (hours,
             TTLocalizer.RentalHours,
             TTLocalizer.RentalOf,
             TTLocalizer.RentalCannon)
        elif self.typeIndex == ToontownGlobals.RentalGameTable:
            return '%s %s %s' % (hours, TTLocalizer.RentalHours, TTLocalizer.RentalGameTable)
        else:
            return TTLocalizer.RentalTypeName
            

    def recordPurchase(self, avatar, optional):
        if avatar:
            self.notify.debug('rental -- has avatar')
            estate = simbase.air.estateManager._lookupEstate(avatar)
            if estate:
                self.notify.debug("rental -- has estate")
                estate.rentItem(self.typeIndex, self.duration)
            else:
                self.notify.warning('rental -- something not there')
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        scale = 1
        heading = 0
        pitch = 30
        roll = 0
        spin = 1
        down = -1
        if self.typeIndex == ToontownGlobals.RentalCannon:
            model = loader.loadModel("phase_4/models/minigames/toon_cannon")
            scale = .5
            heading = 45
        elif self.typeIndex == ToontownGlobals.RentalGameTable:
            model = loader.loadModel("phase_6/models/golf/game_table")
        assert (not self.hasPicture)
        self.hasPicture = True

        return self.makeFrameModel(model, spin)

    def output(self, store = -1):
        return 'CatalogRentalItem(%s%s)' % (self.typeIndex, self.formatOptionalData(store))

    def compareTo(self, other):
        return self.typeIndex - other.typeIndex

    def getHashContents(self):
        return self.typeIndex

    def getBasePrice(self):
        if self.typeIndex == ToontownGlobals.RentalCannon:
            return self.cost
        elif self.typeIndex == ToontownGlobals.RentalGameTable:
            return self.cost
        else:
            return 50

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.cost = di.getUint16()
        self.duration = di.getUint16()
        self.typeIndex = di.getUint16()
        
    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.cost)
        dg.addUint16(self.duration)
        dg.addUint16(self.typeIndex)
        
    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 1  # 1 minute.
        
    def isRental(self):
        return 1
        
    def acceptItem(self, mailbox, index, callback):
        self.confirmRent = TTDialog.TTGlobalDialog(doneEvent='confirmRent', message=TTLocalizer.MessageConfirmRent, command=Functor(self.handleRentConfirm, mailbox, index, callback), style=TTDialog.TwoChoice)
        self.confirmRent.show()
        #self.accept("confirmRent", Functor(self.handleRentConfirm, mailbox, index, callback))
        #self.__handleRentConfirm)
        #self.mailbox = mailbox
        #self.mailIndex = index
        #self.mailcallback = callback
        
    def handleRentConfirm(self, mailbox, index, callback, choice):
    #def handleRentConfirm(self, *args):
        #print(args)
        if choice > 0:
            mailbox.acceptItem(self, index, callback)
        else:
            callback(ToontownGlobals.P_UserCancelled, self, index)
        if self.confirmRent:
            self.confirmRent.cleanup()
            self.confirmRent = None
        
    
def getAllRentalItems():
    list = []
    for rentalType in (ToontownGlobals.RentalCannon,):
        list.append(CatalogRentalItem(rentalType, 2880, 1000))
    for rentalType in (ToontownGlobals.RentalGameTable,):
        list.append(CatalogRentalItem(rentalType, 2890, 1000))

    return list
