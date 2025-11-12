#!/bin/bash
# Checks SUMO_HOME and then navigates to the scenario directory to generate all traffic levels.

# --- PATH & VALIDATION CHECK ---
# Check if SUMO_HOME is set (Required for finding tools reliably)
if [ -z "$SUMO_HOME" ]; then
    echo "❌ Error: The SUMO_HOME environment variable is not set."
    echo "Please set SUMO_HOME to your SUMO installation directory before running."
    exit 1
fi

# Use SUMO_HOME to find the tool reliably
RANDOM_TRIPS_SCRIPT="$SUMO_HOME/tools/randomTrips.py"

if [ ! -f "$RANDOM_TRIPS_SCRIPT" ]; then
    echo "❌ randomTrips.py not found at expected location: $RANDOM_TRIPS_SCRIPT"
    echo "Please verify that SUMO_HOME is set correctly."
    exit 1
fi
# --- END PATH CHECK ---


# Navigate to the project scenarios directory (as defined in your script)
cd "$(dirname "$0")/src/scenarios/4x4_grid" || exit 1

echo "🚀 Generating traffic route files for SUMO simulation..."
echo "✅ Using randomTrips.py from: $RANDOM_TRIPS_SCRIPT"


# Check if network file exists (now relative to the new CWD)
if [ ! -f "osm.net.xml.gz" ]; then
    echo "❌ Network file osm.net.xml.gz not found!"
    # Change back to original directory before exiting
    cd - > /dev/null
    exit 1
fi
echo "✅ Found network file: osm.net.xml.gz"

# --- GENERATION START ---

# Generate LOW traffic (10s period = ~360 vehicles/hour)
echo ""
echo "📊 Generating LOW traffic scenario..."
python3 "$RANDOM_TRIPS_SCRIPT" \
    -n osm.net.xml.gz \
    -o low_traffic.rou.xml \
    -e 3600 \
    -p 10 \
    --seed 42 \
    --fringe-factor 5 \
    --validate
if [ $? -eq 0 ]; then
    echo "✅ low_traffic.rou.xml generated successfully"
else
    echo "❌ Failed to generate low_traffic.rou.xml"
fi

# Generate MEDIUM traffic (3.6s period = ~1000 vehicles/hour)
echo ""
echo "📊 Generating MEDIUM traffic scenario..."
python3 "$RANDOM_TRIPS_SCRIPT" \
    -n osm.net.xml.gz \
    -o medium_traffic.rou.xml \
    -e 3600 \
    -p 3.6 \
    --seed 42 \
    --fringe-factor 5 \
    --validate
if [ $? -eq 0 ]; then
    echo "✅ medium_traffic.rou.xml generated successfully"
else
    echo "❌ Failed to generate medium_traffic.rou.xml"
fi

# Generate HIGH traffic (2s period = ~1800 vehicles/hour)
echo ""
echo "📊 Generating HIGH traffic scenario..."
python3 "$RANDOM_TRIPS_SCRIPT" \
    -n osm.net.xml.gz \
    -o high_traffic.rou.xml \
    -e 3600 \
    -p 2 \
    --seed 42 \
    --fringe-factor 5 \
    --validate
if [ $? -eq 0 ]; then
    echo "✅ high_traffic.rou.xml generated successfully"
else
    echo "❌ Failed to generate high_traffic.rou.xml"
fi

echo ""
echo "🎉 Route generation complete!"
echo ""
echo "Generated files:"
ls -lh *_traffic.rou.xml 2>/dev/null || echo "⚠️  No route files found"

# Change back to original directory
cd - > /dev/null