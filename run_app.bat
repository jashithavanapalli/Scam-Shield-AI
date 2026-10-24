@echo off
cd /d "%~dp0"
python app.py
if errorlevel 1 (
  echo.
  echo The application did not start. Install dependencies with:
  echo python -m pip install -r requirements.txt
  pause
)
