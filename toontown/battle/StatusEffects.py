'''
This file will contain all of the status effect classes needed for shaking up the battle.
'''

# General
class StatusEffect:
    '''
    This status effect serves as the parent class for all status effects.
    '''

    def __init__(self, currRounds: int, maxRounds: int | None = None) -> None:
        '''
        Parameters:
            currRounds (int): Determines how many rounds are currently left for this status effect.  Use -1 if this status effect is permanent unless forcefully removed.
            maxRounds (int|None): The maximum number of rounds this status effect can go for.  This can be as short as one round.  None means that there is no limit as to how many turns this status effect can have.

        Raises:
            TypeError: TypeError is raised if currRounds is not an int.<br/>
                       TypeError is raised if maxRounds is not an int or a NoneType.
            ValueError: ValueError is raised if currRounds is less than -1.<br/>
                        ValueError is raised if maxRounds is neither None nor at least 1.
        '''
        if not isinstance(currRounds, int):
            raise TypeError
        if currRounds < -1:
            raise ValueError('currRounds must be greater than or equal to -1 (got {} instead).'.format(currRounds))
        if not isinstance(maxRounds, (int, type(None))):
            raise TypeError
        if isinstance(maxRounds, int): # Do this check so that we know it's not a NoneType.
            if maxRounds < 1:
                raise ValueError('maxRounds must be greater than or equal to 1 (got {} instead).'.format(maxRounds))
        self.currRounds: int = currRounds
        self.maxRounds: int | None = maxRounds
        self.good: bool = False # In case we want to clear a bad status effect from a Cog, use this attribute.  A status effect with no change should default to False so that excess bloat can be removed.
    
    def updateEffect(self) -> None:
        '''
        This method is inherited by every status effect in case we want to change something in it by the turn.
        '''
        pass

    def decrementRounds(self) -> None:
        '''
        Every turn, a status effect's rounds decrement.  We can also use this to call updateEffect and have an effect update every turn.
        '''
        self.currRounds -= 1
        self.updateEffect()

class DamageModifier(StatusEffect):
    '''
    Modify how much damage a combatant deals.
    '''

    def __init__(self, currRounds: int, damageMod: int | float, **kwargs) -> None:
        '''
        Parameters:
            damageMod (int|float): A change in how much damage is dealt.  It can either be an int for a flat damage change or a float for a multiplier.

        Raises:
            TypeError: TypeError is raised if damageMod is not an int or a float.
        '''
        if not isinstance(damageMod, (int, float)):
            raise TypeError
        StatusEffect.__init__(self, currRounds, **kwargs)
        self.damageMod: int | float = damageMod
        # Sometimes, we can use updateEffect() while initializing in cases we want to put something on a status effect immediately.
        self.updateEffect()
    
    def updateEffect(self) -> None:
        '''
        If this effect ever gets updated for some reason, update whether or not it is still good.
        '''
        # Begin by checking the data type of our damage modifier.
        if isinstance(self.damageMod, int):
            self.good = self.damageMod > 0
        else:
            self.good = self.damageMod > 1.0

class DefenseModifier(StatusEffect):
    '''
    Modify how much damage a combatant takes.
    '''

    def __init__(self, currRounds: int, defenseMod: int | float, **kwargs) -> None:
        '''
        :param int|float defenseMod: A change in how much damage is taken.  It can either be an int for a flat damage change or a float for a multiplier.

        :raise TypeError: TypeError is raised if defenseMod is not an int or a float.
        '''
        if not isinstance(defenseMod, (int, float)):
            raise TypeError
        StatusEffect.__init__(self, currRounds, **kwargs)
        self.defenseMod: int | float = defenseMod
        self.updateEffect()
    
    def updateEffect(self) -> None:
        '''
        If this effect ever gets updated for some reason, update whether or not it is still good.
        '''
        # Begin by checking the data type of our defense modifier.
        if isinstance(self.defenseMod, int):
            self.good = self.defenseMod < 0
        else:
            self.good = self.defenseMod < 1.0

class AccuracyModifier(StatusEffect):
    '''
    Modify how much accuracy a combatant has while attacking.
    '''

    def __init__(self, currRounds: int, accuracyMod: int | float, **kwargs) -> None:
        '''
        :param int|float accuracyMod: A change in accuracy.  It can either be an int for flat accuracy change or a float for a multiplier.\n
                                      NOTE: If it is a float, it must not be greater than 1.0!  Those values can get ridiculous (e.g. Squirt accuracy can too easily exceed the 100% accuracy cap), and we'll throw an error to prevent that; less than 1.0 is more manageable.
        
        :raise ValueError: ValueError is raised if accuracyMod is a float greater than 1.0.
        '''
        if isinstance(accuracyMod, float):
            if accuracyMod > 1.0:
                raise ValueError("accuracyMod float exceeds 1.0 (it's {})!".format(accuracyMod))
        elif not isinstance(accuracyMod, int):
            raise TypeError
        StatusEffect.__init__(self, currRounds, **kwargs)
        self.accuracyMod = accuracyMod
        self.updateEffect()
    
    def updateEffect(self) -> None:
        '''
        If this effect ever gets updated for some reason, update whether or not it is still good.
        '''
        if isinstance(self.accuracyMod, float):
            self.good = False # self.accuracyMod as a float should never exceed 1.0 for any reason, though we currently have no way to make sure it stays that way.  For now, assume that it can never exceed that.
        else:
            self.good = self.accuracyMod > 0

class DamageOverTime(StatusEffect):
    '''
    Force a combatant to take damage every round until expiry.
    '''

    def __init__(self, currRounds: int, damagePerRound: int, **kwargs) -> None:
        '''
        :param int damagePerRound: How much damage will be dealt per round.  Alternatively, a negative value will cause healing... maybe... depending... I don't know.  ~Professor Control

        :raise TypeError: TypeError is raised if damagePerRound is not an int.
        '''
        if not isinstance(damagePerRound, int):
            raise TypeError
        StatusEffect.__init__(self, currRounds, **kwargs)
        self.damagePerRound: int = damagePerRound
        self.updateEffect()

    def updateEffect(self) -> None:
        '''
        If this effect ever gets updated for some reason, update whether or not it is still good.
        '''
        self.good = self.damagePerRound < 0
