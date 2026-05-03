@echo off
chcp 65001 > nul
title BeforeSending - restore tokens

python restore_tokens.py

echo.
pause
