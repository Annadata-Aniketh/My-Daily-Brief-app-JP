#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/my_daily_brief"

# Name of the virtual environment
VENV_NAME="venv_macos"

# check if venv exists
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment: $VENV_NAME..."
    python3 -m venv "$VENV_NAME"
    
    # Activate and install requirements
    source "$VENV_NAME/bin/activate"
    echo "Installing dependencies... (this may take a minute)"
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "Warning: requirements.txt not found!"
    fi
else
    source "$VENV_NAME/bin/activate"
fi

# Function to wait for the port and then open the browser
(
    # Wait for up to 15 seconds for port 8501 to become available
    for i in {1..15}; do
        if nc -z localhost 8501 2>/dev/null; then
            open "http://localhost:8501"
            exit 0
        fi
        sleep 1
    done
    echo "Timed out waiting for Streamlit to start."
) &

# Run the app
echo "Starting My Daily Brief..."
streamlit run app.py
