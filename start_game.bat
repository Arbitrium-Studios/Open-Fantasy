@echo off
title PLAYER ZER0 STUDIO's Toontown Fantasy Launcher

:root
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Setting Root Directory
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set ROOT_PATH=%CD%
set PREVIOUS_DIR="..\"
echo Root path is: %ROOT_PATH%

set SCRIPTS_PATH=%ROOT_PATH%\scripts
set SCRIPTS_DIR=scripts
echo Scripts Directory path is: %SCRIPTS_DIR%
echo.

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

echo.
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting PLAYER ZER0 STUDIO's Toontown Fantasy's compiled Panda3D
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
echo Directory path is: %ROOT_PATH%
echo.
goto :set_panda3d

:set_panda3d
cd %CD%
cd %ROOT_PATH%\%DEPENDENCIES_PATH%
echo Directory path is: %CD%
set PANDA3D_PATH=panda3d
echo Panda3d folder path will be: %CD%\%PANDA3D_PATH%
echo.
echo Checking if the Panda3D folder exists.
if exist %PANDA3D_PATH% (
    echo Cool! The Panda3D folder exists at %PANDA3D_PATH%
    echo.
    echo Entering the Panda3D folder.
    cd %PANDA3D_PATH%
    @REM set CURRENT_DIR=%PANDA3D_PATH%
    echo CURRENT_DIR is now set to: %CD%
    @REM echo Current directory path in set_panda3d is: %CURRENT_DIR%
    @REM @REM echo Cool! The Panda3D folder exists at %PANDA3D_PATH%
    
    echo Cool! The Panda3D folder exists at %PANDA3D_PATH%
    echo.
    @REM echo Entering the Panda3D folder.
    @REM cd %PANDA3D_PATH%
    @REM set CURRENT_DIR=%PANDA3D_PATH%
    echo CURRENT_DIR is now set to: %CD%
    @REM echo Current directory path in set_panda3d is: %CURRENT_DIR%
    echo Checking for updates to the Panda3D repository.
    echo.
    call git fetch origin development && git status --porcelain
    call git pull https://github.com/Arbitrium-Studios/panda3d.git main --allow-unrelated-histories
    @REM pause rem for debugging purposes
    goto :ppython
) else (
    echo The Panda3D folder does not exist, creating it now.
    @REM mkdir %PANDA3D_PATH%
    echo Created the Panda3D folder at %ROOT_PATH%\%PANDA3D_PATH%
    echo CURRENT_DIR at Panda3D Else is now set to: %CD%
    @REM pause rem for debugging purposes
    goto :panda3d_version
)

echo Choose what Panda3D version you want to use!
echo.
echo #1 - Pre-Compiled
@REM echo.
@REM echo #2 - Local Panda3D Version
echo.

:panda3d_version

set INPUT=-1
set \P INPUT=Selection: 

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
@REM     set \P PANDA3D_PATH="Please Enter the path to your local Panda3D folder: "
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

cd %ROOT_PATH%
echo Current directory at PYTHON_PATH is: %CD%
echo.
echo Current directory at requirements is: %CD%
echo ROOT_PATH is: %CD%
echo Dependencies path is: %DEPENDENCIES_PATH%
rem Read the contents of PYTHON_PATH into %PYTHON_PATH%:
@REM set %DEPENDENCIES_PATH%/variables
@REM set \P PYTHON_PATH=<PYTHON_PATH
@REM echo PPYTHON PATH is set as: %PYTHON_PATH%
set PYTHON_PATH=%ROOT_PATH%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\ppython.exe
echo PYTHON_PATH is set as: %PYTHON_PATH%
set PIP_PATH=%ROOT_PATH%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\Scripts\pip.exe
echo PIP_PATH is: %PIP_PATH%

@REM pause
goto :requirements

:requirements
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting Requirements
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


@REM pause
@REM set PYTHON_PATH = "dependencies\panda3d\python\ppython.exe"

cd %ROOT_PATH%
echo Current directory at Requirements is: %CD%

set GET_PIP_PATH = dependencies\get-pip.py

call %PYTHON_PATH% "%GET_PIP_PATH%" --no-warn-script-location

@REM "%PYTHON_PATH%" %GET_PIP_PATH%
@REM call %PYTHON_PATH% -m %ROOT_PATH%\%DEPENDENCIES_PATH%\%PIP_PATH% install --upgrade pip
@REM call %PYTHON_PATH% %ROOT_PATH%\%DEPENDENCIES_PATH%\%PIP_PATH% install -r %ROOT_PATH%\requirements.txt

goto :submodules

:submodules
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting Submodules
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
%PYTHON_PATH% %DEPENDENCIES_PATH%/initialize.py
@REM call git submodule update --init --recursive
@REM pause

@REM echo Checking for updates from the development branch.
@REM call git fetch origin development && git status --porcelain
@REM call git diff --quiet HEAD..origin\development
@REM if errorlevel 1 (
@REM     echo Updates found, pulling changes...
@REM     call git pull origin development
@REM     pause
@REM     @REM :submodules
@REM     goto :localhost
@REM ) else (
@REM     echo No updates found.
@REM     @REM pause
@REM     goto :localhost
@REM )

echo All done!
@REM pause
echo Current directory is: %CD%
goto :localhost

:localhost
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting Localhost!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

cd %CD%\%SCRIPTS_DIR%
echo Current directory is: %CD%
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
%PYTHON_PATH% -m toontown.launcher.QuickStartLauncher
pause
goto startgame