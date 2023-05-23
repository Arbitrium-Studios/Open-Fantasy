import argparse
import os

# These are arguments that *can* be parsed by running python multify.py -- (args)
parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='bin',
                    help='The directory in which to store the build files.')
parser.add_argument('--resources-dir', default='../resources',
                    help='The directory of the Toontown resources.')
args = parser.parse_args()

print ('Building Phase Files...')
dest = os.path.join(args.build_dir)
if not os.path.exists(dest):
    os.mkdir(dest)
dest = os.path.realpath(dest)
os.chdir(args.resources_dir)
for phase in os.listdir('.'):
    if not phase.startswith('phase_'):
        continue
    if not os.path.isdir(phase):
        continue
    filename = phase + '.mf'
    print('Writing ', filename)
    filepath = os.path.join(dest, filename)
    os.system('C:/Open-Panda/bin/multify -c -f "%s" "%s"' % (filepath, phase))
print ('Done Building Phase Files')