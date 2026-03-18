@echo off
title Suno Prompt Hub
echo ====================================
echo   SUNO PROMPT HUB - Starting...
echo ====================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python not found.
        echo Please install Python from https://www.python.org
        echo.
        pause
        exit /b 1
    )
    python3 launch.py
) else (
    python launch.py
)

pause
