from ByteArray import ByteArray
import os, zlib, sys

class Unpacker:
    def __init__(self):
        self.magicCode = 1146110283

        self.unpackDir = 'unpacked/'

        if not os.path.exists(self.unpackDir):
            os.mkdir(self.unpackDir)

    def open(self, filename):
        source = open(filename, 'rb').read()

        data = zlib.decompress(source)

        reader = ByteArray(data)

        magicCode = reader.readUnsignedInt()

        if magicCode != self.magicCode:
            raise Exception('Magic code invalid!')

        numFiles = reader.readUnsignedShort()

        lengths = []

        for _ in range(numFiles):
            length = reader.readUnsignedInt()

            lengths.append(length)

        names = []

        for _ in range(numFiles):
            lengthBytes = reader.readUnsignedShort()

            name = reader.readMultiByte(lengthBytes)

            names.append(name)

        for i in range(numFiles):
            data = reader.readBytes(lengths[x])

            with open(self.unpackDir + names[x], 'wb') as file:
                print('Writing {0} to disk!'.format(names[x]))
                file.write(data)

unpacker = Unpacker()
unpacker.open(sys.argv[1])