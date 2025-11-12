#!/bin/bash

# Reset Environment Script for Traffic MADRL Project
# This script resets all processes, caches, and temporary files

echo "════════════════════════════════════════════════════════════════"
echo "🔄 RESETTING TRAFFIC MADRL ENVIRONMENT"
echo "════════════════════════════════════════════════════════════════"

PROJECT_ROOT="/Users/sohamghadge/Documents/Final_Project"
cd "$PROJECT_ROOT" || exit 1

# Step 1: Kill any running processes
echo "⏹️  Stopping any running processes..."
pkill -f sumo 2>/dev/null
pkill -f "python.*main" 2>/dev/null
pkill -f "python.*test" 2>/dev/null
pkill -f "python.*run" 2>/dev/null
sleep 2
echo "   ✅ Processes stopped"

# Step 2: Clear Python cache
echo "🧹 Clearing Python cache..."
find "$PROJECT_ROOT" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null
find "$PROJECT_ROOT" -type f -name ".pytest_cache" -delete 2>/dev/null
echo "   ✅ Cache cleared"

# Step 3: Reset log and model directories
echo "📁 Resetting directories..."
rm -rf "$PROJECT_ROOT/TrafficLearningproject/src/logs/tensorboard"/* 2>/dev/null
mkdir -p "$PROJECT_ROOT/TrafficLearningproject/src/logs/tensorboard"
rm -f "$PROJECT_ROOT/TrafficLearningproject/src/logs/metrics.json" 2>/dev/null
rm -f "$PROJECT_ROOT/logs/metrics.json" 2>/dev/null
echo "   ✅ Directories reset"

# Step 4: Verify virtual environment
echo "🐍 Verifying virtual environment..."
if [ -f "$PROJECT_ROOT/.venv/bin/python3" ]; then
    PYTHON_VER=$("$PROJECT_ROOT/.venv/bin/python3" --version 2>&1)
    echo "   ✅ Virtual environment active: $PYTHON_VER"
else
    echo "   ⚠️  Virtual environment not found!"
    exit 1
fi

# Step 5: Verify key files exist
echo "📋 Verifying key files..."
FILES=(
    "$PROJECT_ROOT/TrafficLearningproject/src/main.py"
    "$PROJECT_ROOT/TrafficLearningproject/src/config.py"
    "$PROJECT_ROOT/TrafficLearningproject/src/traffic_env.py"
    "$PROJECT_ROOT/TrafficLearningproject/src/scenarios/4x4_grid/osm.net.xml.gz"
    "$PROJECT_ROOT/run_agent.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $(basename "$file")"
    else
        echo "   ❌ Missing: $file"
    fi
done

# Step 6: Final status
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ ENVIRONMENT RESET COMPLETE"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Ready to run:"
echo "  cd /Users/sohamghadge/Documents/Final_Project"
echo "  python3 run_agent.py"
echo ""
