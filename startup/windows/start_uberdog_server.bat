@echo off
set "projectName=PLAYER ZER0 STUDIO's Toontown Fantasy"
title %projectName%'s UberDOG

:root
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting %projectName%
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
@REM set RootPath=%CD%
set "MainDirectory="%CD%""

set PREVIOUS_DIR="..\"

cd /d %PREVIOUS_DIR%%PREVIOUS_DIR%
echo Current directory is: %CD%
echo.

@REM pause

@REM set "MainDirectory="%CD%""

echo Current Directory is %CD%
echo.

set "RootPath=%CD%"

set "RootPathAlt=%CD%"
echo Root Directory is "%RootPath%"
echo.

set "PYTHON_PATH_FILE=%RootPath%\PYTHON_PATH"

goto :ppython

echo.

:ppython
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Setting Python Path
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

REM Read the contents of PYTHON_PATH into %PYTHON_PATH%:
if exist "%PYTHON_PATH_FILE%" (
    echo The "PYTHON_PATH_FILE" exists at "%PYTHON_PATH_FILE%"
    echo.
    set /p CUSTOM_PYTHON_PATH=<PYTHON_PATH
) else (
    echo Python Path File does not exist at %PYTHON_PATH_FILE%
    echo.
    goto :ending
)

echo Python Path is set to "%CUSTOM_PYTHON_PATH%"
echo.

if not defined PYTHON_PATH (
    set CUSTOM_PYTHON_PATH=%RootPath%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\ppython.exe
) else (
    set CUSTOM_PYTHON_PATH=%PYTHON_PATH%
)

echo PYTHON_PATH is set as: %CUSTOM_PYTHON_PATH%
echo.

@REM cd ../
@REM set ROOT_PATH=%CD%
@REM echo Root path is: %ROOT_PATH%
@REM echo.

@REM cd %ROOT_PATH%
@REM echo Directory path is: %ROOT_PATH%

set "DEPENDENCIES_PATH=dependencies"
echo Dependencies path is: %DEPENDENCIES_PATH%
set "PANDA3D_PATH=panda3d"


set PREVIOUS_DIR="..\"

echo Current directory is: %CD%
echo.

@REM cd /d %PREVIOUS_DIR%%PREVIOUS_DIR%
@REM echo Current directory is: %CD%
@REM echo.

set "PackageDependencies=%CD%\dependencies\packages"
set "getPipPackageDependencies=%CD%\dependencies\packages\%GET_PIP%"

set "PYTHON_PATH_FILE=%CD%\PYTHON_PATH"
set "PPYTHON_PATH_FILE=%CD%\PPYTHON_PATH"

set "DEPENDENCIES_DIR=dependencies"
set "PANDA3D_DIR=panda3d"
set "Panda3DPath=C:\Open-Panda"

set "DEPENDENCIES_PATH=%CD%\%DEPENDENCIES_DIR%"
set "PANDA3D_PATH=%CD%\%DEPENDENCIES_DIR%\%PANDA3D_DIR%"

set "MainDirectory="%CD%""

echo Current Directory is %CD%
echo.

set "RootPath=%CD%"

set "RootPathAlt=%CD%"
echo Root Directory is "%RootPath%"
echo.

set "PYTHON_PATH_FILE=%RootPath%\PYTHON_PATH"

goto :ppython

echo.

:ppython
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Setting Python Path
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

REM Read the contents of PYTHON_PATH into %PYTHON_PATH%:
if exist "%PYTHON_PATH_FILE%" (
    echo The "PYTHON_PATH_FILE" exists at "%PYTHON_PATH_FILE%"
    echo.
    set /p CUSTOM_PYTHON_PATH=<PYTHON_PATH
) else (
    echo Python Path File does not exist at %PYTHON_PATH_FILE%
    echo.
    goto :ending
)

if not defined PYTHON_PATH (
    set CUSTOM_PYTHON_PATH=%RootPath%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\ppython.exe
) else (
    set CUSTOM_PYTHON_PATH=%PYTHON_PATH%
)

echo The "CUSTOM_PYTHON_PATH" variable is set as: %CUSTOM_PYTHON_PATH%
echo.

@REM set PYTHON_PATH=%ROOT_PATH%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\ppython.exe
@REM echo PYTHON_PATH is set as: %PYTHON_PATH%
@REM echo.

:start_uberdog
cls

rem Define some constants for our UberDOG server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENTLOGGER_IP=127.0.0.1:7198
set BASE_CHANNEL=1000000

:main

%CUSTOM_PYTHON_PATH% ^
	-m toontown.uberdog.UDStart ^
	--base-channel %BASE_CHANNEL% ^
	--max-channels %MAX_CHANNELS% ^
	--stateserver %STATESERVER% ^
	--messagedirector-ip %ASTRON_IP% ^
	--eventlogger-ip %EVENTLOGGER_IP%
PAUSE
@REM goto main
goto :start_uberdog