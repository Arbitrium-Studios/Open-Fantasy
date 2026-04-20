@echo off
SetLocal DisableDelayedExpansion

set "projectOwnerName=PLAYER ZER0 STUDIO"
set "projectName=Toontown Fantasy"
set "projectNameFull=%projectOwnerName%'s %projectName%"
title %projectNameFull% Launcher
set "projectAbbreviation=TTFan"
set "projectAbbreviationUpper=TTFAN"

:: Placing any variables here allows for them to placed as is.
:: The placement of variables such as "exclaimStr" here allows exclamation points...
:: to be used in echos by surrounding the variable in exclamation points like the following:
:: !exclaimStr!
set "exclaimStr=!"

SetLocal EnableDelayedExpansion

goto :root

:root

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo                     Checking Variables and Files...
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

set PREVIOUS_DIR="..\"

set "MainDirectory="%CD%""

set "RootPath=%CD%"

set "RootPathAlt=%CD%"

set "SCRIPTS_PATH=%RootPath%\scripts"
set "SCRIPTS_DIR=scripts"
set "STARTUP_DIR=startup"
set "STARTUP_WIN_DIR=windows"

goto :set_dependencies

:set_dependencies
cd /d "%RootPath%"
set "DEPENDENCIES_PATH=dependencies"
if exist %DEPENDENCIES_PATH% (
    goto :set_panda3d
) else (
    echo Dependencies folder does not exist, creating it now.
    echo.
    mkdir %DEPENDENCIES_PATH%
    pause
    goto :set_dependencies
)

:panda3d

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting %projectNameFull%'s compiled Panda3D!exclaimStr!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

echo Directory path is: %RootPath%
echo.

goto :set_panda3d

:set_panda3d
@REM cd /d "%CD%"
cd /d "%RootPath%\%DEPENDENCIES_PATH%"
set "PANDA3D_PATH=panda3d"

if exist %PANDA3D_PATH% (
    cd /d "%PANDA3D_PATH%"
    goto :ppython
) else (
    echo The Panda3D folder does not exist, creating it now.
    echo.
    echo Created the Panda3D folder at %RootPath%\%PANDA3D_PATH%
    echo CURRENT_DIR at Panda3D Else is now set to: %CD%
    @REM pause rem for debugging purposes
    goto :panda3d_version
)

echo Choose what Panda3D version you want to use!exclaimStr!
echo.
echo #1 - Pre-Compiled
echo.
@REM echo #2 - Local Panda3D Version
@REM echo.

:panda3d_version

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    echo Pre-Compiled Panda3D version has been selected.
    echo.
    @REM echo Cloning the pre-compiled Panda3D repository.
    @REM echo.
    @REM call git clone https://github.com/Arbitrium-Studios/panda3d.git
    @REM echo Directory path is: %CD%
    @REM echo Panda3D has been retrieved.
    @REM echo.
    pause
    goto :set_panda3d
) else (
    echo Invalid selection, please try again.
    echo.
    goto :panda3d
)

:ppython

set "PYTHON_PATH_FILE=%RootPath%\PYTHON_PATH"

cd /d "%RootPath%"

REM Read the contents of PYTHON_PATH into %PYTHON_PATH%:
if exist "%PYTHON_PATH_FILE%" (
    set /p CUSTOM_PYTHON_PATH=<PYTHON_PATH
) else (
    echo Python Path File does not exist at %PYTHON_PATH_FILE%
    echo.
    goto :ending
)

if not defined %projectAbbreviationUpper%_PYTHON_PATH (
    setx %projectAbbreviationUpper%_PYTHON_PATH "%CUSTOM_PYTHON_PATH%"
    echo.
) else (
    set CUSTOM_PYTHON_PATH=%PYTHON_PATH%
)

set "PIP_PATH=%RootPath%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\Scripts\pip.exe"

cd /d "%RootPath%"

set "GET_PIP_PATH=dependencies\get-pip.py"

if exist "%CUSTOM_PYTHON_PATH%" (
    echo Yep, the "CUSTOM_PYTHON_PATH" exists at "%CUSTOM_PYTHON_PATH%"!
    echo.
    goto :login
) else (
    echo The "CUSTOM_PYTHON_PATH" does not exist at "%CUSTOM_PYTHON_PATH%"...
    echo.
    goto :ending
)

@REM goto :login

:login

set "Fallback_TTFan_Username=%username%"
set "DefaultTTFanUsernameStr=Enter input Python Path (or press ENTER to use the following default version "%Fallback_TTFan_Username%"]): "

if not defined TTFan_Username (
    goto :warningEcho
    :setUsername
    set /p "TTFan_Username=%DefaultTTFanUsernameStr%"
    echo.

    set TTFAN_PLAYCOOKIE=%TTFan_Username%

    set "greetingString=Welcome"
    goto :createUsername
) else (
    set TTFAN_PLAYCOOKIE=%TTFan_Username%
    set "greetingString=Welcome back"
    goto :defineUsernameInSystemVariables
)

:warningEcho

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Your Username is your username and does get stored in your source code so beware!exclaimStr!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

echo The Tooniverse needs your help!exclaimStr! To take your first step towards the adventure of a lifetime,
echo please enter a username to use with this computer...
echo.
echo Please note that if you clear your user environment variables, you can re-enter your previous username to regain access to your account.
echo.

goto :setUsername

:createUsername

setx TTFan_Username "%TTFan_Username%"
set "TTFAN_LOGIN_TOKEN=%TTFan_Username%"

goto :defineUsernameInSystemVariables

:defineUsernameInSystemVariables

set "TTFAN_LOGIN_TOKEN=%TTFan_Username%"

goto :localhost

:localhost
@REM cls
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo                  Starting %projectNameFull%!exclaimStr!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

cd /d "%CD%\%STARTUP_DIR%\%STARTUP_WIN_DIR%"

echo Launching Astron...
start start_astron_server.bat

echo Launching the Uberdog Server...
start start_uberdog_server.bat

echo Launching the AI Server...
start start_toon_valley_ai_server.bat

echo Launching the game client...
echo.

cd /d "%RootPath%"
set TT_GAMESERVER=127.0.0.1

goto :StartGameWithWelcome

:StartGameWithWelcome

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo     %greetingString% to %projectNameFull%, %TTFAN_LOGIN_TOKEN%!exclaimStr!
echo            The vast, ever-expanding Tooniverse awaits you...
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

:StartGame

title %projectNameFull%
%CUSTOM_PYTHON_PATH% -m toontown.launcher.QuickStartLauncher

pause
goto :StartGame

:ending

pause
@REM cls
goto :root
endlocal