@echo off
title Toontown Fantasy CLI Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo What do you want to do!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
echo #1 - Run Toontown Fantasy
echo #2 - Exit
echo. 
:selection
choice /C:12 /n /m "Selection: "%1
if errorlevel ==2 EXIT
if errorlevel ==1 goto run


:run
cls
echo ===============================================================
echo What do you want to launch!
echo ===============================================================
echo. 
echo #1 - Locally Host a Server
echo #2 - Connect to an Existing Server
echo.
choice /C:12 /n /m "Selection: "%1
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
START start-nutty-river-ai-server.bat
START start-thwackville-ai-server.bat
START start-toon-valley-ai-server.bat
cd ..
SET TT_GAMESERVER=127.0.0.1
goto game

:connect
cls
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo What Server are you connecting to!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set /P TT_GAMESERVER="Server IP: "
goto game

:game
cls
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Username [!] This does get stored in your source code so beware!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set /P TT_Username="Username: "
set /P TT_Password="Password: "
echo.
cls
SET LOGIN_TOKEN=%TT_Username%%TT_Password%
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Welcome to Toontown Fantasy, %TT_Username%!
echo The Tooniverse Awaits You!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
:startgame
title Toontown Fantasy
%PPYTHON_PATH% -m toontown.launcher.QuickStartLauncher
PAUSE
goto startgame