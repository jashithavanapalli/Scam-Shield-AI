@echo off
cd /d "%~dp0"
echo Installing Scam Shield AI dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Package installation failed. Read the error above and check your internet connection and Python installation.
  pause
  exit /b 1
)
echo.
echo Starting Scam Shield AI at http://127.0.0.1:5000
python app.py
pause
