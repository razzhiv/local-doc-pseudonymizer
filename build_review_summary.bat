@echo off

cd /d "%~dp0"

if exist "build_review_summary.py" (
    python build_review_summary.py
    pause
    exit /b
)

if exist "..\build_review_summary.py" (
    cd ..
    python build_review_summary.py
    pause
    exit /b
)

echo Не найден build_review_summary.py.
echo Положите этот bat в корень проекта рядом с build_review_summary.py или в папку review.
pause
