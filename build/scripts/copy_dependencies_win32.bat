@echo off
cd ..
mkdir "bin\panda3d\"
mkdir "bin\user"
COPY "C:\OpenPanda\bin\*.dll" "bin\panda3d\"
COPY "C:\OpenPanda\panda3d\*.pyd" "bin\panda3d\"
COPY "C:\OpenPanda\python\DLLs\*" "bin\"
COPY "C:\OpenPanda\python\python39.dll" "bin\user\"
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