@echo off
cd ..
title Toontown Fantasy Uberdog

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Define some constants for our UberDOG server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENTLOGGER_IP=127.0.0.1:7198
set BASE_CHANNEL=1000000

:uberdog

%PPYTHON_PATH% ^
	-m toontown.uberdog.UDStart ^
	--base-channel %BASE_CHANNEL% ^
	--max-channels %MAX_CHANNELS% ^
	--stateserver %STATESERVER% ^
	--messagedirector-ip %ASTRON_IP% ^
	--eventlogger-ip %EVENTLOGGER_IP%

pause
goto uberdog


