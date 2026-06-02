@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
title BeforeSending - synthetic demo

for %%G in ("%~dp0..") do set "PROJECT_ROOT=%%~fG"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "DEMO_ROOT=%PROJECT_ROOT%\output\demo_runtime_%RANDOM%"
set "DEMO_DOCX=%DEMO_ROOT%\input\golden_synthetic_client_matter.docx"

cd /d "%PROJECT_ROOT%" || goto fail

if not exist "%PYTHON_EXE%" goto missing_python

if not exist "%DEMO_ROOT%\input" mkdir "%DEMO_ROOT%\input"

echo(Creating synthetic demo DOCX...
"%PYTHON_EXE%" "%PROJECT_ROOT%\examples\golden_demo\create_demo_docx.py" "%DEMO_DOCX%"
if errorlevel 1 goto fail

echo(
echo(Running demo pseudonymization in an isolated synthetic-only folder...
pushd "%DEMO_ROOT%" || goto fail
"%PYTHON_EXE%" "%PROJECT_ROOT%\pseudonymize.py"
set "DEMO_EXIT=%ERRORLEVEL%"
popd
if not "%DEMO_EXIT%"=="0" goto fail

if not exist "%DEMO_ROOT%\output\reports\review_report_latest.html" goto done
if not exist "%PROJECT_ROOT%\review" mkdir "%PROJECT_ROOT%\review"
copy /Y "%DEMO_ROOT%\output\reports\review_report_latest.html" "%PROJECT_ROOT%\review\demo_review_report_latest.html" >nul

:done
echo(
"%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" demo_done "%DEMO_ROOT%" "%PROJECT_ROOT%"
echo(
echo(Demo complete.
echo(These demo artifacts are synthetic and generated locally. They should not be committed.
exit /b 0

:missing_python
echo(Local environment was not found: "%PYTHON_EXE%"
echo(Run scripts\setup_windows.bat first.
exit /b 1

:fail
echo(
echo(ERROR: demo did not complete.
exit /b 1
