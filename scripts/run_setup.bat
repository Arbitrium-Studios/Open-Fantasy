@echo off
title PLAYER ZER0 STUDIO's Toontown Fantasy - Setup

:root
echo.
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Welcome to the PLAYER ZER0 STUDIO's Toontown Fantasy Setup, %username%!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
echo Please hold on while we set up the variables for you.
echo.

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Setting Root Directory
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
set PREVIOUS_DIR=..
echo Previous directory path is: "%PREVIOUS_DIR%\"
echo.
set ROOT_PATH=%CD%
echo Starting Directory path is: %ROOT_PATH%
echo.
set DIRECTORY_PATH=%ROOT_PATH%
echo set DIRECTORY PATH to: %DIRECTORY_PATH%
echo.
@REM set SCRIPTS_PATH=%ROOT_PATH%\scripts
set SCRIPTS_DIR=scripts
echo Scripts Directory path is: %SCRIPTS_DIR%
echo.
set DEPENDENCIES_PATH=%ROOT_PATH%\dependencies
echo The Dependencies Path variable has been set to is: %DEPENDENCIES_PATH%

:scripts

echo Choose what script you want to test!

echo.
echo #1 - Check for what is missing
echo.
echo #2 - Get Dependencies
echo.
echo #3 - Get Panda3D
echo.
echo #4 - Python
echo.
echo #5 - Requirements
echo.
echo #6 - Initialize & Download Submodules
echo.
echo #7 - Update Submodules
echo.
echo #8 - Go Back to the Main Menu
echo.
echo #9 - All of the above

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    @REM cls
    @REM title PLAYER ZER0 STUDIO's Toontown Fantasy - Setup
    @REM call
    echo.
    echo Running Setup Script.
    pause
    @REM goto :set_panda3d
) else if %INPUT%==2 (
    echo Local Panda3D version selected.
    set /P PANDA3D_PATH="Please Enter the path to your local Panda3D folder: "
    echo PANDA3D_PATH is now set to: %PANDA3D_PATH%
    pause
    goto :set_panda3d
) else (
    echo Invalid selection, please try again.
    goto :scripts
)








echo.

:set_dependencies
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Checking PLAYER ZER0 STUDIO's Toontown Fantasy's Dependencies
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
echo Directory path is: %ROOT_PATH%
echo.
set CURRENT_DIR=%DEPENDENCIES_PATH%
echo Checking if the dependencies folder exists.
if exist %DEPENDENCIES_PATH% (
    echo Cool! Dependencies folder exists at %DEPENDENCIES_PATH%
    echo.
    echo Entering the dependencies folder.
    cd %DEPENDENCIES_PATH%
    echo.
    echo Current directory path in set_dependencies is: %CURRENT_DIR%
    @REM pause rem for debugging purposes
    goto :panda3d
) else (
    echo Dependencies folder does not exist, creating it now.
    mkdir %DEPENDENCIES_PATH%
    echo Created the dependencies folder at %CD%\%DEPENDENCIES_PATH%
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
set PANDA3D_PATH=panda3d
set PANDA3D_DIR=%DEPENDENCIES_PATH%\panda3d
echo Set the PANDA3D_PATH variable to: %PANDA3D_PATH%
@REM set CURRENT_DIR=%CD%
echo.
echo Checking if the Panda3D folder exists.
if exist %PANDA3D_PATH% (
    echo Cool! The Panda3D folder exists at %PANDA3D_PATH%
    echo.
    echo Entering the Panda3D folder.
    cd %PANDA3D_PATH%
    set CURRENT_DIR=%PANDA3D_PATH%
    echo CURRENT_DIR is now set to: %CD%
    echo Current directory path in set_panda3d is: %CURRENT_DIR%
    @REM echo.
    @REM echo The PREVIOUS_DIR variable is set to: %PREVIOUS_DIR%
    @REM set 
    @REM echo.
    @REM echo Checking for updates to the Panda3D repository.
    @REM echo.
    @REM call git fetch origin development && git status --porcelain
    @REM call git pull https://github.com/Arbitrium-Studios/panda3d.git main --allow-unrelated-histories
    @REM echo.
    echo.
    @REM echo Current directory path in set_panda3d is: %PANDA3D_PATH%
    pause rem for debugging purposes
    goto :panda3d
) else (
    echo The Panda3D folder does not exist, creating it now.
    @REM mkdir %PANDA3D_PATH%
    echo Created the Panda3D folder at %PANDA3D_PATH%
    pause rem for debugging purposes
    @REM goto :set_dependencies
)

@REM :panda3d

@REM echo.
@REM echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
@REM echo Getting PLAYER ZER0 STUDIO's Toontown Fantasy's compiled Panda3D
@REM echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
@REM echo.
@REM echo Current directory path in panda3d is: %DIRECTORY_PATH%
@REM @REM echo Root path is: %CD%
@REM goto :set_panda3d

@REM :set_panda3d
@REM @REM cd %ROOT_PATH%/%DEPENDENCIES_PATH%
@REM @REM echo Directory path is: %CD%
@REM @REM set DIRECTORY_PATH=%CD%
@REM set PANDA3D_PATH=%DEPENDENCIES_PATH%\panda3d
@REM echo Set the PANDA3D_PATH variable to: %PANDA3D_PATH%
@REM echo.
@REM @REM cd %CD%\%PANDA3D_PATH%
@REM if exist %PANDA3D_PATH% (
@REM     echo Cool! The Panda3D folder exists at %PANDA3D_PATH%
@REM     echo Directory path is: %ROOT_PATH%
@REM     echo.
@REM     echo Entering the Panda3D folder.
@REM     cd %PANDA3D_PATH%
@REM     @REM echo.
@REM     @REM echo Checking for updates to the Panda3D repository.
@REM     echo.
@REM     echo Directory path is: %ROOT_PATH%
@REM     @REM call git fetch origin development && git status --porcelain
@REM     @REM call git pull https://github.com/Arbitrium-Studios/panda3d.git main --allow-unrelated-histories
@REM     echo.
@REM     @REM cd %PANDA3D_PATH%
@REM     @REM goto :ppython
@REM     pause
@REM ) else (
@REM     echo Panda3d folder does not exist.
@REM     echo Directory path is: %ROOT_PATH%
@REM     goto :panda3D_version
@REM )

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
    @REM goto :set_panda3d
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
pause

@REM :ppython
@REM echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
@REM echo Setting Python Path
@REM echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

@REM cd %PREVIOUS_DIR%
@REM echo Current directory is: %CD%

@REM rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
@REM set /P PPYTHON_PATH=<PPYTHON_PATH
@REM echo Python path is: %PPYTHON_PATH%
@REM set PIP_PATH=/panda3d/python/Scripts/pip.exe

@REM goto :requirements

@REM :requirements
@REM echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
@REM echo Getting Requirements
@REM echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

@REM call %PPYTHON_PATH% %DEPENDENCIES_PATH%/%PIP_PATH% install -r requirements.txt
@REM call %PPYTHON_PATH% -m %DEPENDENCIES_PATH%/%PIP_PATH% install --upgrade pip

@REM goto :submodules

@REM :submodules
@REM echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
@REM echo Getting Submodules
@REM echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
@REM %PPYTHON_PATH% %DEPENDENCIES_PATH%/initialize.py
@REM @REM call git submodule update --init --recursive

@REM goto :updates

@REM :updates

@REM echo Checking for updates from the development branch.
@REM call git fetch origin development && git status --porcelain
@REM call git diff --quiet HEAD..origin/development
@REM if errorlevel 1 (
@REM     echo Updates found, pulling changes...
@REM     call git pull origin development
@REM     @REM :submodules
@REM     goto :updates
@REM ) else (
@REM     echo No updates found.
    
@REM     goto :localhost
@REM )

echo All done!
goto :account_setup

:account_setup

if exist %ROOT_PATH%\%ACCOUNT_DIR%\accounts.json (
    echo.
    echo The accounts.json file exists in %ROOT_PATH%\%ACCOUNT_DIR%.
    echo.
    pause
    @REM goto :set_dependencies
) else (
    echo.
    echo The accounts.json file does NOT exist in %ROOT_PATH%\%ACCOUNT_DIR%.
    echo.
    copy /y nul %ROOT_PATH%\%ACCOUNT_DIR%\accounts.json

    pause
)

pause