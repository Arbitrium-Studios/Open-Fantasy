@echo off
title Start Toontown Fantasy - Astron Server
cd ../astron/win32
astrond --loglevel info ../config/astrond.yml
pause
