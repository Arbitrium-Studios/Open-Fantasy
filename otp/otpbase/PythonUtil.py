import builtins
import sys
import math
import random
import time
from html.parser import HTMLParser
from direct.showbase.PythonUtil import *

__all__ = ['enumerate', 'nonRepeatingRandomList', 'describeException', 'pdir', 'choice', 'cmp', 'lerp', 'triglerp', 'Enum']

class EnumIter:
    def __init__(self, enum):
        self._values = tuple(enum._stringTable.keys())
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index >= len(self._values):
            raise StopIteration
        self._index += 1
        return self._values[self._index-1]

class Enum:
    """Pass in list of strings or string of comma-separated strings.
    Items are accessible as instance.item, and are assigned unique,
    increasing integer values. Pass in integer for 'start' to override
    starting value.
    Example:
    >>> colors = Enum('red, green, blue')
    >>> colors.red
    0
    >>> colors.green
    1
    >>> colors.blue
    2
    >>> colors.getString(colors.red)
    'red'
    """

    if __debug__:
        # chars that cannot appear within an item string.
        def _checkValidIdentifier(item):
            import string
            invalidChars = string.whitespace + string.punctuation
            invalidChars = invalidChars.replace('_', '')
            invalidFirstChars = invalidChars+string.digits
            if item[0] in invalidFirstChars:
                raise SyntaxError("Enum '%s' contains invalid first char" %
                                    item)
            if not disjoint(item, invalidChars):
                for char in item:
                    if char in invalidChars:
                        raise SyntaxError(
                            "Enum\n'%s'\ncontains illegal char '%s'" %
                            (item, char))
            return 1
        _checkValidIdentifier = staticmethod(_checkValidIdentifier)

    def __init__(self, items, start=0):
        if isinstance(items, str):
            items = items.split(',')

        self._stringTable = {}

        # make sure we don't overwrite an existing element of the class
        assert self._checkExistingMembers(items)
        assert uniqueElements(items)

        i = start
        for item in items:
            # remove leading/trailing whitespace
            item = item.strip()
            # is there anything left?
            if len(item) == 0:
                continue
            # make sure there are no invalid characters
            assert Enum._checkValidIdentifier(item)
            self.__dict__[item] = i
            self._stringTable[i] = item
            i += 1

    def __iter__(self):
        return EnumIter(self)

    def hasString(self, string):
        return string in set(self._stringTable.values())

    def fromString(self, string):
        if self.hasString(string):
            return self.__dict__[string]
        # throw an error
        {}[string]

    def getString(self, value):
        return self._stringTable[value]

    def __contains__(self, value):
        return value in self._stringTable

    def __len__(self):
        return len(self._stringTable)

    def copyTo(self, obj):
        # copies all members onto obj
        for name, value in self._stringTable:
            setattr(obj, name, value)

    if __debug__:
        def _checkExistingMembers(self, items):
            for item in items:
                if hasattr(self, item):
                    return 0
            return 1

if not hasattr(builtins, 'enumerate'):
    def enumerate(L):
        """Returns (0, L[0]), (1, L[1]), etc., allowing this syntax:
        for i, item in enumerate(L):
           ...

        enumerate is a built-in feature in Python 2.3, which implements it
        using an iterator. For now, we can use this quick & dirty
        implementation that returns a list of tuples that is completely
        constructed every time enumerate() is called.
        """
        return list(zip(list(range(len(L))), L))

    builtins.enumerate = enumerate
else:
    enumerate = builtins.enumerate


def nonRepeatingRandomList(vals, max):
    random.seed(time.time())
    # first generate a set of random values
    valueList = list(range(max))
    finalVals = []
    for i in range(vals):
        index = int(random.random() * len(valueList))
        finalVals.append(valueList[index])
        valueList.remove(valueList[index])
    return finalVals

# class 'decorator' that records the stack at the time of creation
# be careful with this, it creates a StackTrace, and that can take a
# lot of CPU


def recordCreationStack(cls):
    if not hasattr(cls, '__init__'):
        raise 'recordCreationStack: class \'%s\' must define __init__' % cls.__name__
    cls.__moved_init__ = cls.__init__

    def __recordCreationStack_init__(self, *args, **kArgs):
        self._creationStackTrace = StackTrace(start=1)
        return self.__moved_init__(*args, **kArgs)

    def getCreationStackTrace(self):
        return self._creationStackTrace

    def getCreationStackTraceCompactStr(self):
        return self._creationStackTrace.compact()

    def printCreationStackTrace(self):
        print((self._creationStackTrace))
    cls.__init__ = __recordCreationStack_init__
    cls.getCreationStackTrace = getCreationStackTrace
    cls.getCreationStackTraceCompactStr = getCreationStackTraceCompactStr
    cls.printCreationStackTrace = printCreationStackTrace
    return cls

# __dev__ is not defined at import time, call this after it's defined


def recordFunctorCreationStacks():
    global Functor
    from pandac.PandaModules import getConfigShowbase
    config = getConfigShowbase()
    # off by default, very slow
    if __dev__ and config.GetBool('record-functor-creation-stacks', 0):
        if not hasattr(Functor, '_functorCreationStacksRecorded'):
            Functor = recordCreationStackStr(Functor)
            Functor._functorCreationStacksRecorded = True
            Functor.__call__ = Functor._exceptionLoggedCreationStack__call__


def describeException(backTrace=4):
    # When called in an exception handler, returns a string describing
    # the current exception.

    def byteOffsetToLineno(code, byte):
        # Returns the source line number corresponding to the given byte
        # offset into the indicated Python code module.

        import array
        lnotab = array.array('B', code.co_lnotab)

        line = code.co_firstlineno
        for i in range(0, len(lnotab), 2):
            byte -= lnotab[i]
            if byte <= 0:
                return line
            line += lnotab[i + 1]

        return line

    infoArr = sys.exc_info()
    exception = infoArr[0]
    exceptionName = getattr(exception, '__name__', None)
    extraInfo = infoArr[1]
    trace = infoArr[2]

    stack = []
    while trace.tb_next:
        # We need to call byteOffsetToLineno to determine the true
        # line number at which the exception occurred, even though we
        # have both trace.tb_lineno and frame.f_lineno, which return
        # the correct line number only in non-optimized mode.
        frame = trace.tb_frame
        module = frame.f_globals.get('__name__', None)
        lineno = byteOffsetToLineno(frame.f_code, frame.f_lasti)
        stack.append("%s:%s, " % (module, lineno))
        trace = trace.tb_next

    frame = trace.tb_frame
    module = frame.f_globals.get('__name__', None)
    lineno = byteOffsetToLineno(frame.f_code, frame.f_lasti)
    stack.append("%s:%s, " % (module, lineno))

    description = ""
    for i in range(len(stack) - 1, max(len(stack) - backTrace, 0) - 1, -1):
        description += stack[i]

    description += "%s: %s" % (exceptionName, extraInfo)
    return description


def pdir(obj, str=None, width=None,
         fTruncate=1, lineWidth=75, wantPrivate=0):
    # Remove redundant class entries
    uniqueLineage = []
    for l in getClassLineage(obj):
        if isinstance(l, type):
            if l in uniqueLineage:
                break
        uniqueLineage.append(l)
    # Pretty print out directory info
    uniqueLineage.reverse()
    for obj in uniqueLineage:
        _pdir(obj, str, width, fTruncate, lineWidth, wantPrivate)
        print()


def lerp(v0, v1, t):
    """
    returns a value lerped between v0 and v1, according to t
    t == 0 maps to v0, t == 1 maps to v1
    """
    return v0 + ((v1 - v0) * t)


def triglerp(v0, v1, t):
    """
    lerp using the curve of sin(-pi/2) -> sin(pi/2)
    """
    x = lerp(-math.pi / 2, math.pi / 2, t)
    v = math.sin(x)
    return lerp(v0, v1, (v + 1.) / 2.)


def choice(condition, ifTrue, ifFalse):
    # equivalent of C++ (condition ? ifTrue : ifFalse)
    if condition:
        return ifTrue
    else:
        return ifFalse


def quantize(value, divisor):
    # returns new value that is multiple of (1. / divisor)
    return float(int(value * int(divisor))) / int(divisor)


def quantizeVec(vec, divisor):
    # in-place
    vec[0] = quantize(vec[0], divisor)
    vec[1] = quantize(vec[1], divisor)
    vec[2] = quantize(vec[2], divisor)


def isClient():
    if hasattr(builtins, 'simbase') and not hasattr(builtins, 'base'):
        return False
    return True


def cmp(a, b):
    return (a > b) - (a < b)


def addListsByValue(a, b):
    """
    returns a new array containing the sums of the two array arguments
    (c[0] = a[0 + b[0], etc.)
    """
    c = []
    for x, y in zip(a, b):
        c.append(x + y)
    return c


def nonRepeatingRandomList(vals, max):
    random.seed(time.time())
    # first generate a set of random values
    valueList = list(range(max))
    finalVals = []
    for i in range(vals):
        index = int(random.random() * len(valueList))
        finalVals.append(valueList[index])
        valueList.remove(valueList[index])
    return finalVals


class HTMLStringToElements(HTMLParser):
    def __init__(self, str, *a, **kw):
        self._elements = []
        self._elementStack = Stack()
        HTMLParser.__init__(self, *a, **kw)
        self.feed(str)
        self.close()

    def getElements(self):
        return self._elements

    def _handleNewElement(self, element):
        if len(self._elementStack):
            self._elementStack.top().append(element)
        else:
            self._elements.append(element)
        self._elementStack.push(element)

    def handle_starttag(self, tag, attrs):
        kwArgs = {}
        for name, value in attrs:
            kwArgs[name] = value
        el = ET.Element(tag, **kwArgs)
        self._handleNewElement(el)

    def handle_data(self, data):
        # this ignores text outside of a tag
        if len(self._elementStack):
            self._elementStack.top().text = data

    def handle_endtag(self, tag):
        top = self._elementStack.top()
        if len(top.getchildren()) == 0:
            # insert a comment to prevent ElementTree from using <... /> convention
            # force it to create a tag closer a la </tag>
            # prevents problems in certain browsers
            if top.tag == 'script' and top.get('type') == 'text/javascript':
                if top.text is None:
                    top.text = '// force tag closer'
            else:
                self.handle_comment('force tag closer')
                self._elementStack.pop()
        self._elementStack.pop()

    def handle_comment(self, data):
        comment = ET.Comment(data)
        self._handleNewElement(comment)


def str2elements(str):
    return HTMLStringToElements(str).getElements()


def unescapeHtmlString(s):
    # converts %## to corresponding character
    # replaces '+' with ' '
    result = ''
    i = 0
    while i < len(s):
        char = s[i]
        if char == '+':
            char = ' '
        elif char == '%':
            if i < (len(s) - 2):
                num = eval('0x' + s[i + 1:i + 3])
                char = chr(num)
                i += 2
        i += 1
        result += char
    return result


def randUint32(rng=random.random):
    """returns a random integer in [0..2^32).
    rng must return float in [0..1]"""
    return int(rng() * 0xFFFFFFFF)


"""
ParamObj/ParamSet
=================
These two classes support you in the definition of a formal set of
parameters for an object type. The parameters may be safely queried/set on
an object instance at any time, and the object will react to newly-set
values immediately.
ParamSet & ParamObj also provide a mechanism for atomically setting
multiple parameter values before allowing the object to react to any of the
new values--useful when two or more parameters are interdependent and there
is risk of setting an illegal combination in the process of applying a new
set of values.
To make use of these classes, derive your object from ParamObj. Then define
a 'ParamSet' subclass that derives from the parent class' 'ParamSet' class,
and define the object's parameters within its ParamSet class. (see examples
below)
The ParamObj base class provides 'get' and 'set' functions for each
parameter if they are not defined. These default implementations
respectively set the parameter value directly on the object, and expect the
value to be available in that location for retrieval.
Classes that derive from ParamObj can optionally declare a 'get' and 'set'
function for each parameter. The setter should simply store the value in a
location where the getter can find it; it should not do any further
processing based on the new parameter value. Further processing should be
implemented in an 'apply' function. The applier function is optional, and
there is no default implementation.
NOTE: the previous value of a parameter is available inside an apply
function as 'self.getPriorValue()'
The ParamSet class declaration lists the parameters and defines a default
value for each. ParamSet instances represent a complete set of parameter
values. A ParamSet instance created with no constructor arguments will
contain the default values for each parameter. The defaults may be
overriden by passing keyword arguments to the ParamSet's constructor. If a
ParamObj instance is passed to the constructor, the ParamSet will extract
the object's current parameter values.
ParamSet.applyTo(obj) sets all of its parameter values on 'obj'.
SETTERS AND APPLIERS
====================
Under normal conditions, a call to a setter function, i.e.
 cam.setFov(90)
will actually result in the following calls being made:
 cam.setFov(90)
 cam.applyFov()
Calls to several setter functions, i.e.
 cam.setFov(90)
 cam.setViewType('cutscene')
will result in this call sequence:
 cam.setFov(90)
 cam.applyFov()
 cam.setViewType('cutscene')
 cam.applyViewType()
Suppose that you desire the view type to already be set to 'cutscene' at
the time when applyFov() is called. You could reverse the order of the set
calls, but suppose that you also want the fov to be set properly at the
time when applyViewType() is called.
In this case, you can 'lock' the params, i.e.
 cam.lockParams()
 cam.setFov(90)
 cam.setViewType('cutscene')
 cam.unlockParams()
This will result in the following call sequence:
 cam.setFov(90)
 cam.setViewType('cutscene')
 cam.applyFov()
 cam.applyViewType()
NOTE: Currently the order of the apply calls following an unlock is not
guaranteed.
EXAMPLE CLASSES
===============
Here is an example of a class that uses ParamSet/ParamObj to manage its
parameters:
class Camera(ParamObj):
    class ParamSet(ParamObj.ParamSet):
        Params = {
            'viewType': 'normal',
            'fov': 60,
            }
    ...
    def getViewType(self):
        return self.viewType
    def setViewType(self, viewType):
        self.viewType = viewType
    def applyViewType(self):
        if self.viewType == 'normal':
            ...
    def getFov(self):
        return self.fov
    def setFov(self, fov):
        self.fov = fov
    def applyFov(self):
        base.camera.setFov(self.fov)
    ...
EXAMPLE USAGE
=============
cam = Camera()
...
# set up for the cutscene
savedSettings = cam.ParamSet(cam)
cam.setViewType('closeup')
cam.setFov(90)
...
# cutscene is over, set the camera back
savedSettings.applyTo(cam)
del savedSettings
"""


class ParamObj:
    # abstract base for classes that want to support a formal parameter
    # set whose values may be queried, changed, 'bulk' changed (defer reaction
    # to changes until multiple changes have been performed), and
    # extracted/stored/applied all at once (see documentation above)

    # ParamSet subclass: container of parameter values. Derived class must
    # derive a new ParamSet class if they wish to define new params. See
    # documentation above.
    class ParamSet:
        Params = {
            # base class does not define any parameters, but they would
            # appear here as 'name': defaultValue,
            #
            # WARNING: default values of mutable types that do not copy by
            # value (dicts, lists etc.) will be shared by all class instances
            # if default value is callable, it will be called to get actual
            # default value
            #
            # for example:
            #
            # class MapArea(ParamObj):
            #     class ParamSet(ParamObj.ParamSet):
            #         Params = {
            #             'spawnIndices': Functor(list, [1,5,22]),
            #         }
            #
        }

        def __init__(self, *args, **kwArgs):
            self.__class__._compileDefaultParams()
            if len(args) == 1 and len(kwArgs) == 0:
                # extract our params from an existing ParamObj instance
                obj = args[0]
                self.paramVals = {}
                for param in self.getParams():
                    self.paramVals[param] = getSetter(obj, param, 'get')()
            else:
                assert len(args) == 0
                if __debug__:
                    for arg in list(kwArgs.keys()):
                        assert arg in self.getParams()
                self.paramVals = dict(kwArgs)

        def getValue(self, param):
            if param in self.paramVals:
                return self.paramVals[param]
            return self._Params[param]

        def applyTo(self, obj):
            # Apply our entire set of params to a ParamObj
            obj.lockParams()
            for param in self.getParams():
                getSetter(obj, param)(self.getValue(param))
            obj.unlockParams()

        def extractFrom(self, obj):
            # Extract our entire set of params from a ParamObj
            obj.lockParams()
            for param in self.getParams():
                self.paramVals[param] = getSetter(obj, param, 'get')()
            obj.unlockParams()

        @classmethod
        def getParams(cls):
            # returns safely-mutable list of param names
            cls._compileDefaultParams()
            return list(cls._Params.keys())

        @classmethod
        def getDefaultValue(cls, param):
            cls._compileDefaultParams()
            dv = cls._Params[param]
            if hasattr(dv, '__call__'):
                dv = dv()
            return dv

        @classmethod
        def _compileDefaultParams(cls):
            if '_Params' in cls.__dict__:
                # we've already compiled the defaults for this class
                return
            bases = list(cls.__bases__)
            if object in bases:
                bases.remove(object)
            # bring less-derived classes to the front
            mostDerivedLast(bases)
            cls._Params = {}
            for c in (bases + [cls]):
                # make sure this base has its dict of param defaults
                c._compileDefaultParams()
                if 'Params' in c.__dict__:
                    # apply this class' default param values to our dict
                    cls._Params.update(c.Params)
            del bases

        def __repr__(self):
            argStr = ''
            for param in self.getParams():
                argStr += '%s=%s,' % (param,
                                      repr(self.getValue(param)))
            return '%s.%s(%s)' % (
                self.__class__.__module__, self.__class__.__name__, argStr)
    # END PARAMSET SUBCLASS

    def __init__(self, *args, **kwArgs):
        assert issubclass(self.ParamSet, ParamObj.ParamSet)
        # If you pass in a ParamSet obj, its values will be applied to this
        # object in the constructor.
        params = None
        if len(args) == 1 and len(kwArgs) == 0:
            # if there's one argument, assume that it's a ParamSet
            params = args[0]
        elif len(kwArgs) > 0:
            assert len(args) == 0
            # if we've got keyword arguments, make a ParamSet out of them
            params = self.ParamSet(**kwArgs)

        self._paramLockRefCount = 0
        # these hold the current value of parameters while they are being set to
        # a new value, to support getPriorValue()
        self._curParamStack = []
        self._priorValuesStack = []

        # insert stub funcs for param setters, to handle locked params
        for param in self.ParamSet.getParams():

            # set the default value on the object
            setattr(self, param, self.ParamSet.getDefaultValue(param))

            setterName = getSetterName(param)
            getterName = getSetterName(param, 'get')

            # is there a setter defined?
            if not hasattr(self, setterName):
                # no; provide the default
                def defaultSetter(self, value, param=param):
                    # print '%s=%s for %s' % (param, value, id(self))
                    setattr(self, param, value)
                #self.__class__.__dict__[setterName] = defaultSetter
                setattr(self, setterName, defaultSetter)
            # is there a getter defined?
            if not hasattr(self, getterName):
                # no; provide the default. If there is no value set, return
                # the default
                def defaultGetter(self, param=param,
                                  default=self.ParamSet.getDefaultValue(param)):
                    return getattr(self, param, default)
                setattr(self, getterName, defaultGetter)
                #self.__class__.__dict__[getterName] = defaultGetter

            # have we already installed a setter stub?
            origSetterName = '%s_ORIG' % (setterName,)
            if not hasattr(self, origSetterName):
                # move the original setter aside
                origSetterFunc = getattr(self.__class__, setterName)
                setattr(self.__class__, origSetterName, origSetterFunc)
                """
                # if the setter is a direct member of this instance, move the setter
                # aside
                if setterName in self.__dict__:
                    self.__dict__[setterName + '_MOVED'] = self.__dict__[setterName]
                    setterFunc = self.__dict__[setterName]
                    """
                # install a setter stub that will a) call the real setter and
                # then the applier, or b) call the setter and queue the
                # applier, depending on whether our params are locked
                """
                setattr(self, setterName, types.MethodType(
                    Functor(setterStub, param, setterFunc), self, self.__class__))
                    """

                def setterStub(self, value, param=param, origSetterName=origSetterName):
                    # should we apply the value now or should we wait?
                    # if this obj's params are locked, we track which values have
                    # been set, and on unlock, we'll call the applyers for those
                    # values
                    if self._paramLockRefCount > 0:
                        priorValues = self._priorValuesStack[-1]
                        if param not in priorValues:
                            try:
                                priorValue = getSetter(self, param, 'get')()
                            except BaseException:
                                priorValue = None
                            priorValues[param] = priorValue
                        self._paramsSet[param] = None
                        getattr(self, origSetterName)(value)
                    else:
                        # prepare for call to getPriorValue
                        try:
                            priorValue = getSetter(self, param, 'get')()
                        except BaseException:
                            priorValue = None
                        self._priorValuesStack.append({
                            param: priorValue,
                        })
                        getattr(self, origSetterName)(value)
                        # call the applier, if there is one
                        applier = getattr(self, getSetterName(param, 'apply'), None)
                        if applier is not None:
                            self._curParamStack.append(param)
                            applier()
                            self._curParamStack.pop()
                        self._priorValuesStack.pop()
                        if hasattr(self, 'handleParamChange'):
                            self.handleParamChange((param,))

                setattr(self.__class__, setterName, setterStub)

        if params is not None:
            params.applyTo(self)

    def destroy(self):
        """
        for param in self.ParamSet.getParams():
            setterName = getSetterName(param)
            self.__dict__[setterName].destroy()
            del self.__dict__[setterName]
            """
        pass

    def setDefaultParams(self):
        # set all the default parameters on ourself
        self.ParamSet().applyTo(self)

    def getCurrentParams(self):
        params = self.ParamSet()
        params.extractFrom(self)
        return params

    def lockParams(self):
        self._paramLockRefCount += 1
        if self._paramLockRefCount == 1:
            self._handleLockParams()

    def unlockParams(self):
        if self._paramLockRefCount > 0:
            self._paramLockRefCount -= 1
            if self._paramLockRefCount == 0:
                self._handleUnlockParams()

    def _handleLockParams(self):
        # this will store the names of the parameters that are modified
        self._paramsSet = {}
        # this will store the values of modified params (from prior to
        # the lock).
        self._priorValuesStack.append({})

    def _handleUnlockParams(self):
        for param in self._paramsSet:
            # call the applier, if there is one
            applier = getattr(self, getSetterName(param, 'apply'), None)
            if applier is not None:
                self._curParamStack.append(param)
                applier()
                self._curParamStack.pop()
        self._priorValuesStack.pop()
        if hasattr(self, 'handleParamChange'):
            self.handleParamChange(tuple(self._paramsSet.keys()))
        del self._paramsSet

    def paramsLocked(self):
        return self._paramLockRefCount > 0

    def getPriorValue(self):
        # call this within an apply function to find out what the prior value
        # of the param was
        return self._priorValuesStack[-1][self._curParamStack[-1]]

    def __repr__(self):
        argStr = ''
        for param in self.ParamSet.getParams():
            try:
                value = getSetter(self, param, 'get')()
            except BaseException:
                value = '<unknown>'
            argStr += '%s=%s,' % (param, repr(value))
        return '%s(%s)' % (self.__class__.__name__, argStr)


if __debug__ and __name__ == '__main__':
    class ParamObjTest(ParamObj):
        class ParamSet(ParamObj.ParamSet):
            Params = {
                'num': 0,
            }

        def applyNum(self):
            self.priorValue = self.getPriorValue()
    pto = ParamObjTest()
    assert pto.getNum() == 0
    pto.setNum(1)
    assert pto.priorValue == 0
    assert pto.getNum() == 1
    pto.lockParams()
    pto.setNum(2)
    # make sure applyNum is not called until we call unlockParams
    assert pto.priorValue == 0
    assert pto.getNum() == 2
    pto.unlockParams()
    assert pto.priorValue == 1
    assert pto.getNum() == 2
builtins.pdir = pdir
builtins.isClient = isClient
builtins.lerp = lerp
builtins.triglerp = triglerp
builtins.choice = choice
builtins.cmp = cmp
builtins.Enum = Enum