@echo off
title Toontown Fantasy Astron
cd ../astron

:main
astrond --loglevel info --pretty config/astrond.yml
pause
goto :main