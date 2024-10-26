@echo off
setlocal enabledelayedexpansion

echo Support development in an Windows environment
echo.

:: Only for development of this script
::set ONLY_INSTALL_EXTERNAL_DEPENDENCIES_ONCE=
::set ONLY_SETUP_PYTHON_PATH_ONCE=
::set PYTHONPATH=


if defined ONLY_INSTALL_EXTERNAL_DEPENDENCIES_ONCE (
    echo "*** External dependencies alread installed. Skipping this part!"
    echo.
) else (
    set ONLY_INSTALL_EXTERNAL_DEPENDENCIES_ONCE=true

    :: install external dependencies
    python --version
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r windows-support\common-requirements-on-windows.txt --upgrade
)


if defined ONLY_SETUP_PYTHON_PATH_ONCE (
    echo "*** PYTHONPATH already set. Skipping new set!"
    echo.
) else (
    set ONLY_SETUP_PYTHON_PATH_ONCE=true

    :: setup python path to all the components in this repo
    echo ... setup PYTHONPATH
    set PYTHONPATH=!PYTHONPATH!;%cd%\
)

echo.
echo %PYTHONPATH%
echo.
echo ... resulting PYTHONPATH has these individual path
echo.

set "str=!PYTHONPATH!"
set "delimiter=;"
:loop
    for /f "tokens=1* delims=;" %%a in ("!str!") do (
        echo     - %%a
        set "str=%%b"
    )
    if "!str!" NEQ "" goto loop

set transport_to_outside_local=!PYTHONPATH!
endlocal & set PYTHONPATH=%transport_to_outside_local%
