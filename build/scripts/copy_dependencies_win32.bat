@echo off
cd ..
mkdir "bin\panda3d\"
mkdir "bin\user"
COPY "C:\Open-Panda\bin\*.dll" "bin\panda3d\"
COPY "C:\Open-Panda\panda3d\*.pyd" "bin\panda3d\"
COPY "C:\Open-Panda\python\DLLs\*" "bin\"
COPY "C:\Open-Panda\python\python39.dll" "bin\user\"
COPY "..\user\*" "bin\"
DEL "bin\_msi.pyd"
DEL "bin\python_lib.cat"
DEL "bin\python_tools.cat"
DEL "bin\py.ico"
DEL "bin\pyc.ico"
DEL "bin\pyd.ico"
DEL "bin\sqlite3.dll"
DEL "bin\_sqlite3.pyd"
DEL "bin\winsound.pyd"
PAUSE