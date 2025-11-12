#!/bin/bash
# Run the Traffic MADRL Agent with proper environment setup

PROJECT_ROOT="/Users/sohamghadge/Documents/Final_Project"
VENV_PATH="$PROJECT_ROOT/.venv"
SRC_DIR="$PROJECT_ROOT/TrafficLearningproject/src"

echo "🚀 Starting Traffic MADRL Agent..."
echo "=================================="

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    echo "Please create it first: python3 -m venv $VENV_PATH"
    exit 1
fi

# Activate venv and run
cd "$SRC_DIR"
source "$VENV_PATH/bin/activate"

echo "✅ Virtual environment activated"
echo "📁 Working directory: $(pwd)"
echo "🐍 Python: $(which python)"
echo ""
echo "Starting training..."
echo "=================================="
echo ""

python main.py

# Capture exit code
EXIT_CODE=$?

echo ""
echo "=================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Training completed successfully!"
else
    echo "❌ Training failed with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
