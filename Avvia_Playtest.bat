@echo off
setlocal
cd /d "%~dp0"
echo ======================================
echo   NFT Single Player - Playtest
echo ======================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (
    py playtest_web.py
) else (
    python playtest_web.py
)
if errorlevel 1 (
    echo.
    echo Se compare un errore di dipendenze, esegui prima Installa_Playtest.bat
    pause
)
