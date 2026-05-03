@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo === AFTER ANONYMIZE REVIEW ===
echo.

echo Создаю review-summary...
python build_review_summary.py

echo.
echo Создаю Excel-review...
python review_tool.py export

echo.
echo Готово.
echo Откройте файл:
echo review\review_cases.xlsx
echo.
pause