from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import MintProduct


class MintProductPallet(MintProduct.MintProduct):
    Models = {CashbotMintIntA: 'user/resources/default/phase_10/models/cashbotHQ/DoubleCoinStack.bam',
              CashbotMintIntB: 'user/resources/default/phase_10/models/cogHQ/DoubleMoneyStack.bam',
              CashbotMintIntC: 'user/resources/default/phase_10/models/cashbotHQ/DoubleGoldStack.bam'}
    Scales = {CashbotMintIntA: 1.0,
              CashbotMintIntB: 1.0,
              CashbotMintIntC: 1.0}
