@echo off

:root

SetLocal DisableDelayedExpansion

:: Placing any variables here allows for them to placed as is.
:: The placement of variables such as "exclaimStr" here allows exclamation points...
:: ...to be used in echos by surrounding the variable in exclamation points like the following:
:: !exclaimStr!
set "exclaimStr=!"

SetLocal EnableDelayedExpansion

for /f "tokens=*" %%a in ('git remote get-url origin') do set "url=%%a"
:: Remove potential .git suffix and extract the part after the last slash

for %%f in ("%url:/=\%") do set "repo_name=%%~nf"
echo Repository Name: %repo_name%
echo.

set "STARTUP_DIR=startup"
set "STARTUP_WIN_DIR=windows"

if "%repo_name%" EQU "THE_STAICY_B0T" (
    set "projectOwnerName=Nexus Application"
    set "ROOT_DIR=%~dp0"
    set "ROOT_DIR=!ROOT_DIR:~0,-1!"

    if "%CD%" NEQ "!ROOT_DIR!" (
        cd /d "!ROOT_DIR!"
    )

    for %%I in (.) do set "DirectoryName=%%~nxI"
    if "!DirectoryName!" EQU "windows" (
        set "ROOT_DIR=!CD!"
    )
    set "STARTUP_PATH=!ROOT_DIR!\!STARTUP_DIR!\!STARTUP_WIN_DIR!"

    set "projectAbbreviation=TSB"
    for %%I in (.) do set "PROJECT_NAME=%%~nxI"
    set "projectName=!PROJECT_NAME!"
    set "projectNameFull=!projectOwnerName!'s !projectName!"
    title Launching !projectNameFull!

    set "LAUNCHER_PATH=!STARTUP_PATH!\start_staicy.bat"
) else if "%repo_name%" EQU "Open-Fantasy" (
    set "projectOwnerName=PLAYER ZER0 STUDIO"
    set "projectName=Toontown Fantasy"
    set "projectNameFull=!projectOwnerName!'s !projectName!"
    title Launching !projectNameFull!'s Standalone Launcher
    set "projectAbbreviation=TTFan"

    set "ROOT_DIR=%~dp0"
    set "ROOT_DIR=!ROOT_DIR:~0,-1!"

    if "%CD%" NEQ "!ROOT_DIR!" (
        cd /d "!ROOT_DIR!"
    )

    set "SCRIPTS_PATH=!ROOT_DIR!\scripts"
    set "SCRIPTS_DIR=scripts"
    set "STARTUP_PATH=!ROOT_DIR!\!STARTUP_DIR!\!STARTUP_WIN_DIR!"
    set "ASTRON_PATH=!STARTUP_PATH!\start_astron_server.bat"
    set "UBERDOG_PATH=!STARTUP_PATH!\start_uberdog_server.bat"
    set "AI_PATH=!STARTUP_PATH!\start_toon_valley_ai_server.bat"
    set "LAUNCHER_PATH=!STARTUP_PATH!\start_toontown.bat"

) else (
    goto :unsupported
)

set "wantExtraLogging=False"
set "wantDirLoggingCLS=False"

set "fileName=%~nx0"

if "%wantExtraLogging%" EQU "True" (
    echo Hello from the "!fileName!" file!exclaimStr!
    echo.
)

if "%wantExtraLogging%" EQU "True" (
    echo The Current Directory is "%CD%"
    echo.
)

set "GetPipWeb=https://bootstrap.pypa.io/get-pip.py"
set "GET_PIP=get-pip.py"

set "PackageDependencies=%ROOT_DIR%\dependencies\packages"
set "getPipPackageDependencies=%ROOT_DIR%\dependencies\packages\%GET_PIP%"
set "PANDA3D_TYPE=Open-Panda"
set "PANDA3D_TYPE_FULL=!PANDA3D_TYPE!3D"

set "pythonInterpreter="
set "pythonName=python"
set "ppythonName=ppython"
set "Executable=exe"
set "PythonExe=%pythonName%.%Executable%"
set "PPythonExe=%ppythonName%.%Executable%"

set "RequirementsIn=requirements.in"
set "RequirementsTXT=requirements.txt"
set "RequirementsInPath=%ROOT_DIR%\%RequirementsIn%"
set "RequirementsTXTPath=%ROOT_DIR%\%RequirementsTXT%"
set "RequirementsInDownload=https://cdn.arbitriumstudios.com/application_assets/bots/tsb_assets/dependencies/packages/requirements.in"

set "latestVersionOfOpenPanda3D=1.11.2"
set "OP3D_v1.11.1=https://github.com/Arbitrium-Studios/!PANDA3D_TYPE!/releases/download/v1.11.1/!PANDA3D_TYPE!-1.11.1-py3.11-x64.exe"
set "OP3D_v1.11.2=https://github.com/Arbitrium-Studios/!PANDA3D_TYPE!/releases/download/v1.11.2-Pre_Release/!PANDA3D_TYPE_FULL!-1.11.2-py3.13.exe"
set "OpenPanda3DInstallerExecutableName=!PANDA3D_TYPE_FULL!-v!latestVersionOfOpenPanda3D!-py3.13.!Executable!"
set "LatestOfficialOpenPanda3DInstaller=https://github.com/Arbitrium-Studios/!PANDA3D_TYPE!/releases/download/v!latestVersionOfOpenPanda3D!/!OpenPanda3DInstallerExecutableName!"

set "OpenPanda3DInstallerPath=%PackageDependencies%\%OpenPanda3DInstallerExecutableName%"

set "pythonPathFileName=PYTHON_PATH"
set "PYTHON_PATH_FILE=%ROOT_DIR%\%pythonPathFileName%"
set "PPYTHON_PATH_FILE=%ROOT_DIR%\P%pythonPathFileName%"

set "DEPENDENCIES_DIR=dependencies"
set "PANDA3D_DIR=panda3d"

set "DEPENDENCIES_PATH=%ROOT_DIR%\%DEPENDENCIES_DIR%"
set "SYMBOLIC_PANDA3D_PATH=%ROOT_DIR%\%DEPENDENCIES_DIR%\%PANDA3D_DIR%"

:: Check for the "L" attribute (Reparse Point/Symbolic Link)
dir /ad /al "%DEPENDENCIES_PATH%" >nul 2>&1
if %errorlevel%==0 (
    for /f "tokens=2 delims=[]" %%a in ('dir /ad /al "%DEPENDENCIES_PATH%" ^| findstr "\["') do set "PRESET_PANDA3D_PATH=%%a"
) else (
    set "PRESET_PANDA3D_PATH=%SYMBOLIC_PANDA3D_PATH%"
)

set "pythonVersionStr=Python 3"

set "DefaultPanda3DPath=C:\!PANDA3D_TYPE!"
set "DefaultPythonPath=%DefaultPanda3DPath%\!pythonName!\!PythonExe!"
set "DefaultPythonPathFallback=%DefaultPythonPath%"

set "CUSTOM_PYTHON_PATH="""
set "REBUILT_PYTHON_PATH="""
set "CUSTOM_AS_PYTHON_PATH"="""

set LF=!LF!

:SelectPythonDirectory

REM Read the contents of PYTHON_PATH into %PYTHON_PATH%:
if exist "%PYTHON_PATH_FILE%" (
    echo The "PYTHON_PATH_FILE" exists at "%PYTHON_PATH_FILE%"
    echo.
    set /P CUSTOM_PYTHON_PATH=<PYTHON_PATH
) else if exist "%PPYTHON_PATH_FILE%" (
    set /P CUSTOM_PYTHON_PATH=<PPYTHON_PATH
    echo Python Path is set to %PYTHON_PATH%
    echo.
) else (
    echo The PYTHON_PATH file does NOT exist.
    echo.
    goto :set_python_path
)

:: Use quotes to handle paths with spaces
set "SelectedPythonPathFile=%CUSTOM_PYTHON_PATH%"

:: Cleans "%LF%" character
set "SelectedPythonPathFile=!SelectedPythonPathFile:"%LF%=!"
set "SelectedPythonPathFile=%SelectedPythonPathFile%"
echo SelectedPythonPathFile is set to %SelectedPythonPathFile%
echo.

:: Check if the specified file exists
if exist "%SelectedPythonPathFile%" (
    echo Success: The file exists at the given directory: %CUSTOM_PYTHON_PATH%
    echo.
    :: Create or update the necessary file
    echo | set /p=""%SelectedPythonPathFile%"" > %pythonPathFileName%

    echo The "SelectedPythonPathFile" variable is set to %SelectedPythonPathFile%
    echo.
    set "CUSTOM_PYTHON_PATH=%SelectedPythonPathFile%"
) else (
    echo The "SelectedPythonPathFile" does not exist at "%SelectedPythonPathFile%".
    echo.
    goto :set_python_path
)

echo The "CUSTOM_PYTHON_PATH" variable is set to "%CUSTOM_PYTHON_PATH%"
echo.

if defined AS_PYTHON_PATH (
    if exist "%PRESET_PANDA3D_PATH%" (
        if "!PRESET_PANDA3D_PATH:~-10!" EQU "!PythonExe!" (
            set "REBUILT_PYTHON_PATH=%PRESET_PANDA3D_PATH%"
            echo The "REBUILT_PYTHON_PATH" variable is set to "!REBUILT_PYTHON_PATH!"
            echo.
            goto :setCustomPanda3DPathWithoutRebuilt
        ) else if "!PRESET_PANDA3D_PATH:~-11!" EQU "!PPythonExe!" (
            set "REBUILT_PYTHON_PATH=%PRESET_PANDA3D_PATH%"
            echo The "REBUILT_PYTHON_PATH" variable is set to "!REBUILT_PYTHON_PATH!"
            echo.
            goto :setCustomPanda3DPathWithoutRebuilt
        ) else (
            set "OPEN_PANDA_PATH=%PRESET_PANDA3D_PATH%"
            echo The "OPEN_PANDA_PATH" variable is set to "!OPEN_PANDA_PATH!"
            echo.
            goto :setCustomPanda3DPath
        )
    ) else (
        echo The "PRESET_PANDA3D_PATH" variable does not exist at "%PRESET_PANDA3D_PATH%"
        echo.
        set "PRESET_PANDA3D_PATH=%AS_PYTHON_PATH%"
        set "REBUILT_PYTHON_PATH=%AS_PYTHON_PATH%"
        goto :setCustomPanda3DPathWithoutRebuilt
    )
) else (
    if exist "%PRESET_PANDA3D_PATH%" (
        echo The "PRESET_PANDA3D_PATH" variable is set to %PRESET_PANDA3D_PATH%.
        echo.
        set "OPEN_PANDA_PATH=%PRESET_PANDA3D_PATH%"
        goto :setCustomPanda3DPath
    ) else (
        set "OPEN_PANDA_PATH=%CUSTOM_PYTHON_PATH%"
        goto :setCustomPanda3DPath
    )
)

:setCustomPanda3DPath

set "REBUILT_PYTHON_PATH=%OPEN_PANDA_PATH%\!pythonName!\!PythonExe!"

:setCustomPanda3DPathWithoutRebuilt

if exist "%REBUILT_PYTHON_PATH%" (
    set "CUSTOM_PYTHON_PATH=%REBUILT_PYTHON_PATH%"

    if not defined AS_PYTHON_PATH (
        setx AS_PYTHON_PATH "%REBUILT_PYTHON_PATH%"
        goto :Update_PYTHON_PATH_File
    ) else (
        if "%AS_PYTHON_PATH%" == "%REBUILT_PYTHON_PATH%" (
            echo The "AS_PYTHON_PATH" and the "REBUILT_PYTHON_PATH" variables are the exact same and set to "%REBUILT_PYTHON_PATH%"
            echo.
            goto :Update_PYTHON_PATH_File
        ) else (
            echo The "AS_PYTHON_PATH" and the "REBUILT_PYTHON_PATH" variables are NOT the same.
            echo.

            echo The "REBUILT_PYTHON_PATH" variable exists at "%REBUILT_PYTHON_PATH%"
            echo.
            echo The "AS_PYTHON_PATH" variable is set to "%AS_PYTHON_PATH%"
            echo.
            echo Do you wish to update the "AS_PYTHON_PATH" variable to use the REBUILT_PYTHON_PATH variable?
            echo.
            choice /C YN /M "(Y)es/(N)o "
            echo.
            if ErrorLevel 2 goto :NoPythonPathUpdate
            if ErrorLevel 1 goto :YesUpdatePythonPath
        )
    )
) else (
    echo The "REBUILT_PYTHON_PATH" variable does NOT exist at "%REBUILT_PYTHON_PATH%"
    echo.
    goto :set_python_path
)

:YesUpdatePythonPath
echo You chose "Yes" to updating the program's Python Path!exclaimStr!
echo.

echo The "CUSTOM_PYTHON_PATH" variable is set to "%CUSTOM_PYTHON_PATH%"
echo The "REBUILT_PYTHON_PATH" variable is set to "%REBUILT_PYTHON_PATH%"
echo.

if not "%CUSTOM_PYTHON_PATH%" EQU "" if not "%REBUILT_PYTHON_PATH%" EQU "" (
    if "%REBUILT_PYTHON_PATH%" == "%CUSTOM_PYTHON_PATH%" (
        if not "%AS_PYTHON_PATH%" == "%CUSTOM_PYTHON_PATH%" (
            echo "%AS_PYTHON_PATH%" does not equal "%CUSTOM_PYTHON_PATH%"
            echo.
            set "CUSTOM_AS_PYTHON_PATH=%CUSTOM_PYTHON_PATH%"
            setx AS_PYTHON_PATH "%REBUILT_PYTHON_PATH%"
            echo.
        ) else (
            echo "%AS_PYTHON_PATH%" equals "%CUSTOM_PYTHON_PATH%"!exclaimStr!
            echo.
            set "CUSTOM_AS_PYTHON_PATH=%CUSTOM_PYTHON_PATH%"
        )
    )

) else if defined %CUSTOM_PYTHON_PATH% (
    echo The "CUSTOM_PYTHON_PATH" variable is set to "%CUSTOM_PYTHON_PATH%"
    echo.
    set "CUSTOM_AS_PYTHON_PATH=%CUSTOM_PYTHON_PATH%"
    if not "%AS_PYTHON_PATH%" == "%CUSTOM_PYTHON_PATH%" (
        echo "%AS_PYTHON_PATH%" does not equal "%CUSTOM_PYTHON_PATH%"!exclaimStr!
        echo.
        setx AS_PYTHON_PATH "%CUSTOM_PYTHON_PATH%"
        echo.
    ) else (
        echo "%AS_PYTHON_PATH%" equals "%CUSTOM_PYTHON_PATH%"!exclaimStr!
        echo.
    )
) else if defined %REBUILT_PYTHON_PATH% (
    echo The "REBUILT_PYTHON_PATH" variable is set to "%REBUILT_PYTHON_PATH%"
    echo.
    set "CUSTOM_AS_PYTHON_PATH=%REBUILT_PYTHON_PATH%"
    if not "%AS_PYTHON_PATH%" == "%REBUILT_PYTHON_PATH%" (
        echo "%AS_PYTHON_PATH%" does not equal "%REBUILT_PYTHON_PATH%"!exclaimStr!
        echo.
        setx AS_PYTHON_PATH "%REBUILT_PYTHON_PATH%"
        echo.
    ) else (
        echo "%AS_PYTHON_PATH%" equals "%REBUILT_PYTHON_PATH%"!exclaimStr!
        echo.
    )
)

goto :Update_PYTHON_PATH_File

:Update_PYTHON_PATH_File

echo The Current Directory is "%CD%"
echo.

if "%CUSTOM_AS_PYTHON_PATH%" EQU "" (
    if not "%AS_PYTHON_PATH%" EQU "" (
        set "CUSTOM_AS_PYTHON_PATH=%AS_PYTHON_PATH%"
    )
)

echo The "CUSTOM_AS_PYTHON_PATH" variable is set to "%CUSTOM_AS_PYTHON_PATH%"
echo.

:: Use quotes to handle paths with spaces
set "INPUT_AS_PYTHON_PATH=%CUSTOM_AS_PYTHON_PATH%"

:: Cleans the " character
set "INPUT_AS_PYTHON_PATH=!INPUT_AS_PYTHON_PATH:"=!"

echo The "INPUT_AS_PYTHON_PATH" variable is set to "%INPUT_AS_PYTHON_PATH%"
echo.

if "!INPUT_AS_PYTHON_PATH:~-10!" EQU "%PythonExe%" (
    echo The following input ends with %PythonExe%: "%INPUT_AS_PYTHON_PATH%"
    echo.
) else if "!INPUT_AS_PYTHON_PATH:~-11!" EQU "%PPythonExe%" (
    echo The following input ends with %PPythonExe%: "%INPUT_AS_PYTHON_PATH%"
    echo.
) else (
    echo Error: Input does not end with "%PythonExe%" or "%PPythonExe%".
    echo.
)

:question_userInput_existence

set "INPUT_AS_PYTHON_PATH_ADJUSTED=!INPUT_AS_PYTHON_PATH:/=\!"

echo The "INPUT_AS_PYTHON_PATH_ADJUSTED" variable is set to "!INPUT_AS_PYTHON_PATH_ADJUSTED!"
echo.

set "pythonDirDelim=\"

echo The "pythonDirDelim" variable is set to "!pythonDirDelim!"
echo.

set "modified_python_path_input_string=!INPUT_AS_PYTHON_PATH_ADJUSTED:%pythonDirDelim%=,!"

set "beforePythonDir="
for /f "tokens=1-4 delims=," %%a in ("!modified_python_path_input_string!") do (
    set "beforePythonDir=%%a\%%b"
    if "%wantExtraLogging%" EQU "True" (
        echo Token 1: %%a
        echo Token 2: %%b
        echo Token 3: %%c
        echo Token 4: %%d
        echo.
        echo The "beforePythonDir" variable is set to "!beforePythonDir!"
        echo.
    )
)

:: Check if the specified file exists
if exist "%INPUT_AS_PYTHON_PATH%" (

    echo Yes, the contents of the "INPUT_AS_PYTHON_PATH" variable exist at the given directory: "%INPUT_AS_PYTHON_PATH%"
    echo.

    if "!CD!" NEQ "!ROOT_DIR!" (
        cd /d "!ROOT_DIR!"
    )

    :: Create or update the necessary file
    echo | set /p=""%INPUT_AS_PYTHON_PATH%"" > %pythonPathFileName%

    echo Updated the "%pythonPathFileName%" file to %INPUT_AS_PYTHON_PATH%
    echo.

    if not defined AS_PYTHON_PATH (
        setx AS_PYTHON_PATH "!INPUT_AS_PYTHON_PATH!"
    )

    if "%AS_PYTHON_PATH%" NEQ "!INPUT_AS_PYTHON_PATH!" (
        setx AS_PYTHON_PATH "!INPUT_AS_PYTHON_PATH!"
    )

    if not exist "!SYMBOLIC_PANDA3D_PATH!" (
        goto :create_symbolic_link
    )

    set "CUSTOM_AS_PYTHON_PATH=%INPUT_AS_PYTHON_PATH%"
    goto :launcher
) else (
    echo Error: The specified file was not found.
    echo Please check the path and try again.
    echo.
    goto :custom_panda3d_directory
)

:create_symbolic_link

if not exist "%SYMBOLIC_PANDA3D_PATH%" (
    if not exist "%INPUT_AS_PYTHON_PATH%" (
        echo Error: The specified python path was not found.
        echo Please check the path and try again.
        echo.
        goto :set_python_path
    ) else (

        if "!beforePythonDir!" NEQ "" (
            if exist "!beforePythonDir!" (
                cd /d "!DEPENDENCIES_PATH!"
                mklink /d "!PANDA3D_DIR!" "!beforePythonDir!"
                echo.
            )
        )

        echo The "INPUT_AS_PYTHON_PATH" variable is set to "%INPUT_AS_PYTHON_PATH%"
        echo.

        if "!CD!" NEQ "!ROOT_DIR!" (
            cd /d "!ROOT_DIR!"
        )

        set "CUSTOM_AS_PYTHON_PATH=%INPUT_AS_PYTHON_PATH%"
        goto :launcher
    )
) else (
    goto :launcher
)

goto :python_check

:NoPythonPathUpdate
echo You chose "No" to updating the program's Python Path.
echo.
goto :python_check

:python_check
if exist "%CUSTOM_AS_PYTHON_PATH%" (
    if "%CUSTOM_AS_PYTHON_PATH%" EQU "" (
        echo The specified "CUSTOM_AS_PYTHON_PATH" is blank: "%CUSTOM_AS_PYTHON_PATH%"
        echo.
        goto :set_python_path
    ) else (
        echo The specified "CUSTOM_AS_PYTHON_PATH" exists at "%CUSTOM_AS_PYTHON_PATH%".
        echo.

        if /i "%CUSTOM_AS_PYTHON_PATH:~-10%" EQU "!PythonExe!" (
            echo The specified python path exists at "%CUSTOM_AS_PYTHON_PATH%"!exclaimStr!
            echo.

            goto :check_path_in_environment_variables
        ) else if /i "%CUSTOM_AS_PYTHON_PATH:~-11%" EQU "p!PythonExe!" (
            echo The specified python path exists at "%CUSTOM_AS_PYTHON_PATH%"!exclaimStr!
            echo.

            goto :check_path_in_environment_variables
        ) else (
            echo The string does NOT end with !PythonExe!
            echo.
            goto :set_python_path
        )
    )
) else (
    goto :doesNotExistPythonPath
)

:doesNotExistPythonPath

echo The python path variable you provided does not exist...
echo.
goto :set_python_path

:set_python_path

echo Select how you want to proceed:
echo.
echo #1 - Enter Custom Python Path
echo #2 - Select Python Path from Windows Path
echo #3 - Install Python
echo.

:selection

set INPUT=-1
set /P INPUT=Selection: 
echo.

if %INPUT%==1 (
    goto :set_custom_python_path
) else if %INPUT%==2 (
    goto :check_path_in_environment_variables
) else if %INPUT%==3 (
    goto :install_python
) else (
    goto :selection
)

echo.

:set_custom_python_path

set "DefaultPythonPathStr=Enter input Python Path (or press ENTER to use the following default version "%DefaultPythonPathFallback%"]): "

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Enter the path to your version of %pythonVersionStr% in Open-Panda3D:
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.
:set_custom_python_path_functionality

set /P "DefaultPythonPath=%DefaultPythonPathStr%"
echo.
set "ENTERED_PYTHON_PATH=%DefaultPythonPath%"

:set_custom_python_path_functionality_textless

if exist "%ENTERED_PYTHON_PATH%" (
    echo The "ENTERED_PYTHON_PATH" variable is set to "%ENTERED_PYTHON_PATH%"
    echo.
    set "CUSTOM_AS_PYTHON_PATH=%ENTERED_PYTHON_PATH%"
    goto :entered_python_path_exists
) else (
    set "typed_python_path=%DefaultPythonPath%"
    echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    echo Enter the path to your version of %pythonVersionStr% in Open-Panda3D:
    echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    echo.
    if exist "%DefaultPythonPathFallback%" (
        set "DefaultPythonPathStr=Please input a valid Python Path (or press ENTER to use the following default version "%DefaultPythonPathFallback%"]): "
    ) else (
        set "DefaultPythonPathStr=Please input a valid Python Path: "
    )
    echo The path you have entered doesn't exist.
    echo.
    goto :set_custom_python_path_functionality
)

:entered_python_path_exists

echo The path you entered exists!exclaimStr!
echo.

goto :untyped_python_path

:untyped_python_path

set "listOfPanda3DFolderNames=Panda Panda3D Open-Panda3D Open-Panda"
set "foundPanda3DFolder=false"
for %%a in (%listOfPanda3DFolderNames%) do (
    if not "!ENTERED_PYTHON_PATH:%%a=!" EQU "!ENTERED_PYTHON_PATH!" (
        set "foundPanda3DFolder=true"
    )
)

if "!foundPanda3DFolder!" EQU "true" (
    if exist "%ENTERED_PYTHON_PATH%" (

        set "INPUT_AS_PYTHON_PATH=%ENTERED_PYTHON_PATH%"
        if /i "%ENTERED_PYTHON_PATH:~-10%" EQU "!PythonExe!" (
            set "CUSTOM_AS_PYTHON_PATH=%ENTERED_PYTHON_PATH%"
            echo The specified python path exists at "!CUSTOM_AS_PYTHON_PATH!"!exclaimStr!
            echo.

            goto :create_symbolic_link
        ) else if /i "%ENTERED_PYTHON_PATH:~-11%" EQU "p!PythonExe!" (
            set "CUSTOM_AS_PYTHON_PATH=%ENTERED_PYTHON_PATH%"
            echo The specified python path exists at "!CUSTOM_AS_PYTHON_PATH!"!exclaimStr!
            echo.

            goto :create_symbolic_link
        ) else (
            echo The string does NOT end with !PythonExe!
            echo.
            goto :set_custom_python_path
        )
    ) else (
        echo The entered python path does not exist at the path specified...
        echo.
        goto :set_custom_python_path
    )
) else (
    echo Error: Please enter a directory that contains a copy of "Open-Panda3D" and ensure that it contains one of the following words: "Panda", "Panda3D", "Open-Panda3D", or "Open-Panda".
    echo.
    goto :set_custom_python_path
)

:check_path_in_environment_variables

if defined AS_PYTHON_PATH (
    echo The variable "AS_PYTHON_PATH" already exists at: %AS_PYTHON_PATH%
    echo.
    set "SYMBOLIC_PANDA3D_PATH=%AS_PYTHON_PATH%"
    goto :ensure_panda3d_directory
) else (
    echo The "AS_PYTHON_PATH" variable is not in the user environment variables...
    echo.
    goto :set_custom_python_path
)

:install_python

if exist "%PackageDependencies%" (
    echo Found the "PackageDependencies" directory at "%PackageDependencies%"
    echo.
    cd /d "%PackageDependencies%"
    set "OpenPanda3DInstallerDirectory=%PackageDependencies%"
) else (
    echo Unable to locate the "PackageDependencies" directory at "%PackageDependencies%" Setting the install directory to the current directory at "%CD%"
    echo.
    set "OpenPanda3DInstallerDirectory=%CD%"
)

echo The directory the Open-Panda3D installer will be downloaded to is "%OpenPanda3DInstallerDirectory%"
echo.

cd /d "%OpenPanda3DInstallerDirectory%"

goto :OpenPanda3DInstaller

:OpenPanda3DInstaller

if not exist "!OpenPanda3DInstallerPath!" (
    echo Downloading "!OpenPanda3DInstallerExecutableName!" into the "!PackageDependencies!" directory!exclaimStr!
    echo.

    bitsadmin /transfer "DownloadOpenPanda3DJob" /priority high "!LatestOfficialOpenPanda3DInstaller!" "!OpenPanda3DInstallerPath!"
    echo.

    if %ERRORLEVEL% EQU 0 (
        echo Successfully downloaded the installer!exclaimStr!
        echo.
        goto :start_python_installer
    ) else (
        echo Failed to download !LatestOfficialOpenPanda3DInstaller! with error code %ERRORLEVEL%. Please check your internet connection or try again later.
        echo.
        goto :ending
    )
) else (
    echo The "!OpenPanda3DInstallerExecutableName!" installer already exists in the "!PackageDependencies!" directory!exclaimStr!
    echo.
    goto :file_cleanup
)

:start_python_installer

echo Running installation script...
echo.

echo Please note that if you enter a custom installation directory/drive when installing Open-Panda3D, please make note of what it is. You will be asked to enter it. Otherwise, the script should do the rest of the work for you!
echo.

start /wait "" "!OpenPanda3DInstallerPath!"

echo Finished installing "!OpenPanda3DInstallerExecutableName!".
echo.

timeout /t 5 /nobreak > nul

if exist "!OpenPanda3DInstallerPath!" (
    del "!OpenPanda3DInstallerPath!"
    echo Deleted the "!OpenPanda3DInstallerExecutableName!" file.
    echo.
)

if exist "%DefaultPanda3DPath%" (
    set "ENTERED_PYTHON_PATH=%DefaultPanda3DPath%"
    goto :set_custom_python_path_functionality_textless
) else (
    :set_custom_python_path
)

:ensure_panda3d_directory

cd /d "%ROOT_DIR%"

if exist "%SYMBOLIC_PANDA3D_PATH%" (
    echo Found the "SYMBOLIC_PANDA3D_PATH" file at %SYMBOLIC_PANDA3D_PATH%
    echo.
    set "CUSTOM_AS_PYTHON_PATH=%SYMBOLIC_PANDA3D_PATH%"
    set "INPUT_AS_PYTHON_PATH=%SYMBOLIC_PANDA3D_PATH%"
    goto :question_userInput_existence
) else (
    echo Could not find the "SYMBOLIC_PANDA3D_PATH" file at %SYMBOLIC_PANDA3D_PATH%
    echo.
    goto :doesNotExistPythonPath
)

:pip_check

"%CUSTOM_AS_PYTHON_PATH%" -m pip --version >nul 2>&1

if %ERRORLEVEL% equ 0 (
    echo Pip is installed.
    echo.
    goto :launcher
) else (
    echo Pip not installed. Please wait while I download the latest version of Pip...
    echo.
    cd /d "!PackageDependencies!"
    if exist "%GET_PIP%" (
        del "%GET_PIP%"
    )

    call curl %GetPipWeb% -o %GET_PIP%

    if %ERRORLEVEL% equ 0 (
        echo Download successful!exclaimStr! Running installation script...
        echo.
        cd /d "!ROOT_DIR!"
        "%CUSTOM_AS_PYTHON_PATH%" "!getPipPackageDependencies!"
        if %ERRORLEVEL% equ 0 (
            echo Successfully installed Pip!exclaimStr!
            echo.
            cd /d "!PackageDependencies!"
            del "%GET_PIP%"
            cd /d "!ROOT_DIR!"
        ) else (
            echo Failed to install Pip. Please make sure Open-Panda is installed and Open-Panda3D's Python in the PATH.
            echo.
        )
    ) else (
        echo Failed to download %GET_PIP%. Please check your internet connection or try again later.
        echo.
    )
    goto :install_pip_packages
)

:install_pip_packages

cd /d "%ROOT_DIR%"

if exist "%RequirementsInPath%" (
    if exist "%RequirementsTXTPath%" (
        echo Found the "%RequirementsTXT%"
        echo.
        del "%RequirementsTXT%"
        goto :install_pip_packages
    ) else (
        echo Installing "pip-tools"
        echo.
        "%CUSTOM_AS_PYTHON_PATH%" -m pip install "pip-tools"
        echo Compiling the %RequirementsIn% into a %RequirementsTXT% file.
        echo.
        pip-compile %RequirementsIn%
        echo Installing the contents of the %RequirementsTXT% file.
        echo.
        "%CUSTOM_AS_PYTHON_PATH%" -m pip install -r %RequirementsTXT%
        echo.
        goto :file_cleanup
    ) 
) else (
    echo Could not find the %RequirementsInPath% file... Downloading the fallback from Arbitrium Studios.
    echo.
    call curl %RequirementsInDownload% -o %RequirementsIn%
    echo.
    goto :install_pip_packages
)

goto :file_cleanup

:file_cleanup

if exist "!OpenPanda3DInstallerPath!" (
    del "!OpenPanda3DInstallerPath!"
)

if exist "!getPipPackageDependencies!" (
    del "!getPipPackageDependencies!"
)

goto :ending

:launcher

if "%CD%" NEQ "!ROOT_DIR!" (
    cd /d "!ROOT_DIR!"
)

if "%projectAbbreviation%" == "TSB" (
    if exist "!LAUNCHER_PATH!" (
        echo Starting !projectNameFull!
        echo.
        call "!LAUNCHER_PATH!"
        goto :ending
    )
) else if "%projectAbbreviation%" == "TTFan" (
    echo Launching Astron...
    if exist "!ASTRON_PATH!" (
        start "" "!ASTRON_PATH!"
    )

    echo Launching the Uberdog Server...
    if exist "!UBERDOG_PATH!" (
        start "" "!UBERDOG_PATH!"
    )

    echo Launching the AI Server...
    if exist "!AI_PATH!" (
        start "" "!AI_PATH!"
    )

    timeout /t 3 /nobreak > nul

    echo Launching the game client...
    echo.

    if exist "!LAUNCHER_PATH!" (
        call "!LAUNCHER_PATH!"
        goto :ending
    ) else (
        goto :unsupported
    )
) else (
    goto :unsupported
)

goto :ending

:unsupported

echo The selected project abbreviation is not supported: %projectAbbreviation%
echo.
goto :ending

:ending

pause
cls
goto :launcher
endlocal