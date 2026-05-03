@echo off
chcp 65001 > nul
title BeforeSending - pseudonymize documents

python pseudonymize.py

echo.
pause
