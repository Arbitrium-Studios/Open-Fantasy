"""LoginTTAccount: Login using an Account Manager server"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from . import LoginTTAccount


class LoginWebPlayTokenAccount(LoginTTAccount.LoginTTAccount):

    # Create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("LoginWebPlayTokenAccount")

    def supportsRelogin(self):
        """
        Since you login to through the web page, it does not really make
        sense to relogin in the game.
        """
        return 0

    def createAccount(self, loginName, password, data):
        pass

    def authorize(self, loginName, password):
        self.playToken=password
        self.playTokenIsEncrypted=1
        self.freeTimeExpires=-1
        self.cr.freeTimeExpiresAt=self.freeTimeExpires
    
    def createBilling(self, loginName, password, data):
        pass

    def setParentPassword(self, loginName, password, parentPassword):
        pass

    def supportsParentPassword(self):
        return 1

    # from TTAccount: def authenticateParentPassword(self, loginName, password, parentPassword):
    
    # from TTAccount: def enableSecretFriends(self, loginName, password, parentPassword, enable=1):
    
    def changePassword(self, loginName, password, newPassword):
        pass

    def requestPwdReminder(self, email=None, acctName=None):
        pass
    
    def cancelAccount(self, loginName, password):
        pass

    def getAccountData(self, loginName, password):
        pass

    def getErrorCode(self):
        if "response" not in self:
            return 0
        return self.response.getInt('errorCode', 0)

    def needToSetParentPassword(self):
        return 0
