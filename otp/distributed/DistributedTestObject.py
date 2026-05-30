from direct.distributed import DistributedObject


class DistributedTestObject(DistributedObject.DistributedObject):

    def setRequiredField(self, r) -> None:
        self.requiredField = r

    def setB(self, B) -> None:
        self.B = B

    def setBA(self, BA) -> None:
        self.BA = BA

    def setBO(self, BO) -> None:
        self.BO = BO

    def setBR(self, BR) -> None:
        self.BR = BR

    def setBRA(self, BRA) -> None:
        self.BRA = BRA

    def setBRO(self, BRO) -> None:
        self.BRO = BRO

    def setBROA(self, BROA) -> None:
        self.BROA = BROA

    def gotNonReqThatWasntSet(self) -> bool:
        for field in ('B', 'BA', 'BO', 'BR', 'BRA', 'BRO', 'BROA'):
            if hasattr(self, field):
                return True

        return False
