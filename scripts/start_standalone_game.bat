@echo off
title PLAYER ZER0 STUDIO's Toontown Fantasy Standalone Launcher

cd ../
set ROOT_PATH=%CD%
echo Root path is: %ROOT_PATH%
echo.

cd %ROOT_PATH%
echo Directory path is: %ROOT_PATH%

set DEPENDENCIES_PATH=dependencies
echo Dependencies path is: %DEPENDENCIES_PATH%
set PANDA3D_PATH=panda3d
set PYTHON_PATH=%ROOT_PATH%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\ppython.exe
echo PYTHON_PATH is set as: %PYTHON_PATH%

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
%PYTHON_PATH% -m toontown.launcher.QuickStartLauncher
PAUSE
goto startgame