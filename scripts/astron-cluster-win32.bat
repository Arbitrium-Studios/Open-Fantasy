@echo off
cd "../astron/"
title Toontown Fantasy Astron

:start
"win32/astrond" --loglevel info config/astrond.yml
PAUSE
goto start