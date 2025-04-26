@echo off
@REM cd ..
title Toontown Fantasy UberDOG

cd ../
set ROOT_PATH=%CD%
echo Root path is: %ROOT_PATH%
echo.

cd %ROOT_PATH%
echo Directory path is: %ROOT_PATH%

set DEPENDENCIES_PATH=dependencies
echo Dependencies path is: %DEPENDENCIES_PATH%
set PANDA3D_PATH=panda3d
set PYTHON_PATH=%ROOT_PATH%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\ppython.exe
echo PYTHON_PATH is set as: %PYTHON_PATH%

rem Define some constants for our UberDOG server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENTLOGGER_IP=127.0.0.1:7198
set BASE_CHANNEL=1000000

:main

%PYTHON_PATH% ^
	-m toontown.uberdog.UDStart ^
	--base-channel %BASE_CHANNEL% ^
	--max-channels %MAX_CHANNELS% ^
	--stateserver %STATESERVER% ^
	--messagedirector-ip %ASTRON_IP% ^
	--eventlogger-ip %EVENTLOGGER_IP%
PAUSE
goto main