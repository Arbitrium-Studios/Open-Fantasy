from direct.stdpy import threading

class DNABulkLoader:
    def __init__(self, storage, files):
        self.dnaStorage = storage
        self.dnaFiles = files

    def loadDNAFiles(self):
        for file in self.dnaFiles:
            print('Reading DNA file...', file)
            loadDNABulk(self.dnaStorage, file)
        del self.dnaStorage
        del self.dnaFiles

def loadDNABulk(dnaStorage, file):
    dnaLoader = DNALoader()
    file = '/' + file
    dnaLoader.loadDNAFile(dnaStorage, file)

def loadDNAFile(dnaStorage, file):
    print('Reading DNA file...', file)
    dnaLoader = DNALoader()
    file = '/' + file
    node = dnaLoader.loadDNAFile(dnaStorage, file)
    if node.node().getNumChildren() > 0:
        return node.node()

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader()
    file = '/' + file
    data = dnaLoader.loadDNAFileAI(dnaStorage, file)
    return data

def setupDoor(a, b, c, d, e, f):
    try:
        e = int(str(e).split('_')[0])
    except:
        print('setupDoor: error parsing', e)
        e = 9999

    DNADoor.setupDoor(a, b, c, d, e, f)
