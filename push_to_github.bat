@echo off
title Push AI Smart Healthcare to GitHub
cd /d "C:\Users\user\.gemini\antigravity\scratch\AI-smart-healthcare"
echo Pushing commits to GitHub...
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo SUCCESS! Project successfully pushed to GitHub!
    echo https://github.com/sbharath1332007/AI-smart-healthcare
    echo ========================================================
) else (
    echo Push encountered an issue. Check your connection or GitHub credentials.
)
pause
