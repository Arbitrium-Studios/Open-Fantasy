from direct.distributed import DistributedObject
from . import Entity
from direct.directnotify import DirectNotifyGlobal

class DistributedEntity(DistributedObject.DistributedObject, Entity.Entity):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedEntity')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        Entity.Entity.__init__(self)

        self.levelDoId = 0
        self.entId = 0
        self.level = None

    def generateInit(self):
        DistributedEntity.notify.debug('generateInit')
        DistributedObject.DistributedObject.generateInit(self)
        # load stuff

    def generate(self):
        DistributedEntity.notify.debug('generate')
        DistributedObject.DistributedObject.generate(self)

    def setLevelDoId(self, levelDoId):
        DistributedEntity.notify.debug('setLevelDoId: %s' % levelDoId)
        self.levelDoId = levelDoId

    def setEntId(self, entId):
        DistributedEntity.notify.debug('setEntId: %s' % entId)
        self.entId = entId

    def announceGenerate(self):
        ###
        ### THIS IS WHERE CLIENT-SIDE DISTRIBUTED ENTITIES GET THEIR
        ### ATTRIBUTES SET
        ###
        DistributedEntity.notify.debug('announceGenerate (%s)' % self.entId)

        # ask our level obj for our spec data
        if self.levelDoId != 0:
            level = base.cr.doId2do[self.levelDoId]
            self.initializeEntity(level, self.entId)
            # announce our presence (Level does this for non-distributed entities)
            self.level.onEntityCreate(self.entId)

        else:
            # We don't have a level.  This probably indicates an
            # intention to create an Entity unassociated with any
            # particular level (e.g. a Goon).
            self.level = None

        DistributedObject.DistributedObject.announceGenerate(self)

    def disable(self):
        DistributedEntity.notify.debug('disable (%s)' % self.entId)
        # stop things
        self.destroy()
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        DistributedEntity.notify.debug('delete')
        # unload things
        DistributedObject.DistributedObject.delete(self)
