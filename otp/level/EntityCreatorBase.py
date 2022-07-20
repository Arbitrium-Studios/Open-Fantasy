"""EntityCreatorBase module: contains the EntityCreatorBase class"""

from direct.directnotify import DirectNotifyGlobal

class EntityCreatorBase:
    """This class is responsible for creating instances of Entities on the
    AI and on the client. It must be subclassed to specify what entity
    types it can create, and to provide the creation implementation."""
    notify = DirectNotifyGlobal.directNotify.newCategory('EntityCreator')

    def __init__(self, level):
        self.level = level
        self.entType2Ctor = {}

    def createEntity(self, entId):
        entType = self.level.getEntityType(entId)
        
        if entType not in self.entType2Ctor:
            self.notify.error('unknown entity type: %s (ent%s)' %
                              (entType, entId))

        # inheritor must define doCreateEntity
        ent = self.doCreateEntity(self.entType2Ctor[entType], entId)
        assert ent is not None # must be Entity or 'nothing'
        return ent

    def getEntityTypes(self):
        """by definition, this object knows the full list of entity types
        that may exist within the level"""
        return list(self.entType2Ctor.keys())

    def privRegisterType(self, entType, ctor):
        if entType in self.entType2Ctor:
            self.notify.debug('replacing %s ctor %s with %s' %
                              (entType, self.entType2Ctor[entType], ctor))
        self.entType2Ctor[entType] = ctor

    def privRegisterTypes(self, type2ctor):
        for entType, ctor in list(type2ctor.items()):
            self.privRegisterType(entType, ctor)
