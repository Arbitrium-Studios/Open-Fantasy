@echo off
title PLAYER ZER0 STUDIO's Toontown Fantasy Standalone Launcher

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
cd "../"
set /P PPYTHON_PATH=<PPYTHON_PATH

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