@echo off
cd my_daily_brief

set VENV_NAME=venv_windows

if not exist %VENV_NAME% (
    echo Creating virtual environment: %VENV_NAME%...
    python -m venv %VENV_NAME%
)

call %VENV_NAME%\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Starting My Daily Brief...
streamlit run app.py
pause
