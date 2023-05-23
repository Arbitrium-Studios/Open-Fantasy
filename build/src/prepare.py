import argparse
import hashlib
import os
import platform
import shutil
import subprocess

from pandac.PandaModules import *

parser = argparse.ArgumentParser()

#Argument for the location of the source code.              
parser.add_argument('--src-dir', default='..',
                    help='The directory of the source code.')

#Argument for Python Modules to be Included
parser.add_argument('modules', nargs='*', default=['otp', 'toontown', 'dependencies'],
                    help='The modules to be included in the build.')

#Argument for the build directory. This is not the final directory this is where the code is temporarely stored.
parser.add_argument('--build-dir', default='build',
                    help='The directory in which to store the build files.')

#Argument for the version number of the game. REVISION is replaced with the git hash
parser.add_argument('--server-ver', default='tt-REVISION',
                    help='The server version of this build.\n'
                    'REVISION tokens will be replaced with the current Git revision string.')

#Argument for the location of the Panda3D prc's.
parser.add_argument('--configprc-dir', default='etc',
                    help='The directory of the Panda3D Config.prc.')
parser.add_argument('--general-prc', default='Configrc.prc',
                    help='The directory of the Panda3D Config.prc.')
parser.add_argument('--qa-prc', default='Release.prc',
                    help='The directory of the Panda3D Config.prc.')

#Argument for the location of the Astron dclass.
parser.add_argument('--dclass-dir', default='etc',
                    help='The directory of the Astron dclass.')

args = parser.parse_args()

print ('Preparing to build the Cient... Please wait')

# Create a clean build directory for us to store our build material:
if not os.path.exists(args.build_dir):
    os.mkdir(args.build_dir)
print ('Build directory = {0}'.format(args.build_dir))

# This next part is only required if the invoker wants to include the Git
# revision string in their server version:
revision = ''
if 'REVISION' in args.server_ver:
    if platform.system() == 'Windows':
        # If we don't have Git on our path, let's attempt to add it:
        paths = (
            '{0}\\Git\\bin'.format(os.environ['ProgramFiles']),
            '{0}\\Git\\cmd'.format(os.environ['ProgramFiles'])
        )
        for path in paths:
            if path not in os.environ['PATH']:
                os.environ['PATH'] += ';' + path
    # Now, let's get that revision string:
    revision = subprocess.Popen(
        ['git', 'rev-parse', 'HEAD'],
        stdout=subprocess.PIPE,
        cwd=args.src_dir).stdout.read().strip()[:7].decode('utf-8')

# Replace any REVISION tokens in the server version:
serverVersion = args.server_ver.replace('REVISION', revision)
print ('serverVersion = {0}'.format(serverVersion))

includes = ('NonRepeatableRandomSourceUD.py', 'NonRepeatableRandomSourceAI.py', 'DistributedPhysicsWorldAI')
print ("Including", includes)

# This is a list of explicitly excluded files:
excludes = ('ServiceStart.py', 'ToontownUberRepository', 'ToontownAIRepository')
print ('Excluding', excludes)

print ("Removing _debug_ statements from build")
def minify(f):
    """
    Returns the "minified" file data with removed __debug__ code blocks.
    """

    data = ''

    debugBlock = False  # Marks when we're in a __debug__ code block.
    elseBlock = False  # Marks when we're in an else code block.

    # The number of spaces in which the __debug__ condition is indented:
    indentLevel = 0
    for line in f:
        thisIndentLevel = len(line) - len(line.lstrip())
        if ('if __debug__:' not in line) and (not debugBlock):
            data += line
            continue
        elif 'if __debug__:' in line:
            debugBlock = True
            indentLevel = thisIndentLevel
            continue
        if thisIndentLevel <= indentLevel:
            if 'else' in line:
                elseBlock = True
                continue
            if 'elif' in line:
                line = line[:thisIndentLevel] + line[thisIndentLevel+2:]
            data += line
            debugBlock = False
            elseBlock = False
            indentLevel = 0
            continue
        if elseBlock:
            data += line[4:]

    return data

for module in args.modules:
    print ('Writing modules... And not copying excluded files'), module
    for root, folders, files in os.walk(os.path.join(args.src_dir, module)):
        outputDir = root.replace(args.src_dir, args.build_dir)
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        for filename in files:
            if filename not in includes:
                if not filename.endswith('.py'):
                    continue
                if filename.endswith('UD.py'):
                    continue
                if filename.endswith('AI.py'):
                    continue
                if filename in excludes:
                    continue
            with open(os.path.join(root, filename), 'r') as f:
                data = minify(f)
            with open(os.path.join(outputDir, filename), 'w') as f:
                f.write(data)

# Let's write gamedata.py now. gamedata is a compile-time generated
# collection of data that will be used by the game at runtime. It contains the
# PRC file data, (stripped) DC file, and time zone info.

# First, we need the PRC file data:
print ('Writing public_client.prc into gamedata')
configData = []
with open(os.path.join(args.src_dir, args.configprc_dir, args.general_prc)) as f:
    data = f.read()
    configData.append(data)
with open(os.path.join(args.src_dir, args.configprc_dir, args.qa_prc)) as f:
    data = f.read()
    configData.append(data.replace('SERVER_VERSION', serverVersion))
print ('Using config files: {0}, {1}'.format(args.general_prc, args.qa_prc))

# Next, we need the (stripped) DC file:
dcFile = DCFile()
filepath = os.path.join(args.src_dir, args.dclass_dir)
for filename in os.listdir(filepath):
    if filename.endswith('.dc'):
        dcFile.read(Filename.fromOsSpecific(os.path.join(filepath, filename)))
dcStream = StringStream()
dcFile.write(dcStream, True)
dcData = dcStream.getData()

# Finally, write our data to gamedata.py:
print ('Writing gamedata.py...')
gameData = '''\
CONFIG = %r
DC = %r
'''
with open(os.path.join(args.build_dir, 'gamedata.py'), 'w') as f:
    f.write(gameData % (configData, dcData))

print ('Done')