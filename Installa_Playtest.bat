@echo off
setlocal
cd /d "%~dp0"
echo ======================================
echo   NFT Single Player - Installazione
echo ======================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (
    py -m pip install -r requirements-playtest.txt
) else (
    python -m pip install -r requirements-playtest.txt
)
if errorlevel 1 (
    echo.
    echo Installazione non riuscita.
    pause
    exit /b 1
)
echo.
echo Installazione completata. Ora avvia Avvia_Playtest.bat
pause
