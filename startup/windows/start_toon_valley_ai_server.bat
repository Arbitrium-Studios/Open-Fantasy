@echo off

:start_district

SetLocal EnableDelayedExpansion
set "projectOwnerName=PLAYER ZER0 STUDIO"
set "projectName=Toontown Fantasy"
set "projectNameFull=!projectOwnerName!'s !projectName!"
title (District) !projectNameFull!
set "projectAbbreviation=TTFan"
set "projectAbbreviationUpper=TTFAN"
set "wantDirLogging=False"
set "wantDirLoggingCLS=True"

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

if exist "%PYTHON_PATH_FILE%" (
    if "%wantDirLogging%" EQU "True" (
        echo The "PYTHON_PATH_FILE" exists at "%PYTHON_PATH_FILE%"
        echo.
    )
    set /P CUSTOM_PYTHON_PATH=<PYTHON_PATH
) else (
    echo The PYTHON_PATH file does NOT exist.
    echo.
    goto :ending
)

if "%wantDirLogging%" EQU "True" (
    if "%wantDirLoggingCLS%" EQU "True" (
        cls
    )
)

rem Define some constants for our AI server:
set "DISTRICT_NAME=Toon Valley"
set BASE_CHANNEL=401000000
set MAX_CHANNELS=999999
set STATESERVER=4002
set MESSAGE_DIRECTOR_IP=127.0.0.1:7199
set EVENTLOGGER_IP=127.0.0.1:7197

%CUSTOM_PYTHON_PATH% -m toontown.ai.AIStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATESERVER% ^
               --messagedirector-ip %MESSAGE_DIRECTOR_IP% ^
               --eventlogger-ip %EVENTLOGGER_IP% ^
               --district-name "%DISTRICT_NAME%"

pause
goto :ending

:ending

pause
cls
endlocal
goto :start_district