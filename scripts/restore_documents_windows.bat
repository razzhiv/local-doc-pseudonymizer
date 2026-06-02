@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
title BeforeSending - restore documents

for %%G in ("%~dp0..") do set "PROJECT_ROOT=%%~fG"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"

cd /d "%PROJECT_ROOT%" || goto fail

if not exist "%PYTHON_EXE%" goto missing_python

"%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" restore_warning
echo(
echo(WARNING: restore uses the local token dictionary.
echo(This dictionary may contain original personal and confidential values.
echo(Do not upload, send, commit or archive this file together with the project.
echo(Continue only if you understand where the dictionary is stored and who can access it.
echo(

if not exist "%PROJECT_ROOT%\output\project_dictionary.json" goto missing_dictionary
if not exist "%PROJECT_ROOT%\to_decode" mkdir "%PROJECT_ROOT%\to_decode"

dir /b "%PROJECT_ROOT%\to_decode\*.docx" >nul 2>nul
if errorlevel 1 goto empty_input

set "CONFIRM="
set /p "CONFIRM=Type RESTORE to continue: "
if /i not "%CONFIRM%"=="RESTORE" goto cancelled

echo(
echo(Running token restoration...
"%PYTHON_EXE%" "%PROJECT_ROOT%\restore_tokens.py"
if errorlevel 1 goto fail

echo(
"%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" restore_done
echo(Done. Restored files are in output\restored\
exit /b 0

:missing_python
echo(Local environment was not found: "%PYTHON_EXE%"
echo(Run scripts\setup_windows.bat first.
exit /b 1

:missing_dictionary
echo(Dictionary was not found: output\project_dictionary.json
echo(Restore requires the matching local dictionary.
exit /b 1

:empty_input
"%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" restore_empty "%PROJECT_ROOT%"
echo(No DOCX files were found in to_decode\ for restoration.
echo(Put the edited tokenized DOCX into "%PROJECT_ROOT%\to_decode"
exit /b 0

:cancelled
"%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" restore_cancelled
echo(Restore cancelled.
exit /b 0

:fail
echo(
echo(ERROR: restore did not complete.
exit /b 1
