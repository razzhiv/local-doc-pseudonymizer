@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
title BeforeSending - Windows setup

for %%G in ("%~dp0..") do set "PROJECT_ROOT=%%~fG"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"

cd /d "%PROJECT_ROOT%" || goto fail

echo(BeforeSending Windows setup
echo(This is a local setup script, not a system-wide app install.
echo(
echo(This creates the local environment and runtime folders.
echo(

if exist "%PYTHON_EXE%" goto have_python

echo(.venv was not found. Creating a local virtual environment...
py -3 -m venv "%PROJECT_ROOT%\.venv"
if not errorlevel 1 goto have_python

echo(Could not run py -3. Trying python...
python -m venv "%PROJECT_ROOT%\.venv"
if errorlevel 1 goto fail

:have_python
if not exist "%PYTHON_EXE%" goto missing_python

echo(Installing Python dependencies into local .venv from requirements.txt...
"%PYTHON_EXE%" -m pip install -r "%PROJECT_ROOT%\requirements.txt"
if errorlevel 1 goto fail

for %%G in (input output review to_decode feedback) do if not exist "%PROJECT_ROOT%\%%G" mkdir "%PROJECT_ROOT%\%%G"

echo(
"%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" setup_done "%PROJECT_ROOT%"
echo(
echo(Done. Setup does not process documents.
echo(Next steps:
echo(1. Put DOCX or text-layer PDF files into "%PROJECT_ROOT%\input"
echo(2. Run scripts\prepare_documents_windows.bat
echo(3. Review output\ and the local HTML report in review\
echo(4. Use scripts\restore_documents_windows.bat only when restoration is needed
exit /b 0

:missing_python
echo(
echo(Python was not found inside .venv: "%PYTHON_EXE%"
goto fail

:fail
echo(
echo(ERROR: setup did not complete.
echo(Make sure Python 3 is installed and available as py or python.
exit /b 1
