@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
title BeforeSending - prepare documents

for %%G in ("%~dp0..") do set "PROJECT_ROOT=%%~fG"
set "PYTHON_EXE=%PROJECT_ROOT%\.venv\Scripts\python.exe"

cd /d "%PROJECT_ROOT%" || goto fail

if not exist "%PYTHON_EXE%" goto missing_python

for %%G in (input output review to_decode feedback) do if not exist "%PROJECT_ROOT%\%%G" mkdir "%PROJECT_ROOT%\%%G"

dir /b "%PROJECT_ROOT%\input\*.docx" "%PROJECT_ROOT%\input\*.pdf" >nul 2>nul
if errorlevel 1 goto empty_input

echo(Running local pseudonymization for documents from input\...
echo(
"%PYTHON_EXE%" "%PROJECT_ROOT%\pseudonymize.py"
if errorlevel 1 goto fail

if not exist "%PROJECT_ROOT%\output\reports\review_report_latest.html" goto done
if not exist "%PROJECT_ROOT%\review" mkdir "%PROJECT_ROOT%\review"
copy /Y "%PROJECT_ROOT%\output\reports\review_report_latest.html" "%PROJECT_ROOT%\review\review_report_latest.html" >nul

:done
echo(
"%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" prepare_done
echo(
echo(Done.
echo(Check these files:
echo(- output\anonymized\
echo(- output\anonymization_report.json
echo(- output\anonymization_report.docx
echo(- review\review_report_latest.html
echo(- output\reports\review_report_latest.html
echo(
echo(IMPORTANT: this is a risk-reduction tool, not a guarantee of complete anonymization.
echo(Always review the result manually before sharing documents.
exit /b 0

:empty_input
"%PYTHON_EXE%" "%PROJECT_ROOT%\scripts\windows_messages.py" prepare_empty "%PROJECT_ROOT%"
echo(
echo(No DOCX or text-layer PDF files were found in input\.
echo(Put documents into "%PROJECT_ROOT%\input"
echo(Then run scripts\prepare_documents_windows.bat again.
echo(Supported now: DOCX and PDFs with a text layer. Scanned PDFs/images need OCR, which is not included.
exit /b 0

:missing_python
echo(Local environment was not found: "%PYTHON_EXE%"
echo(Run scripts\setup_windows.bat first.
exit /b 1

:fail
echo(
echo(ERROR: document preparation did not complete.
exit /b 1
