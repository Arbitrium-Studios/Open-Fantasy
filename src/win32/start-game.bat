@echo off
title Toontown Fantasy Game
cd ..

:main
python -m toontown.toonbase.ToontownStart
pause
goto :main