import builtins, os

class game:
    name = 'uberDog'
    process = 'server'

builtins.game = game

from panda3d.core import *

loadPrcFile('etc/Configrc.prc')

localPrc = 'etc/local.prc'

if os.path.exists(localPrc):
    loadPrcFile(localPrc)

from otp.uberdog.UberDogGlobal import *
from toontown.uberdog.ToontownUDRepository import ToontownUDRepository
import argparse

parser = argparse.ArgumentParser(description="Open Toontown - UberDOG Server")
parser.add_argument(
    '--base-channel',
    help='The base channel that the server will use.')
parser.add_argument(
    '--max-channels',
    help='The number of channels that the server will be able to use.')
parser.add_argument(
    '--stateserver',
    help='The control channel of this UberDOG\'s designated State Server.')
parser.add_argument('--messagedirector-ip',
                    help='The IP address of the Message Director that this UberDOG will connect to.')
parser.add_argument(
    '--eventlogger-ip',
    help='The IP address of the Astron Event Logger that this UberDOG will log to.')
parser.add_argument('config', nargs='*', default=['etc/Configrc.prc'],
                    help='PRC file(s) that will be loaded on this UberDOG instance.')
args = parser.parse_args()

localConfig = ''
if args.base_channel:
    localConfig += 'air-base-channel %s\n' % args.base_channel
if args.max_channels:
    localConfig += 'air-channel-allocation %s\n' % args.max_channels
if args.stateserver:
    localConfig += 'air-stateserver %s\n' % args.stateserver
if args.messagedirector_ip:
    localConfig += 'air-connect %s\n' % args.messagedirector_ip
if args.eventlogger_ip:
    localConfig += 'eventlog-host %s\n' % args.eventlogger_ip

loadPrcFileData('UberDOG Args Config', localConfig)


uber.air = ToontownUDRepository(config.GetInt('air-base-channel', 1000000), config.GetInt('air-stateserver', 4002))

host = config.GetString('air-connect', '127.0.0.1:7199')
port = 7199
if ':' in host:
    host, port = host.split(':', 1)
    port = int(port)

simbase.air.connect(host, port)

try:
    run()
except SystemExit:
    raise
except Exception:
    from otp.otpbase import PythonUtil
    print(PythonUtil.describeException())
    raise
