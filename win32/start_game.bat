@echo off

title Open-Fantasy Game Launcher

echo Choose your connection method!
echo.
echo #1 - Offline Mode
echo.

:selection

set INPUT=1
set /P INPUT=Selection: 

if %INPUT%==1 (
    set TT_GAMESERVER=127.0.0.1
) else (
    goto selection
)

echo.

if %INPUT%==1 (
    set /P LOGIN_TOKEN="Username: "
) else (
    set /P LOGIN_TOKEN=Username: 
)

echo.

echo ===============================
echo Starting Toontown Fantasy

if %INPUT%==1 (
    echo Username: %LOGIN_TOKEN%
) else (
    echo Username: %LOGIN_TOKEN%
)

echo Gameserver: %TT_GAMESERVER%
echo ===============================

cd ../

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

:main
if %INPUT%==1 (
    %PPYTHON_PATH% -m toontown.launcher.QuickStartLauncher
)

pause

goto main