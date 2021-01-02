@echo off
title Toontown Fantasy Uberdog
cd ..

:main
python -m toontown.uberdog.UDStart
pause
goto :main