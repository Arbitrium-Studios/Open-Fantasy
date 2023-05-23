import argparse
import os
import platform
import sys
parser = argparse.ArgumentParser()

#Argument for the Build Directory prepare made.
parser.add_argument('--build-dir', default='build',
                    help='The directory of which the build was prepared.')

#Argument for the Directory to Output the distribution to
parser.add_argument('--output-dir', default='bin',
                    help='The directory of which the build was prepared.')

#Argument for the Executable of the compiled code
parser.add_argument('--output', default='ToontownFantasy',
                    help='The name of the built file.')

#Argument for the Main Python Module
parser.add_argument('--main-module', default='toontown/toonbase/StartCompiledGame.py',
                    help='The path to the instantiation module.')

#Argument for Python Modules to be Included
parser.add_argument('modules', nargs='*', default=['otp', 'toontown', 'dependencies'],
                    help='The Toontown modules to be included in the build.')

#Argument for the Panda3D Directory
#If user is on Windows this is the default directory
if platform.system() == 'Windows':               
    parser.add_argument('--panda3d-dir', default='C:/Open-Panda',
                        help='The path to the Panda3D build to use for this distribution.')
#If user is on macOS this is the default directory                        
if platform.system() == 'Darwin':
    parser.add_argument('--panda3d-dir', default='/Library/Developer/Panda3D',
                        help='The path to the Panda3D build to use for this distribution.')
#If user is on Linux this is the default directory                        
if platform.system() == 'Linux':
    parser.add_argument('--panda3d-dir', default='/usr/lib/panda3d',
                        help='The path to the Panda3D build to use for this distribution.')

#Argument for the Python Directory
#If user is on Windows this is the default directory
if platform.system() == 'Windows':               
    parser.add_argument('--python-binary', default='python/python.exe',
                        help='The path to the Python Executable.')
#If user is on macOS this is the default directory                        
if platform.system() == 'Darwin':
    parser.add_argument('--python-binary', default='python3',
                        help='The path to the Python Executable.')
#If user is on Linux this is the default directory                        
if platform.system() == 'Linux':
    parser.add_argument('--python-binary', default='python',                     
        help='The path to the Python Executable.')

# If user is on macOS, this is a path for the Python framework.
if platform.system() == 'Darwin':
    parser.add_argument('--python-framework-dir', help='The path to the Python framework.')

#Lets Parse all the Arguments
args = parser.parse_args()

#Lets now do a hack to get the output file name
outputFile = "../" + args.output_dir + "/" + args.output

print ('Building the client...')

#Lets make the Output Directory if it does not currently exist
if not os.path.isdir(args.output_dir):
    os.mkdir(args.output_dir)

#Lets now join the Output Directory
os.chdir(args.build_dir)

#Lets mow compile the distribution
if platform.system() == 'Windows':
    cmd = os.path.join(args.panda3d_dir, args.python_binary)
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    cmd = args.python_binary
cmd += ' -m direct.dist.pfreeze'
cmd += ' -x panda3d'
args.modules.extend(['pandac', 'direct'])
for module in args.modules:
    cmd += ' -i {0}.*.*'.format(module)
cmd += ' -i {0}.*'.format('encodings')
cmd += ' -i {0}'.format('base64')
cmd += ' -i {0}'.format('site')
cmd += ' -i {0}'.format('_strptime')
if platform.system() == 'Darwin' and args.python_framework_dir:
    cmd += ' -L {0}'.format(args.python_framework_dir)
cmd += ' -o {0}'.format(outputFile)
cmd += ' {0}'.format(args.main_module)
os.system(cmd)