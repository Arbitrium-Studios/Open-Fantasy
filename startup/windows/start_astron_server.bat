@echo off

:start_astron
SetLocal EnableDelayedExpansion

set "projectOwnerName=PLAYER ZER0 STUDIO"
set "projectName=Toontown Fantasy"
set "projectNameFull=!projectOwnerName!'s !projectName!"
title (Astron) !projectNameFull!
set "projectAbbreviation=TTFan"
set "projectAbbreviationUpper=TTFAN"
set "wantDirLogging=False"
set "wantDirLoggingCLS=True"

SetLocal EnableDelayedExpansion
for %%I in (.) do set "CURRENT_DIR_NAME=%%~nxI"

if "%wantDirLogging%" EQU "True" (
    echo The "CURRENT_DIR_NAME" variable is set to "!CURRENT_DIR_NAME!"
    echo.
)

if "!CURRENT_DIR_NAME!" EQU "windows" (
    cd /d "../../"
)

if "%wantDirLogging%" EQU "True" (
    echo Current Directory is %CD%
    echo.
)

cd /d "astron/"

"win32/astrond" --loglevel info config/astrond.yml
pause

if "%wantDirLogging%" EQU "True" (
    if "%wantDirLoggingCLS%" EQU "True" (
        cls
    )
)

goto :start_astron