@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
title BeforeSending - local cleanup

for %%G in ("%~dp0..") do set "PROJECT_ROOT=%%~fG"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"

cd /d "%PROJECT_ROOT%" || goto fail

echo(BeforeSending local cleanup helper
echo(This is not a system uninstaller and not secure deletion.
echo(It removes only generated local environment/runtime folders inside this project copy.
echo(Project root: "%PROJECT_ROOT%"
echo(

if exist "%PYTHON_EXE%" "%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" cleanup_warning "%PROJECT_ROOT%"
echo(
echo(WARNING: local cleanup will remove .venv and runtime folders in this project copy.
echo(This may delete input documents, outputs, reports, token dictionaries and restored files.
echo(This is normal deletion, not secure deletion.
echo(Copies may remain in Recycle Bin, backups, cloud sync, SSD traces or other locations.
echo(To fully remove the tool after cleanup, close all windows and delete the project folder manually.
echo(
echo(The following folders may be removed if they exist:
echo(- .venv
echo(- input
echo(- output
echo(- review
echo(- to_decode
echo(- feedback
echo(- __pycache__
echo(- .pytest_cache
echo(
echo(Source code, docs, scripts, tests, examples, expected, and rules are not deleted by this helper.
echo(

set "CONFIRM="
set /p "CONFIRM=Type CLEANUP to delete generated local folders: "
if /i not "%CONFIRM%"=="CLEANUP" goto cancelled

call :delete_dir ".venv"
if errorlevel 1 goto fail
call :delete_dir "input"
if errorlevel 1 goto fail
call :delete_dir "output"
if errorlevel 1 goto fail
call :delete_dir "review"
if errorlevel 1 goto fail
call :delete_dir "to_decode"
if errorlevel 1 goto fail
call :delete_dir "feedback"
if errorlevel 1 goto fail
call :delete_dir "__pycache__"
if errorlevel 1 goto fail
call :delete_dir ".pytest_cache"
if errorlevel 1 goto fail

echo(
echo(Local cleanup finished.
echo(To fully remove the tool, close all files/windows and delete the project folder manually:
echo("%PROJECT_ROOT%"
echo(This was normal deletion, not secure deletion.
exit /b 0

:delete_dir
set "TARGET_NAME=%~1"
set "TARGET_PATH=%PROJECT_ROOT%\%TARGET_NAME%"
if not exist "%TARGET_PATH%" (
    echo(Skipped: %TARGET_NAME% was not found.
    exit /b 0
)
if "%TARGET_PATH%"=="%PROJECT_ROOT%" (
    echo(ERROR: refusing to delete project root.
    exit /b 1
)
if "%TARGET_NAME%"=="" (
    echo(ERROR: refusing empty cleanup target.
    exit /b 1
)
echo(Deleting: %TARGET_NAME%
rmdir /s /q "%TARGET_PATH%"
if errorlevel 1 (
    echo(ERROR: could not delete %TARGET_NAME%
    exit /b 1
)
exit /b 0

:cancelled
echo(Cleanup cancelled.
exit /b 0

:fail
echo(ERROR: cleanup did not complete.
exit /b 1
