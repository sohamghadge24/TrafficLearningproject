# 4x4 Grid Scenarios

This folder contains traffic scenarios for the SUMO traffic simulation on a 4x4 grid network.

## Folder Structure

```
4x4_grid/
├── low/                           # Low traffic scenario
│   └── low_traffic.sumocfg
├── medium/                        # Medium traffic scenario
│   └── medium_traffic.sumocfg
├── high/                          # High traffic scenario
│   └── high_traffic.sumocfg
├── routes/                        # Route files for different traffic densities
│   ├── low_traffic.rou.xml
│   ├── medium_traffic.rou.xml
│   ├── high_traffic.rou.xml
│   ├── osm.passenger.rou.xml
│   └── ...
├── osm.net.xml.gz               # Network topology (compressed)
├── osm.poly.xml.gz              # Polygon definitions (compressed)
├── output.add.xml               # Additional output definitions
├── osm.view.xml                 # View settings for GUI
├── osm.sumocfg                  # Main configuration (legacy)
└── ... (other supporting files)
```

## Traffic Scenarios

### Low Traffic (`low/low_traffic.sumocfg`)
- Uses `routes/low_traffic.rou.xml` 
- Sparse vehicle distribution
- Good for testing basic control strategies
- Period: 10.0 seconds between vehicle departures (fringe-factor: 5)

### Medium Traffic (`medium/medium_traffic.sumocfg`)
- Uses `routes/medium_traffic.rou.xml`
- Moderate vehicle density
- Typical scenario for training
- Balanced congestion levels

### High Traffic (`high/high_traffic.sumocfg`)
- Uses `routes/high_traffic.rou.xml`
- Dense vehicle distribution
- Challenging control scenarios
- High congestion periods

## Usage

### In Python (with TraCI)

```python
from pathlib import Path

# Specify the scenario
scenario = 'medium'  # 'low', 'medium', or 'high'
config_file = f"src/scenarios/4x4_grid/{scenario}/{scenario}_traffic.sumocfg"

# Start SUMO with TraCI
import sumolib
import traci

sumo_binary = sumolib.checkBinary('sumo')
traci.start([sumo_binary, '-c', config_file])

# ... simulation code ...

traci.close()
```

### Command Line

```bash
# Low traffic
sumo -c src/scenarios/4x4_grid/low/low_traffic.sumocfg

# Medium traffic
sumo -c src/scenarios/4x4_grid/medium/medium_traffic.sumocfg

# High traffic
sumo -c src/scenarios/4x4_grid/high/high_traffic.sumocfg

# With GUI
sumo-gui -c src/scenarios/4x4_grid/medium/medium_traffic.sumocfg
```

## Configuration Details

Each scenario configuration includes:

- **Network**: `osm.net.xml.gz` - Real-world OSM-based 4x4 grid network
- **Routes**: Traffic demand defined in corresponding `.rou.xml` file
- **Additionals**: 
  - `osm.poly.xml.gz` - Building polygons
  - `output.add.xml` - Output detectors and data collectors
- **Simulation Time**: 0-3600 seconds (1 hour)
- **Traffic Light Control**: Actuated control with jam threshold of 30 vehicles

## Output Files

When running a scenario, the following files are generated in the respective scenario folder:

- `tripinfos.xml` - Trip information (arrival, departure, duration, etc.)
- `stats.xml` - Overall simulation statistics

## Network Details

- **Grid**: 4x4 intersections (real-world coordinates from OSM)
- **Traffic Lights**: One at each intersection with automatic phase control
- **Vehicle Types**: Default SUMO passenger cars
- **Rerouting**: Enabled with 18-step adaptation interval

## Notes

- Route files were generated using SUMO's `randomTrips.py` tool
- Relative paths in config files assume script execution from project root
- All route files use the same network topology but different traffic demand profiles
- See `routes/` folder for additional route file variants
