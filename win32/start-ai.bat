@echo off
title Toontown Fantasy AI
cd ..

:main
python -m toontown.ai.AIStart
pause
goto :main