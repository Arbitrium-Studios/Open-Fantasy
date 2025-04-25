@echo off
title PLAYER ZER0 STUDIO's Toontown Fantasy Launcher

:root
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Setting Root Directory
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set ROOT_PATH=%CD%
set PREVIOUS_DIR="..\"
echo Root path is: %ROOT_PATH%

goto :set_dependencies

:set_dependencies
cd %ROOT_PATH%
echo Directory path is: %ROOT_PATH%
set DEPENDENCIES_PATH=dependencies
echo Dependencies folder path is: %CD%\%DEPENDENCIES_PATH%
if exist %DEPENDENCIES_PATH% (
    echo Dependencies folder already exists.
    @REM pause
    goto :set_panda3d
) else (
    echo Dependencies folder does not exist, creating it now.
    mkdir %DEPENDENCIES_PATH%
    pause
    goto :set_dependencies
)

:panda3d

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting PLAYER ZER0 STUDIO's Toontown Fantasy's compiled Panda3D
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

echo Root path is: %ROOT_PATH%
@REM goto :set_panda3d

:set_panda3d
cd %ROOT_PATH%/%DEPENDENCIES_PATH%
echo Directory path is: %CD%
set PANDA3D_PATH=panda3d
echo Panda3d folder path will be: %CD%\%PANDA3D_PATH%
@REM pause
if exist %PANDA3D_PATH% (
    echo Cool! The Panda3D folder exists.
    call git pull https://github.com/Arbitrium-Studios/panda3d.git
    pause
    goto :ppython
) else (
    echo Panda3d folder does not exist.
    goto :panda3D_version
)

:panda3D_version

echo Choose what Panda3D version you want to use!
echo.
echo #1 - Pre-Compiled
@REM echo.
@REM echo #2 - Local Panda3D Version
echo.

@REM :panda3d_version

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    echo Pre-Compiled Panda3D version has been selected.
    echo.
    echo Cloning the pre-compiled Panda3D repository.
    call git clone https://github.com/Arbitrium-Studios/panda3d.git
    echo Directory path is: %CD%
    echo Panda3D has been retrieved.
    pause
    goto :set_panda3d
@REM ) else if %INPUT%==2 (
@REM     echo Local Panda3D version selected.
@REM     set /P PANDA3D_PATH="Please Enter the path to your local Panda3D folder: "
@REM     echo PANDA3D_PATH is now set to: %PANDA3D_PATH%
@REM     pause
@REM     goto :set_panda3d
) else (
    echo Invalid selection, please try again.
    goto :panda3d_version
)

echo.

:ppython
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Setting Python Path
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

cd %PREVIOUS_DIR%
echo Current directory is: %CD%

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH
echo Python path is: %PPYTHON_PATH%
set PIP_PATH=/panda3d/python/Scripts/pip.exe
@REM pause
goto :requirements

:requirements
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting Requirements
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

call %PPYTHON_PATH% %DEPENDENCIES_PATH%/%PIP_PATH% install -r requirements.txt
call %PPYTHON_PATH% -m %DEPENDENCIES_PATH%/%PIP_PATH% install --upgrade pip

goto :submodules

:submodules
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting Submodules
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
%PPYTHON_PATH% %DEPENDENCIES_PATH%/initialize.py
@REM call git submodule update --init --recursive
@REM pause
goto :updates

:updates


echo Checking for updates from the development branch.
call git fetch origin development && git status --porcelain
call git diff --quiet HEAD..origin/development
if errorlevel 1 (
    echo Updates found, pulling changes...
    call git pull origin development
    pause
    @REM :submodules
    goto :localhost
) else (
    echo No updates found.
    @REM pause
    goto :localhost
)

echo All done!
@REM pause
goto :localhost

:localhost
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting Localhost!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
cd "scripts"
echo Launching Astron...
START start_astron_server.bat
echo Launching the Uberdog Server...
START start_uberdog_server.bat
echo Launching the AI Server...
START start_toon_valley_ai_server.bat
cd ..
SET TT_GAMESERVER=127.0.0.1
timeout 3
goto game

:game
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Your Username is your username and does get stored in your source code so beware!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set TT_Username=%username%
echo.

SET LOGIN_TOKEN=%TT_Username%
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo The Tooniverse awaits you, %TT_Username%!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
:startgame
title PLAYER ZER0 STUDIO's Toontown Fantasy
%PPYTHON_PATH% -m toontown.launcher.QuickStartLauncher
PAUSE
goto startgame