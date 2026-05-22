@echo off

:root

SetLocal DisableDelayedExpansion

:: Placing any variables here allows for them to placed as is.
:: The placement of variables such as "exclaimStr" here allows exclamation points...
:: ...to be used in echos by surrounding the variable in exclamation points like the following:
:: !exclaimStr!
set "exclaimStr=!"

SetLocal EnableDelayedExpansion

set "projectOwnerName=PLAYER ZER0 STUDIO"
set "projectName=Toontown Fantasy"
set "projectNameFull=!projectOwnerName!'s !projectName!"
title Launching !projectNameFull!'s Standalone Launcher
set "projectAbbreviation=TTFan"
set "projectAbbreviationUpper=TTFAN"
set "wantToClearLogs=False"

set "PREVIOUS_DIR=..\"

set "ROOT_DIR=%~dp0"
set "ROOT_DIR=%ROOT_DIR:~0,-1%"

if "%CD%" NEQ "%ROOT_DIR%" (
    cd /d "%ROOT_DIR%"
)

set "SCRIPTS_PATH=%ROOT_DIR%\scripts"
set "SCRIPTS_DIR=scripts"
set "STARTUP_DIR=startup"
set "STARTUP_WIN_DIR=windows"
set "STARTUP_PATH=%ROOT_DIR%\%STARTUP_DIR%\%STARTUP_WIN_DIR%"
set "ASTRON_PATH=!STARTUP_PATH!\start_astron_server.bat"
set "UBERDOG_PATH=!STARTUP_PATH!\start_uberdog_server.bat"
set "AI_PATH=!STARTUP_PATH!\start_toon_valley_ai_server.bat"

echo ---------------------------------------------------------------------------------------
echo              Starting !projectNameFull!!exclaimStr!
echo ---------------------------------------------------------------------------------------
echo.

echo The %projectNameFull%'s Abbreviation is set to "%projectAbbreviation%"
echo.

if "%ROOT_DIR%" EQU "%CD%" (
    echo The Current and Root Directories are set to: "%CD%"
    echo.
) else (
    echo Current Directory is %CD%
    echo.

    echo Root Directory is "%ROOT_DIR%"
    echo.
)

set "GetPipWeb=https://bootstrap.pypa.io/get-pip.py"
set "GET_PIP=get-pip.py"

set "PackageDependencies=%ROOT_DIR%\dependencies\packages"
set "getPipPackageDependencies=%ROOT_DIR%\dependencies\packages\%GET_PIP%"
set "PANDA3D_TYPE=Open-Panda"
set "PANDA3D_TYPE_FULL=!PANDA3D_TYPE!3D"

set "RequirementsIn=requirements.in"
set "RequirementsTXT=requirements.txt"
set "RequirementsInPath=%ROOT_DIR%\%RequirementsIn%"
set "RequirementsTXTPath=%ROOT_DIR%\%RequirementsTXT%"
set "RequirementsInDownload=https://cdn.arbitriumstudios.com/application_assets/bots/tsb_assets/dependencies/packages/requirements.in"

set "latestVersionOfOpenPanda3D=1.11.2"
set "OP3D_v1.11.1=https://github.com/Arbitrium-Studios/!PANDA3D_TYPE!/releases/download/v1.11.1/!PANDA3D_TYPE!-1.11.1-py3.11-x64.exe"
set "OP3D_v1.11.2=https://github.com/Arbitrium-Studios/!PANDA3D_TYPE!/releases/download/v1.11.2-Pre_Release/!PANDA3D_TYPE_FULL!-1.11.2-py3.13.exe"
set "OpenPanda3DInstallerExecutableName=!PANDA3D_TYPE_FULL!-!latestVersionOfOpenPanda3D!-py3.13.!Executable!"
set "LatestOfficialOpenPanda3DInstaller=https://github.com/Arbitrium-Studios/!PANDA3D_TYPE!/releases/download/v!latestVersionOfOpenPanda3D!-Pre_Release/!OpenPanda3DInstallerExecutableName!"

set "pythonPathFileName=PYTHON_PATH"
set "PYTHON_PATH_FILE=%ROOT_DIR%\%pythonPathFileName%"
set "PPYTHON_PATH_FILE=%ROOT_DIR%\P%pythonPathFileName%"

set "DEPENDENCIES_DIR=dependencies"
set "PANDA3D_DIR=panda3d"

set "pythonInterpreter="
set "pythonName=python"
set "ppythonName=ppython"
set "Executable=exe"
set "PythonExe=%pythonName%.%Executable%"
set "PPythonExe=%ppythonName%.%Executable%"

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
    @REM set /p CUSTOM_PYTHON_PATH=<PYTHON_PATH
    set /P CUSTOM_PYTHON_PATH=<PYTHON_PATH
    @REM goto :python_check
) else if exist "%PPYTHON_PATH_FILE%" (
    set /P CUSTOM_PYTHON_PATH=<PPYTHON_PATH
    echo Python Path is set to %PYTHON_PATH%
    echo.
    @REM goto :python_check
) else (
    echo The PYTHON_PATH file does NOT exist.
    echo.
    goto :set_python_path
    @REM goto :SelectPythonDirectory
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

echo The "CUSTOM_PYTHON_PATH" variable is set to %CUSTOM_PYTHON_PATH%
echo.

if defined AS_PYTHON_PATH (
    if "%projectAbbreviation%" == "TTFan" (
        if exist "%PRESET_PANDA3D_PATH%" (
            if "!PRESET_PANDA3D_PATH:~-10!"=="!PythonExe!" (
                set "REBUILT_PYTHON_PATH=%PRESET_PANDA3D_PATH%"
                echo The "REBUILT_PYTHON_PATH" variable is set to "!REBUILT_PYTHON_PATH!"
                echo.
                goto :setCustomPanda3DPathWithoutRebuilt
            ) else if "!PRESET_PANDA3D_PATH:~-11!"=="!PPythonExe!" (
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
        )
    ) else (
        echo The selected Project Abbreviation is not supported: %projectAbbreviation%
        echo.
        goto :ending
    )
) else (
    if "%projectAbbreviation%" == "TTFan" (
        if exist "%PRESET_PANDA3D_PATH%" (
            echo The "PRESET_PANDA3D_PATH" variable is set to %PRESET_PANDA3D_PATH%.
            echo.
            set "OPEN_PANDA_PATH=%PRESET_PANDA3D_PATH%"
            goto :setCustomPanda3DPath
        )
    ) else (
        echo The selected Project Abbreviation is not supported: %projectAbbreviation%
        echo.
        goto :ending
    )
)

:setCustomPanda3DPath

set "REBUILT_PYTHON_PATH=%OPEN_PANDA_PATH%\python\python.exe"

:setCustomPanda3DPathWithoutRebuilt

if exist %REBUILT_PYTHON_PATH% (
    set "CUSTOM_PYTHON_PATH=%REBUILT_PYTHON_PATH%"

    if "%projectAbbreviation%" == "TTFan" (
        echo The "AS_PYTHON_PATH" variable is not yet defined.
        echo.

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
        echo The selected Project Abbreviation is not supported: %projectAbbreviation%
        echo.
        goto :ending
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

if not "%CUSTOM_PYTHON_PATH%"=="" if not "%REBUILT_PYTHON_PATH%"=="" (
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

echo Current Directory is %CD%
echo.

if "%CUSTOM_AS_PYTHON_PATH%"=="" (
    if not "%AS_PYTHON_PATH%"=="" (
        set "CUSTOM_AS_PYTHON_PATH=%AS_PYTHON_PATH%"
    )
)

echo The "CUSTOM_AS_PYTHON_PATH" variable is set to %CUSTOM_AS_PYTHON_PATH%
echo.

:: Use quotes to handle paths with spaces
set "INPUT_AS_PYTHON_PATH=%CUSTOM_AS_PYTHON_PATH%"

:: Cleans the " character
set "INPUT_AS_PYTHON_PATH=!INPUT_AS_PYTHON_PATH:"=!"

echo The "INPUT_AS_PYTHON_PATH" variable is set to "%INPUT_AS_PYTHON_PATH%"
echo.

if "!INPUT_AS_PYTHON_PATH:~-10!"=="%PythonExe%" (
    echo The following input ends with %PythonExe%: "%INPUT_AS_PYTHON_PATH%"
    echo.
) else if "!INPUT_AS_PYTHON_PATH:~-11!"=="%PPythonExe%" (
    echo The following input ends with %PPythonExe%: "%INPUT_AS_PYTHON_PATH%"
    echo.
) else (
    echo Error: Input does not end with "%PythonExe%" or "%PPythonExe%".
    echo.
)

:question_userInput_existence

:: Check if the specified file exists
if exist "%INPUT_AS_PYTHON_PATH%" (

    echo Success: The file exists at the given directory: %INPUT_AS_PYTHON_PATH%
    echo.

    echo Current Directory is %CD%
    echo.

    cd /d "%ROOT_DIR%"

    echo Current Directory is %CD%
    echo.

    :: Create or update the necessary file
    echo | set /p=""%INPUT_AS_PYTHON_PATH%"" > %pythonPathFileName%

    echo Updated the "%pythonPathFileName%" file to %INPUT_AS_PYTHON_PATH%
    echo.
    goto :create_symbolic_link
) else (
    echo Error: The specified file was not found.
    echo Please check the path and try again.
    echo.
    goto :custom_panda3d_directory
)

:create_symbolic_link

if not exist "%SYMBOLIC_PANDA3D_PATH%" (
    if exist "%INPUT_AS_PYTHON_PATH%" (
        cd /d "%DEPENDENCIES_PATH%"

        mklink /d "%PANDA3D_DIR%" %AS_PYTHON_PATH%

        echo User Input is set to %INPUT_AS_PYTHON_PATH%
        echo.
        cd /d "%ROOT_DIR%"

    ) else (
        echo Error: The specified file was not found.
        echo Please check the path and try again.
        echo.
        goto :custom_panda3d_directory
    )
)

goto :python_check

:NoPythonPathUpdate
echo You chose "No" to updating the program's Python Path.
echo.
goto :python_check

:python_check
if exist "%CUSTOM_AS_PYTHON_PATH%" (
    if "%CUSTOM_AS_PYTHON_PATH%"=="" (
        echo The specified "CUSTOM_AS_PYTHON_PATH" is blank: "%CUSTOM_AS_PYTHON_PATH%"
        echo.
        goto :set_python_path
    ) else (
        echo The specified "CUSTOM_AS_PYTHON_PATH" exists at %CUSTOM_AS_PYTHON_PATH%.
        echo.

        if /i "%CUSTOM_AS_PYTHON_PATH:~-10%"=="python.exe" (
            echo The specified python path exists at "%CUSTOM_AS_PYTHON_PATH%"!exclaimStr!
            echo.

            goto :check_path_in_environment_variables
        ) else if /i "%CUSTOM_AS_PYTHON_PATH:~-11%"=="ppython.exe" (
            echo The specified python path exists at "%CUSTOM_AS_PYTHON_PATH%"!exclaimStr!
            echo.

            goto :check_path_in_environment_variables
        ) else (
            echo The string does NOT end with python.exe
            echo.
            goto :set_python_path
        )
    )
) else (
    echo The "CUSTOM_AS_PYTHON_PATH" variable does not exist...
    echo.
    goto :set_python_path
)

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

if exist "%ENTERED_PYTHON_PATH%" (
    echo The "ENTERED_PYTHON_PATH" variable is set to "%ENTERED_PYTHON_PATH%"
    echo.
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
    if not "!ENTERED_PYTHON_PATH:%%a=!"=="!ENTERED_PYTHON_PATH!" (
        set "foundPanda3DFolder=true"
    )
)

if "!foundPanda3DFolder!"=="true" (
    if exist "%ENTERED_PYTHON_PATH%" (

        if /i "%ENTERED_PYTHON_PATH:~-10%"=="python.exe" (
            set "CUSTOM_AS_PYTHON_PATH=%ENTERED_PYTHON_PATH%"
            echo The specified python path exists at "%CUSTOM_AS_PYTHON_PATH%"!exclaimStr!
            echo.

            goto :ensure_panda3d_directory
        ) else if /i "%ENTERED_PYTHON_PATH:~-11%"=="ppython.exe" (
            set "CUSTOM_AS_PYTHON_PATH=%ENTERED_PYTHON_PATH%"
            echo The specified python path exists at "%CUSTOM_AS_PYTHON_PATH%"!exclaimStr!
            echo.

            goto :ensure_panda3d_directory
        ) else (
            echo The string does NOT end with python.exe
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

set "SELECTED_PYTHON_PATH=%CUSTOM_AS_PYTHON_PATH%"

if defined CUSTOM_AS_PYTHON_PATH (
    echo The variable "CUSTOM_AS_PYTHON_PATH" already exists at: %CUSTOM_AS_PYTHON_PATH%
    echo.
    set "SystemPythonPath=%CUSTOM_AS_PYTHON_PATH%"
    if not defined python (
        setx python "%SystemPythonPath%" /m
        echo The "python" variable has been permanently added to the system variables...
        echo.
    )
    goto :ensure_panda3d_directory
) else (
    echo The "Please check the path and try again." variable is NOT in the environment variables...
    echo.
    setx Please check the path and try again. "%SELECTED_PYTHON_PATH%" /m
    echo The "Please check the path and try again." variable has been permanently added to the system variables...
    echo.
    goto :set_custom_python_path
)

if "%CUSTOM_AS_PYTHON_PATH%" == "%SELECTED_PYTHON_PATH%" (
    echo The "CUSTOM_AS_PYTHON_PATH" system variable and the "SELECTED_PYTHON_PATH" variable are both the same.
    echo.
    echo - Python_Path_Updated Variable: %SELECTED_PYTHON_PATH%
    echo - CUSTOM_AS_PYTHON_PATH Variable: %CUSTOM_AS_PYTHON_PATH%
    echo.
    goto :ensure_panda3d_directory
)

:install_python

if exist "%PackageDependencies%" (
    echo Found the "PackageDependencies" directory at "%PackageDependencies%"
    echo.
    cd /d "%PackageDependencies%"
    set "OpenPanda3DInstallerDirectory="%PackageDependencies%""
    set "OpenPanda3DInstallerPath=%PackageDependencies%\%OpenPanda3DInstallerExecutableName%"
) else (
    echo Unable to locate the "PackageDependencies" directory at "%PackageDependencies%" Setting the install directory to the current directory at "%CD%"
    echo.
    set "OpenPanda3DInstallerDirectory=%CD%"
    set "OpenPanda3DInstallerPath=%CD%\%OpenPanda3DInstallerExecutableName%"
)

echo The directory the Open-Panda3D installer will be downloaded to is "%OpenPanda3DInstallerDirectory%"
echo.

cd /d "%OpenPanda3DInstallerDirectory%"

goto :OpenPanda3DInstaller

:OpenPanda3DInstaller

if not exist "%OpenPanda3DInstallerPath%" (
    call curl %LatestOfficialOpenPanda3DInstaller% -o %OpenPanda3DInstallerExecutableName%
    if %ERRORLEVEL% equ 0 (
        echo Successfully downloaded the installer!exclaimStr! Running installation script...
        echo.
        goto :start_python_installer
    ) else (
        echo Failed to download %GET_PIP%. Please check your internet connection or try again later.
        echo.
        goto :file_cleanup
        goto :ending
    )
) else (
    echo Installer already downloaded in the following directory: "%OpenPanda3DInstallerPath%"
    echo.
    del "%OpenPanda3DInstallerExecutableName%"
    goto :OpenPanda3DInstaller
)

:start_python_installer

echo When you are asked to do so, please make sure the box to add the path to your system environment variables is checked. After the installer has finished, please make sure to restart your computer and re-run this batch file. If the "AS_PYTHON_PATH" variable still cannot be found, try option "#2 - Select Python Path from Windows Path".
echo.
echo If it still doesn't work, re-open this batch and select the "#1 - Enter Custom Python Path" option when prompted.
echo.
echo Before doing anything else, open your file exploreer and navigate to the directory where you installed Panda3D, then enter the python folder, right click on the "python" folder in the navigation bar, left click "Copy Address as Text", then back in the command prompt, press "Control+V" to paste the address (It should look something like this "C:\Open-Panda\python") then add another back slash ("\") then enter "python.exe" (full address should look something like this: "C:\Open-Panda\python\python.exe")
echo.
echo After all of this, if you are still unable to continue, please file a bug report.
echo.

call "%OpenPanda3DInstallerDirectory%\%OpenPanda3DInstallerExecutableName%"

timeout /t 30 /nobreak > nul

pause
goto :ending

:ensure_panda3d_directory

cd /d "%ROOT_DIR%"

echo Current Directory is %CD%
echo.

if exist "%SYMBOLIC_PANDA3D_PATH%" (
    echo Found the "SYMBOLIC_PANDA3D_PATH" file at %SYMBOLIC_PANDA3D_PATH%
    echo.
    set "PANDA3D_PATH=SYMBOLIC_PANDA3D_PATH"
    goto :pip_check
) else (
    echo Could not find the "PANDA3D_PATH" file at %PANDA3D_PATH%
    echo.
    if exist "%DEPENDENCIES_PATH%" (
        cd /d "%DEPENDENCIES_PATH%"
        mklink /d "%PANDA3D_DIR%" "%DefaultPanda3DPath%"
        echo Successfully created a symbolic link between the "%PANDA3D_DIR%" folder and the "%DefaultPanda3DPath%" directory!exclaimStr!
        echo.
        goto :pip_check
    ) else (
        echo Error: Could not find the "DEPENDENCIES_PATH" file at "%DEPENDENCIES_PATH%"
        echo.
        goto :ending
    )
)

:pip_check

"%CUSTOM_AS_PYTHON_PATH%" -m pip --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Pip is installed.
    echo.
    goto :file_cleanup
) else (
    echo Pip not installed. Please wait while I download the latest version of Pip...
    echo.
    cd /d "!PackageDependencies!"
    if exist "%GET_PIP%" (
        del %GET_PIP%
    )

    call curl %GetPipWeb% -o %GET_PIP%
    if %ERRORLEVEL% equ 0 (
        echo Download successful!exclaimStr! Running installation script...
        echo.
        cd /d "!ROOT_DIR!"
        %CUSTOM_AS_PYTHON_PATH% "!getPipPackageDependencies!"
        if %ERRORLEVEL% equ 0 (
            echo Successfully installed Pip!exclaimStr!
            echo.
            cd /d "!PackageDependencies!"
            del %GET_PIP%
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
        del %RequirementsTXT%
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

if exist "%OpenPanda3DInstallerPath%" (
    set "previousDirectory="%CD%""
    cd /d "%OpenPanda3DInstallerPath%"
    del %OpenPanda3DInstallerExecutableName%
    cd /d %previousDirectory%
)

if exist "%getPipPackageDependencies%" (
    set "previousDirectory="%CD%""
    cd /d "%PackageDependencies%"
    del %GET_PIP%
    cd /d "%previousDirectory%"
)

goto :login

:login
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Your Username is your username and does get stored in your source code so beware!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

if not defined !projectAbbreviation!_Username (
    goto :warningEcho

    :setUsername
    set /P TTFan_Username="Username: "
    echo.

    echo.
    set TTFAN_PLAYCOOKIE=%TTFan_Username%

    set "greetingString=Welcome"
    goto :createUsername
) else (
    set TTFAN_PLAYCOOKIE=%TTFan_Username%
    set "greetingString=Welcome back"
    goto :defineUsernameInSystemVariables
)

:warningEcho

echo The Tooniverse needs your help! To take your first step towards the adventure of a lifetime,
echo please enter a username to use with this computer...
echo.
echo Please note that if you clear your user environment variables, you can re-enter your previous username to regain access to your account.
echo.

goto :setUsername

:createUsername

if not defined !projectAbbreviation!_Username (
    setx !projectAbbreviation!_Username "%TTFan_Username%"
    set "TTFAN_LOGIN_TOKEN=%TTFan_Username%"
)

if "%wantToClearLogs%" EQU "True" (
    cls
)

goto :defineUsernameInSystemVariables

:defineUsernameInSystemVariables

set "TTFAN_LOGIN_TOKEN=%TTFan_Username%"

goto :localhost

:localhost
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Starting Localhost!
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

cd /d "!ROOT_DIR!"

echo Launching Astron...
start !ASTRON_PATH!

echo Launching the Uberdog Server...
start !UBERDOG_PATH!

echo Launching the AI Server...
start !AI_PATH!

echo Launching the game client...
echo.

cd /d "%RootPath%"
set TT_GAMESERVER=127.0.0.1

goto :StartGameWithWelcome

:StartGameWithWelcome
if "%wantToClearLogs%" EQU "True" (
    cls
)
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo     %greetingString% to %projectName%, %TTFAN_LOGIN_TOKEN%!
echo            The vast, ever-expanding Tooniverse awaits you...
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo.

:StartGame

title !projectNameFull!
"%CUSTOM_AS_PYTHON_PATH%" -m toontown.launcher.QuickStartLauncher
pause

goto :ending

:ending

pause
cls
endlocal
goto :root