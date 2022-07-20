from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import MintProduct


class MintShelf(MintProduct.MintProduct):
    Models = {CashbotMintIntA: '../../user/default/resources/default/phase_10/models/cashbotHQ/shelf_A1MoneyBags',
              CashbotMintIntB: '../../user/default/resources/default/phase_10/models/cashbotHQ/shelf_A1Money',
              CashbotMintIntC: '../../user/default/resources/default/phase_10/models/cashbotHQ/shelf_A1Gold'}
    Scales = {CashbotMintIntA: 1.0,
              CashbotMintIntB: 1.0,
              CashbotMintIntC: 1.0}
