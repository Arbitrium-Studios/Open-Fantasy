@echo off
cd "../../astron/"
set "projectName=PLAYER ZER0 STUDIO's Toontown Fantasy"
title %projectName%'s Astron

:start
"win32/astrond" --loglevel info config/astrond.yml
pause
goto start