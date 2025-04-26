@echo off
title Start Toontown Fantasy - AI (District) Server

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

:district
%PYTHON_PATH% -m toontown.ai.AIStart --base-channel 403000000 ^
               --max-channels 999999 --stateserver 4002 ^
               --messagedirector-ip 127.0.0.1:7199 ^
               --eventlogger-ip 127.0.0.1:7197 ^
               --district-name "Candy Cliffs"

pause

goto district