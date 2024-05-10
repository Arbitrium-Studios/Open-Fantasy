@echo off
title PLAYER ZER0 STUDIO's Toontown Fantasy Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting Submodules
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
call git submodule update --init --recursive
call git clone https://github.com/Arbitrium-Studios/resources.git

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Getting Requirements
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
call "../dependencies\panda3d\python\Scripts\pip.exe" install -r requirements.txt

:localhost
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting Localhost!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
cd "scripts"
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
timeout 4
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
%PPYTHON_PATH% -m toontown.launcher.QuickStartLauncher
PAUSE
goto startgame