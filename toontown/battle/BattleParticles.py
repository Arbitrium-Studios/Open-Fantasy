from direct.particles.ParticleEffect import *
import os
from direct.directnotify import DirectNotifyGlobal
notify = DirectNotifyGlobal.directNotify.newCategory('BattleParticles')
TutorialParticleEffects = (
    'gearExplosionBig.ptf',
    'gearExplosionSmall.ptf',
    'gearExplosion.ptf')
ParticleNames = (
    'audit-div',
    'audit-five',
    'audit-four',
    'audit-minus',
    'audit-mult',
    'audit-one',
    'audit-plus',
    'audit-six',
    'audit-three',
    'audit-two',
    'blah',
    'brainstorm-box',
    'brainstorm-env',
    'brainstorm-track',
    'buzzwords-crash',
    'buzzwords-inc',
    'buzzwords-main',
    'buzzwords-over',
    'buzzwords-syn',
    'confetti',
    'doubletalk-double',
    'doubletalk-dup',
    'doubletalk-good',
    'filibuster-cut',
    'filibuster-fiscal',
    'filibuster-impeach',
    'filibuster-inc',
    'jargon-brow',
    'jargon-deep',
    'jargon-hoop',
    'jargon-ipo',
    'legalese-hc',
    'legalese-qpq',
    'legalese-vd',
    'mumbojumbo-boiler',
    'mumbojumbo-creative',
    'mumbojumbo-deben',
    'mumbojumbo-high',
    'mumbojumbo-iron',
    'poundsign',
    'schmooze-genius',
    'schmooze-instant',
    'schmooze-master',
    'schmooze-viz',
    'roll-o-dex',
    'rollodex-card',
    'dagger',
    'fire',
    'snow-particle',
    'raindrop',
    'gear',
    'checkmark',
    'dollar-sign',
    'spark')
particleModel = None
particleSearchPath = None


def loadParticles():
    global particleModel
    if particleModel is None:
        particleModel = loader.loadModel(
            'phase_3.5/models/props/suit-particles')
    return


def unloadParticles():
    global particleModel
    if particleModel is not None:
        particleModel.removeNode()
    del particleModel
    particleModel = None
    return


def getParticle(name):
    if name in ParticleNames:
        particle = particleModel.find('**/' + str(name))
        return particle
    else:
        notify.warning('getParticle() - no name: %s' % name)
        return None
    return None


def loadParticleFile(name):
    global particleSearchPath
    if particleSearchPath is None:
        particleSearchPath = DSearchPath()
        if __debug__:
            particleSearchPath.appendDirectory(
                Filename('resources/phase_3.5/etc'))
            particleSearchPath.appendDirectory(
                Filename('resources/phase_4/etc'))
            particleSearchPath.appendDirectory(
                Filename('resources/phase_5/etc'))
            particleSearchPath.appendDirectory(
                Filename('resources/phase_8/etc'))
            particleSearchPath.appendDirectory(
                Filename('resources/phase_9/etc'))

    pfile = Filename(name)
    found = vfs.resolveFilename(pfile, particleSearchPath)
    if not found:
        notify.warning('loadParticleFile() - no path: %s' % name)
        return
    notify.debug('Loading particle file: %s' % pfile)
    effect = ParticleEffect()
    effect.loadConfig(pfile)
    return effect


def createParticleEffect(name=None, file=None, numParticles=None, color=None):
    if not name:
        fileName = file + '.ptf'
        return loadParticleFile(fileName)
    match name:
        case 'GearExplosion':
            return __makeGearExplosion(numParticles)
        case 'BigGearExplosion':
            return __makeGearExplosion(numParticles, 'Big')
        case 'WideGearExplosion':
            return __makeGearExplosion(numParticles, 'Wide')
        case 'BrainStorm':
            return loadParticleFile('brainStorm.ptf')
        case 'BuzzWord':
            return loadParticleFile('buzzWord.ptf')
        case 'Calculate':
            return loadParticleFile('calculate.ptf')
        case 'Confetti':
            return loadParticleFile('confetti.ptf')
        case 'DemotionFreeze':
            return loadParticleFile('demotionFreeze.ptf')
        case 'DemotionSpray':
            return loadParticleFile('demotionSpray.ptf')
        case 'DoubleTalkLeft':
            return loadParticleFile('doubleTalkLeft.ptf')
        case 'DoubleTalkRight':
            return loadParticleFile('doubleTalkRight.ptf')
        case 'FingerWag':
            return loadParticleFile('fingerwag.ptf')
        case 'FiredFlame':
            return loadParticleFile('firedFlame.ptf')
        case 'FreezeAssets':
            return loadParticleFile('freezeAssets.ptf')
        case 'GlowerPower':
            return loadParticleFile('glowerPowerKnives.ptf')
        case 'HotAir':
            return loadParticleFile('hotAirSpray.ptf')
        case 'PoundKey':
            return loadParticleFile('poundkey.ptf')
        case 'ShiftSpray':
            return loadParticleFile('shiftSpray.ptf')
        case 'ShiftLift':
            return __makeShiftLift()
        case 'Shred':
            return loadParticleFile('shred.ptf')
        case 'Smile':
            return loadParticleFile('smile.ptf')
        case 'SpriteFiredFlecks':
            return loadParticleFile('spriteFiredFlecks.ptf')
        case 'Synergy':
            return loadParticleFile('synergy.ptf')
        case 'Waterfall':
            return loadParticleFile('waterfall.ptf')
        case 'PoundKey':
            return loadParticleFile('poundkey.ptf')
        case 'RubOut':
            return __makeRubOut(color)
        case 'SplashLines':
            return loadParticleFile('splashlines.ptf')
        case 'Withdrawal':
            return loadParticleFile('withdrawal.ptf')
        case _:
            notify.warning('createParticleEffect() - no name: %s' % name)
    return None


def setEffectTexture(effect, name, color=None):
    particles = effect.getParticlesNamed('particles-1')
    np = getParticle(name)
    if color:
        particles.renderer.setColor(color)
    particles.renderer.setFromNode(np)


def __makeGearExplosion(numParticles=None, style='Normal'):
    match style:
        case 'Normal':
            effect = loadParticleFile('gearExplosion.ptf')
        case 'Big':
            effect = loadParticleFile('gearExplosionBig.ptf')
        case 'Wide':
            effect = loadParticleFile('gearExplosionWide.ptf')
    if numParticles:
        particles = effect.getParticlesNamed('particles-1')
        particles.setPoolSize(numParticles)
    return effect


def __makeRubOut(color=None):
    effect = loadParticleFile('demotionUnFreeze.ptf')
    loadParticles()
    setEffectTexture(effect, 'snow-particle')
    particles = effect.getParticlesNamed('particles-1')
    particles.renderer.setInitialXScale(0.03)
    particles.renderer.setFinalXScale(0.0)
    particles.renderer.setInitialYScale(0.02)
    particles.renderer.setFinalYScale(0.0)
    if color:
        particles.renderer.setColor(color)
    else:
        particles.renderer.setColor(Vec4(0.54, 0.92, 0.32, 0.7))
    return effect


def __makeShiftLift():
    effect = loadParticleFile('pixieDrop.ptf')
    particles = effect.getParticlesNamed('particles-1')
    particles.renderer.setCenterColor(Vec4(1, 1, 0, 0.9))
    particles.renderer.setEdgeColor(Vec4(1, 1, 0, 0.6))
    particles.emitter.setRadius(0.01)
    effect.setHpr(0, 180, 0)
    effect.setPos(0, 0, 0)
    return effect
