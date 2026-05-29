@echo off

:root

SetLocal EnableDelayedExpansion

set "projectOwnerName=PLAYER ZER0 STUDIO"
set "projectName=Toontown Fantasy"
set "projectNameFull=!projectOwnerName!'s !projectName!"
title (Standalone) !projectNameFull!'s Launcher
set "projectAbbreviation=TTFan"
set "projectAbbreviationUpper=TTFAN"
set "wantDirLogging=False"

if "!projectName!" NEQ "Toontown Fantasy" (
    echo The specified project name is not supported: "!projectName!"
    echo.
    goto :ending
)

if "%wantDirLogging%" EQU "True" (
    echo Current Directory is %CD%
    echo.
)

for %%I in (.) do set "CURRENT_DIR_NAME=%%~nxI"

if "%wantDirLogging%" EQU "True" (
    echo The "CURRENT_DIR_NAME" variable is set to "!CURRENT_DIR_NAME!"
    echo.
)

if "!CURRENT_DIR_NAME!" EQU "windows" (
    cd /d "../../"
)

set "ROOT_DIR=%CD%"

set "pythonPathFileName=PYTHON_PATH"
set "PYTHON_PATH_FILE=%ROOT_DIR%\%pythonPathFileName%"

if "%wantDirLogging%" EQU "True" (
    echo The "ROOT_DIR" variable is set to "%ROOT_DIR%"
    echo.
)

cd /d "%ROOT_DIR%"

if "%wantDirLogging%" EQU "True" (
    echo Directory path is: %ROOT_DIR%
    echo.
)

set "DEPENDENCIES_PATH=dependencies"

if "%wantDirLogging%" EQU "True" (
    echo Dependencies path is: %DEPENDENCIES_PATH%
    echo.
)

set "PANDA3D_PATH=panda3d"
set "SYMBOLIC_PYTHON_PATH=%ROOT_DIR%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\ppython.exe"

if "%wantDirLogging%" EQU "True" (
    echo The "SYMBOLIC_PYTHON_PATH" variable is set as: %SYMBOLIC_PYTHON_PATH%
    echo.
)

if defined AS_PYTHON_PATH (
    set "CUSTOM_PYTHON_PATH=%AS_PYTHON_PATH%"
) else (
    if exist "%PYTHON_PATH_FILE%" (
        if "%wantDirLogging%" EQU "True" (
            echo The "PYTHON_PATH_FILE" exists at "%PYTHON_PATH_FILE%"
            echo.
        )
        set /P CUSTOM_PYTHON_PATH=<PYTHON_PATH
    ) else (
        goto :does_not_exist
    )
)

goto :localhost

:localhost
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting Localhost!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

SET TT_GAMESERVER=127.0.0.1
goto :login

:login
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Your Username is your username and does get stored in your source code so beware!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

if not defined TTFan_Username (
    goto :warningEcho

    :setUsername
    set /P TTFan_Username="Username: "
    echo.

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

echo The Tooniverse needs your help! To take your first step towards the adventure of a lifetime,
echo please enter a username to use with this computer...
echo.
echo Please note that if you clear your user environment variables, you can re-enter your previous username to regain access to your account.
echo.

goto :setUsername

:createUsername

setx TTFan_Username "%TTFan_Username%"
set "TTFAN_LOGIN_TOKEN=%TTFan_Username%"

cls

goto :defineUsernameInSystemVariables

:defineUsernameInSystemVariables

set "TTFAN_LOGIN_TOKEN=%TTFan_Username%"

goto :StartGameWithWelcome

:StartGameWithWelcome
cls
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo     %greetingString% to %projectName%, %TTFAN_LOGIN_TOKEN%!
echo            The vast, ever-expanding Tooniverse awaits you...
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

:StartGame

title !projectNameFull!
"%CUSTOM_PYTHON_PATH%" -m toontown.launcher.QuickStartLauncher
echo.
goto :ending

:does_not_exist

echo The PYTHON_PATH file does NOT exist.
echo.
goto :ending

:ending

pause
cls
endlocal
goto :root