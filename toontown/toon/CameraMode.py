from panda3d.core import *
from direct.showbase import DirectObject
from otp.otpbase.PythonUtil import Enum
from direct.fsm.FSM import FSM
from otp.otpbase import OTPGlobals


class CameraMode(FSM):

    def __init__(self):
        FSM.__init__(self, 'CameraMode')
        self.mouseControl = False
        self.mouseDelta = (0, 0)
        self.lastMousePos = (0, 0)
        self.origMousePos = (0, 0)
        self.request('Off')
        self.__inputEnabled = False
        self.__cursorLock = 0.0
        

    def destroy(self):
        self.ignoreAll()

    def getName(self):
        pass

    def start(self):
        if not self.isActive():
            self.request('Active')

    def stop(self):
        if self.isActive():
            self.request('Off')

    def isActive(self):
        return self.state == 'Active'

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterActive(self):
        self.enableInput()

    def exitActive(self):
        self.disableInput()

    def enableInput(self):
        self.__inputEnabled = True
        self.accept('mouse3', self.enableMouseControl)
        self.accept('mouse3-up', self.disableMouseControl)
        if base.mouseWatcherNode.isButtonDown(MouseButton.three()):
            self.enableMouseControl()

    def disableInput(self):
        self.__inputEnabled = False
        self.disableMouseControl()
        self.ignore('mouse3')
        self.ignore('mouse3-up')

    def isInputEnabled(self):
        return self.__inputEnabled

    def enableMouseControl(self):
        if hasattr(base, 'oobeMode') and base.oobeMode:
            return

        self.mouseControl = True
        self.__cursorLock = 0.0
        mouseData = base.win.getPointer(0)
        self.origMousePos = (mouseData.getX(), mouseData.getY())
        self._hideCursor()

        base.win.movePointer(0, base.win.getXSize() // 2, base.win.getYSize() // 2)
        self.lastMousePos = (base.win.getXSize() / 2, base.win.getYSize() / 2)
        if self.getCurrentOrNextState() == 'Active':
            self._startMouseControlTasks()

    def _hideCursor(self):
        # From pirates guimanager
        wp = WindowProperties()
        wp.setCursorHidden(1)
        base.win.requestProperties(wp)
        base.graphicsEngine.openWindows()

    def disableMouseControl(self):
        if hasattr(base, 'oobeMode') and base.oobeMode:
            return

        if self.mouseControl:
            self.mouseControl = False
            self._stopMouseControlTasks()
            self._showCursor()

            base.win.movePointer(0, int(self.origMousePos[0]), int(self.origMousePos[1]))

    def _showCursor(self):
        # From pirates guimanager
        wp = WindowProperties()
        wp.setCursorHidden(0)
        base.win.requestProperties(wp)
        base.graphicsEngine.openWindows()

    def _startMouseControlTasks(self):
        if self.mouseControl:
            properties = WindowProperties()
            properties.setMouseMode(properties.MRelative)
            base.win.requestProperties(properties)
            self._startMouseReadTask()
            self._startMouseUpdateTask()

    def _stopMouseControlTasks(self):
        properties = WindowProperties()
        properties.setMouseMode(properties.MAbsolute)
        base.win.requestProperties(properties)
        self._stopMouseReadTask()
        self._stopMouseUpdateTask()

    def _startMouseReadTask(self):
        taskMgr.add(self._mouseReadTask, '%s-MouseRead' % self._getTopNodeName(), priority=-29)

    def _mouseReadTask(self, task):
        winSize = (base.win.getXSize(), base.win.getYSize())
        if hasattr(base, 'oobeMode') and base.oobeMode or not base.mouseWatcherNode.hasMouse():
            self.mouseDelta = (0, 0)
        elif self.__cursorLock <= 0.05:
            self.mouseDelta = (0, 0)
            self.__cursorLock = task.time
        else:
            mouseData = base.win.getPointer(0)
            self.mouseDelta = (mouseData.getX() - self.lastMousePos[0], mouseData.getY() - self.lastMousePos[1])
        base.win.movePointer(0, winSize[0] // 2, winSize[1] // 2)
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        return task.cont

    def _stopMouseReadTask(self):
        taskMgr.remove('%s-MouseRead' % self._getTopNodeName())

    def _startMouseUpdateTask(self):
        taskMgr.add(self._avatarFacingTask, '%s-AvatarFacing' % self._getTopNodeName(), priority=23)
        taskMgr.add(self._mouseUpdateTask, '%s-MouseUpdate' % self._getTopNodeName(), priority=40)

    def _avatarFacingTask(self, task):
        return task.cont

    def _mouseUpdateTask(self, task):
        return task.cont

    def _stopMouseUpdateTask(self):
        taskMgr.remove('%s-MouseUpdate' % self._getTopNodeName())
        taskMgr.remove('%s-AvatarFacing' % self._getTopNodeName())

    def avFaceCamera(self):
        pass

    def _getTopNodeName(self):
        return 'RandomCam'
