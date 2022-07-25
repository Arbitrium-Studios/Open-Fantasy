from . import CatalogItem
import time
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *
from toontown.toontowngui import TTDialog
from toontown.estate import GardenTutorial

class CatalogGardenStarterItem(CatalogItem.CatalogItem):
    """CatalogGardenStarterItem

    This is an item that goes away after a period of time.

    """

    def makeNewItem(self):
        # this will need to be persistant (db?)
        CatalogItem.CatalogItem.makeNewItem(self)
        
    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        return 0

    def reachedPurchaseLimit(self, avatar):            
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder or self in avatar.awardMailboxContents or self in avatar.onAwardOrder or hasattr(avatar, 'gardenStarted') and avatar.getGardenStarted():
            return 1
        return 0
        
    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1
        
    def getTypeName(self):
        # Returns the name of the general type of item.
        return TTLocalizer.GardenStarterTypeName
        
        
    def getName(self):
        return TTLocalizer.GardenStarterTypeName
            

    def recordPurchase(self, avatar, optional):
        if avatar:
            self.notify.debug('rental -- has avatar')
            estate = simbase.air.estateManager._lookupEstate(avatar)
            if estate:
                self.notify.debug('rental -- has estate')
                estate.placeStarterGarden(avatar.doId)
            else:
                self.notify.warning('rental -- something not there')
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):

        assert (not self.hasPicture)
        self.hasPicture=True

        scale = 1
        heading = 0
        pitch = 30
        roll = 0
        spin = 1
        down = -1
        #chatBalloon = loader.loadModel("phase_3/models/props/chatbox.bam")
        modelParent = loader.loadModel('phase_5.5/models/estate/watering_cans')
        model = modelParent.find('**/water_canA')
        scale = .5
        heading = 45

        return self.makeFrameModel(model, spin)

    def output(self, store = -1):
        return 'CatalogGardenStarterItem(%s)' % self.formatOptionalData(store)

    def compareTo(self, other):
        return 0

    def getHashContents(self):
        return 0

    def getBasePrice(self):
        return 50

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        
    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        
    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 1  # 1 minute.
        
    def isRental(self):
        return 0
        
    def isGift(self):
        return 0
        
    def acceptItem(self, mailbox, index, callback):
        self.confirmGarden = TTDialog.TTGlobalDialog(doneEvent='confirmGarden', message=TTLocalizer.MessageConfirmGarden, command=Functor(self.handleGardenConfirm, mailbox, index, callback), style=TTDialog.TwoChoice)
        self.confirmGarden.show()
        #self.accept("confirmRent", Functor(self.handleRentConfirm, mailbox, index, callback))
        #self.__handleRentConfirm)
        #self.mailbox = mailbox
        #self.mailIndex = index
        #self.mailcallback = callback
        
    def handleGardenConfirm(self, mailbox, index, callback, choice):
    #def handleRentConfirm(self, *args):
        #print(args)
        if choice > 0:
            def handleTutorialDone():                
                self.gardenTutorial.destroy()
                self.gardenTutorial = None

            self.gardenTutorial = GardenTutorial.GardenTutorial(callback=handleTutorialDone)
            if hasattr(mailbox, 'mailboxGui') and mailbox.mailboxGui:
                mailbox.acceptItem(self, index, callback)
                mailbox.mailboxGui.justExit()
        else:
            callback(ToontownGlobals.P_UserCancelled, self, index)
        if self.confirmGarden:
            self.confirmGarden.cleanup()
            self.confirmGarden = None
