@echo off
title Start Toontown Fantasy - AI (District) Server
cd..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

:district
%PPYTHON_PATH% -m toontown.ai.AIStart --base-channel 403000000 ^
               --max-channels 999999 --stateserver 4002 ^
               --messagedirector-ip 127.0.0.1:7199 ^
               --eventlogger-ip 127.0.0.1:7197 ^
               --district-name "Nutty River"

pause

goto district