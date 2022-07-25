from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.fsm.FSM import FSM
import time

# -- FSMS --
class OperationFSM(FSM):

    def __init__(self, mgr, air, senderAvId, targetAvId=None, callback=None):
        FSM.__init__(self, 'OperationFSM-%s' % senderAvId)
        self.mgr = mgr
        self.air = air
        self.sender = senderAvId
        self.result = None
        self.target = targetAvId
        self.callback = callback

    def enterOff(self):
        if self.callback:
            if self.result is not None:
                self.callback(self.sender, self.result)
            else:
                self.callback()

        if self in self.mgr.operations:
            self.mgr.operations.remove(self)

    def enterError(self, message=None):
        self.mgr.notify.warning("An error has occurred in a '%s'. Message: %s" %
            (type(self).__name__, message) )
        if self.sender in self.mgr.operations:
            del self.mgr.operations[self.sender]


# -- Friends list --
class FriendsListOperation(OperationFSM):

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender,
            self.handleRetrieveSender)

    def handleRetrieveSender(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.demand('Error', 'Distributed Class was not a Toon.')
            return

        self.demand('Retrieved', fields['setFriendsList'][0])

    def enterRetrieved(self, friendsList):
        self.friendsList = friendsList
        if len(self.friendsList) <= 0:
            self.result = []
            self.demand('Off')
            return

        self.friendIndex = 0
        self.realFriendsList = []

        self.air.dbInterface.queryObject(self.air.dbId, self.friendsList[0],
            self.addFriend)

    def addFriend(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.demand('Error', 'Friend was not a Toon')
            return
        friendId = self.friendsList[self.friendIndex]
        self.realFriendsList.append([friendId, fields['setName'][0],
            fields['setDNAString'][0], fields['setAdminAccess'][0], fields['setPetId'][0]])

        if len(self.realFriendsList) >= len(self.friendsList):
            self.result = self.realFriendsList
            self.demand('Off')
            return

        self.friendIndex += 1
        self.air.dbInterface.queryObject(self.air.dbId,
            self.friendsList[self.friendIndex], self.addFriend)


# -- Remove Friends --
class RemoveFriendOperation(OperationFSM):

    def __init__(self, mgr, air, senderAvId, targetAvId=None, callback=None, alert=False):
        OperationFSM.__init__(self, mgr, air, senderAvId, targetAvId, callback)
        self.alert = alert

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender,
            self.handleRetrieve)

    def handleRetrieve(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.demand('Error', 'Distributed Class was not a Toon.')
            return

        self.demand('Retrieved', fields['setFriendsList'][0], fields['setTrueFriends'][0])

    def enterRetrieved(self, friendsList, trueFriendsList):
        if self.target in friendsList:
            friendsList.remove(self.target)
        if self.target in trueFriendsList:
            trueFriendsList.remove(self.target)
        if self.sender in self.mgr.onlineToons:
            dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                    'setFriendsList', self.sender, self.sender,
                    self.air.ourChannel, [friendsList])
            self.air.send(dg)
            if self.alert:
                dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                     'friendsNotify', self.sender, self.sender,
                     self.air.ourChannel, [self.target, 1])
                self.air.send(dg)
            self.demand('Off')
            return

        self.air.dbInterface.updateObject(self.air.dbId, self.sender,
            self.air.dclassesByName['DistributedToonUD'],
            {'setFriendsList' : [friendsList], 'setTrueFriends': [trueFriendsList]})
        self.demand('Off')

# -- Clear List --
class ClearListOperation(OperationFSM):

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender,
            self.handleRetrieved)

    def handleRetrieved(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.demand('Error', 'Distributed Class was not a Toon.')
            return
        self.demand('Retrieved', fields['setFriendsList'][0])

    def enterRetrieved(self, friendsList):
        for friend in friendsList:
            newOperation = RemoveFriendOperation(self.mgr, self.air, friend,
                targetAvId=self.sender, alert=True)
            self.mgr.operations.append(newOperation)
            newOperation.demand('Start')
        self.demand('Off')

# -- FriendsManager --

class TTSFriendsManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('TTSFriendsManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.onlineToons = []
        self.tpRequests = {}
        self.whisperRequests = {}
        self.toon2data = {}
        self.operations = []
        self.delayTime = 1.0

    # -- Friends list --
    def requestFriendsList(self):
        avId = self.air.getAvatarIdFromSender()
        newOperation = FriendsListOperation(self, self.air, avId,
            callback = self.sendFriendsList)
        self.operations.append(newOperation)
        newOperation.demand('Start')

    def sendFriendsList(self, sender, friendsList):
        self.sendUpdateToAvatarId(sender, 'friendList', [friendsList])
        if sender not in self.onlineToons:
            self.toonOnline(sender, friendsList)

    # -- Remove Friend --
    def removeFriend(self, friendId):
        avId = self.air.getAvatarIdFromSender()

        # Sender remove Friend
        newOperation = RemoveFriendOperation(self, self.air, avId, friendId)
        self.operations.append(newOperation)
        newOperation.demand('Start')

        # Friend remove Sender
        newOperation = RemoveFriendOperation(self, self.air, friendId, avId,
            alert=True)
        self.operations.append(newOperation)
        newOperation.demand('Start')

    # -- Avatar Info --
    def getAvatarDetails(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            inventory = fields['setInventory'][0]
            trackAccess = fields['setTrackAccess'][0]
            hp = fields['setHp'][0]
            maxHp = fields['setMaxHp'][0]
            defaultShard = fields['setDefaultShard'][0]
            lastHood = fields['setLastHood'][0]
            dnaString =  fields['setDNAString'][0]
            experience = fields['setExperience'][0]
            trackBonusLevel = fields['setTrackBonusLevel'][0]
            npcFriends = fields['setNPCFriendsDict'][0]

            self.sendUpdateToAvatarId(senderId, 'friendDetails', [avId, inventory, trackAccess, hp, maxHp, defaultShard, lastHood, dnaString, experience, trackBonusLevel, npcFriends])
        self.air.dbInterface.queryObject(self.air.dbId, avId, handleToon)
    
    def getPetDetails(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        def handlePet(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedPetAI']:
                return
            dna = [fields.get(x, [0])[0] for x in ("setHead", "setEars", "setNose", "setTail", "setBodyTexture", "setColor",
                                                 "setColorScale", "setEyeColor", "setGender")]
            moods = [fields.get(x, [0])[0] for x in ("setBoredom", "setRestlessness", "setPlayfulness", "setLoneliness",
                                                   "setSadness", "setAffection", "setHunger", "setConfusion", "setExcitement",
                                                   "setFatigue", "setAnger", "setSurprise")]
            traits = [fields.get(x, [0])[0] for x in ("setForgetfulness", "setBoredomThreshold", "setRestlessnessThreshold",
                                                    "setPlayfulnessThreshold", "setLonelinessThreshold", "setSadnessThreshold",
                                                    "setFatigueThreshold", "setHungerThreshold", "setConfusionThreshold",
                                                    "setExcitementThreshold", "setAngerThreshold", "setSurpriseThreshold",
                                                    "setAffectionThreshold")]
            self.sendUpdateToAvatarId(senderId, 'petDetails', [avId, fields.get("setOwnerId", [0])[0], fields.get("setPetName", ["???"])[0],
                                                               fields.get("setTraitSeed", [0])[0], fields.get("setSafeZone", [0])[0],
                                                               traits, moods, dna, fields.get("setLastSeenTimestamp", [0])[0]])
        self.air.dbInterface.queryObject(self.air.dbId, avId, handlePet)

    # -- Toon Online/Offline --
    def toonOnline(self, doId, friendsList):
        if doId not in self.onlineToons:
            self.onlineToons.append(doId)

        channel = self.GetPuppetConnectionChannel(doId)
        dgcleanup = self.dclass.aiFormatUpdate('goingOffline', self.doId, self.doId, self.air.ourChannel, [doId])
        dg = PyDatagram()
        dg.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addBlob(dgcleanup.getMessage())
        self.air.send(dg)

        for friend in friendsList:
            friendId = friend[0]
            if friendId in self.onlineToons:
                self.sendUpdateToAvatarId(doId, 'friendOnline', [friendId])
            self.sendUpdateToAvatarId(friendId, 'friendOnline', [doId])

    def goingOffline(self, avId):
        self.toonOffline(avId)

    def toonOffline(self, doId):
        if doId not in self.onlineToons:
            return
        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            friendsList = fields['setFriendsList'][0]
            for friend in friendsList:
                if friend in self.onlineToons:
                    self.sendUpdateToAvatarId(friend, 'friendOffline', [doId])
            if doId in self.onlineToons:
                self.onlineToons.remove(doId)
            if doId in self.toon2data:
                del self.toon2data[doId]
        self.air.dbInterface.queryObject(self.air.dbId, doId, handleToon)

    # -- Clear List --
    def clearList(self, doId):
        newOperation = ClearListOperation(self, self.air, doId)
        self.operations.append(newOperation)
        newOperation.demand('Start')

    # -- Teleport and Whispers --
    def routeTeleportQuery(self, toId):
        fromId = self.air.getAvatarIdFromSender()
        if fromId in list(self.tpRequests.values()):
            return
        self.tpRequests[fromId] = toId
        self.sendUpdateToAvatarId(toId, 'teleportQuery', [fromId])
        taskMgr.doMethodLater(5, self.giveUpTeleportQuery, 'tp-query-timeout-%d' % fromId, extraArgs=[fromId, toId])

    def giveUpTeleportQuery(self, fromId, toId):
        # The client didn't respond to the query within the set time,
        # So we will tell the query sender that the toon is unavailable.
        if fromId in self.tpRequests:
            del self.tpRequests[fromId]
            self.sendUpdateToAvatarId(fromId, 'setTeleportResponse', [toId, 0, 0, 0, 0])
            self.notify.warning('Teleport request that was sent by %d to %d timed out.' % (fromId, toId))

    def teleportResponse(self, toId, available, shardId, hoodId, zoneId):
        # Here is where the toId and fromId swap (because we are now sending it back)
        fromId = self.air.getAvatarIdFromSender()

        # We got the query response, so no need to give up!
        if taskMgr.hasTaskNamed('tp-query-timeout-%d' % toId):
            taskMgr.remove('tp-query-timeout-%d' % toId)

        if toId not in self.tpRequests:
            return
        if self.tpRequests.get(toId) != fromId:
            self.air.writeServerEvent('suspicious', fromId, 'toon tried to send teleportResponse for a query that isn\'t theirs!')
            return
        self.sendUpdateToAvatarId(toId, 'setTeleportResponse', [fromId, available, shardId, hoodId, zoneId])
        del self.tpRequests[toId]

    def whisperSCTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        currStamp = time.time()
        if fromId in self.whisperRequests:
            elapsed = currStamp - self.whisperRequests[fromId]
            if elapsed < self.delayTime:
                self.whisperRequests[fromId] = currStamp
                return
        self.whisperRequests[fromId] = currStamp
        self.sendUpdateToAvatarId(toId, 'setWhisperSCFrom', [fromId, msgIndex])

    def whisperSCCustomTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        currStamp = time.time()
        if fromId in self.whisperRequests:
            elapsed = currStamp - self.whisperRequests[fromId]
            if elapsed < self.delayTime:
                self.whisperRequests[fromId] = currStamp
                return
        self.whisperRequests[fromId] = currStamp
        self.sendUpdateToAvatarId(toId, 'setWhisperSCCustomFrom', [fromId, msgIndex])

    def whisperSCEmoteTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        currStamp = time.time()
        if fromId in self.whisperRequests:
            elapsed = currStamp - self.whisperRequests[fromId]
            if elapsed < self.delayTime:
                self.whisperRequests[fromId] = currStamp
                return
        self.whisperRequests[fromId] = currStamp
        self.sendUpdateToAvatarId(toId, 'setWhisperSCEmoteFrom', [fromId, msgIndex])

    def sendTalkWhisper(self, toId, message):
        fromId = self.air.getAvatarIdFromSender()
        currStamp = time.time()
        if fromId in self.whisperRequests:
            elapsed = currStamp - self.whisperRequests[fromId]
            if elapsed < self.delayTime:
                self.whisperRequests[fromId] = currStamp
                return
        self.whisperRequests[fromId] = currStamp
        self.sendUpdateToAvatarId(toId, 'receiveTalkWhisper', [fromId, message])
        self.air.writeServerEvent('whisper-said', fromId, toId, message)

    # -- Routes --
    def battleSOS(self, toId):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setBattleSOS', [requester])

    def teleportGiveup(self, toId):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setTeleportGiveup', [requester])

    def whisperSCToontaskTo(self, toId, taskId, toNpcId, toonProgress, msgIndex):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setWhisperSCToontaskFrom', [requester,
            taskId, toNpcId, toonProgress, msgIndex]
        )

    def sleepAutoReply(self, toId):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setSleepAutoReply', [requester])

    def getToonAccess(self, doId):
        return self.toon2data.get(doId, {}).get('access', 0)
        
    def getToonName(self, doId):
        return self.toon2data.get(doId, {}).get('name', '???')
        
    def getToonAccId(self, doId):
        return self.toon2data.get(doId, {}).get('accId', 0)

    def addToonData(self, doId, fields):
        data = {}
        data['access'] = fields.get('setAdminAccess', [0])[0]
        data['name'] = fields['setName'][0]
        data['accId'] = fields.get('setDISLid', [0])[0]
        self.toon2data[doId] = data
