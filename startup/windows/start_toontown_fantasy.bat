@echo off
set "projectName=PLAYER ZER0 STUDIO's Toontown Fantasy"
title %projectName% Standalone Launcher
set "projectAbbreviation=TTFan"
set "projectAbbreviationUpper=TTFAN"

:root
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting %projectName%
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
@REM set RootPath=%CD%

set PREVIOUS_DIR="..\"

cd /d %PREVIOUS_DIR%%PREVIOUS_DIR%
echo Current directory is: %CD%
echo.

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

setx %projectAbbreviationUpper%_PYTHON_PATH "%CUSTOM_PYTHON_PATH%"
echo.

echo The "%projectAbbreviationUpper%_PYTHON_PATH" variable is set as "%CUSTOM_PYTHON_PATH%"
echo.

@REM if exist %CUSTOM_PYTHON_PATH% (
@REM     echo The "CUSTOM_PYTHON_PATH" exists at %CUSTOM_PYTHON_PATH%
@REM     echo.
@REM     dir /ad %CUSTOM_PYTHON_PATH% | find "<SYMLINKD>" >nul
@REM     if %errorlevel% equ 0 (
@REM         echo The given directory is a symbolic link folder.
@REM         echo.
@REM     ) else (
@REM         echo The given directory is a normal folder, NOT a symbolic link folder.
@REM         echo.
@REM     )
@REM )

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

title %projectName%
%CUSTOM_PYTHON_PATH% -m toontown.launcher.QuickStartLauncher
pause
goto :StartGame

:ending

pause
cls
goto :root
endlocal