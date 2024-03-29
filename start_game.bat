@echo off
title PLAYER ZER0 STUDIO's Toontown Fantasy Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo What do you want to do?
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

cls
echo ===============================================================
echo What do you want to launch!
echo ===============================================================
echo. 
echo #1 - Locally Host a Server
echo #2 - Connect to an Existing Server
echo #3 - Exit
echo.
choice /C:123 /n /m "Selection: "%1
if errorlevel ==3 EXIT
if errorlevel ==2 goto connect
if errorlevel ==1 goto localhost


:localhost
cls 
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting Localhost!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
cd scripts
echo Launching Astron...
START start_astron_server.bat
echo Launching the Uberdog Server...
START start_uberdog_server.bat
echo Launching the AI Server...
START start_candy_cliffs_ai_server.bat
START start_nutty_river_ai_server.bat
START start_toon_valley_ai_server.bat
cd ..
SET TT_GAMESERVER=127.0.0.1
goto game

:connect
cls
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo What Server are you connecting to!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set /P TT_GAMESERVER="Server IP: "
set /P TT_Username="Username: "
goto game

:game
cls
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Username [!] This does get stored in your source code so beware!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set TT_Username=%username%
echo.
cls
SET LOGIN_TOKEN=%TT_Username%
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Welcome to Toontown Fantasy, %TT_Username%!
echo The Tooniverse Awaits You!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
:startgame
title Toontown Fantasy
%PPYTHON_PATH% -m toontown.launcher.QuickStartLauncher
PAUSE
goto startgame