@echo off
title PLAYER ZER0 STUDIO's Toontown Fantasy Standalone Launcher

:root
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Setting Root Directory
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
cd ..
echo Current directory is: %CD%
echo .
set ROOT_PATH=%CD%
set PREVIOUS_DIR="..\"
echo Root path is: %ROOT_PATH%

echo.

cd %PREVIOUS_DIR%
echo Current directory is: %CD%

goto :ppython

echo.

:ppython
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Setting Python Path
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

cd %ROOT_PATH%
echo Current directory at PYTHON_PATH is: %CD%
echo.
set DEPENDENCIES_PATH=dependencies
set PANDA3D_PATH=panda3d
echo .
echo Current directory at requirements is: %CD%
echo ROOT_PATH is: %CD%
echo Dependencies path is: %DEPENDENCIES_PATH%
set PYTHON_PATH=%ROOT_PATH%\%DEPENDENCIES_PATH%\%PANDA3D_PATH%\python\ppython.exe
echo PYTHON_PATH is set as: %PYTHON_PATH%


echo Current directory is: %CD%
goto :localhost

:localhost
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting Localhost!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

SET TT_GAMESERVER=127.0.0.1
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
%PYTHON_PATH% -m toontown.launcher.QuickStartLauncher
pause
goto startgame