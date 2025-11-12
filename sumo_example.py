import os
import sys
import traci

# Make sure SUMO_HOME is set
if "SUMO_HOME" not in os.environ:
    os.environ["SUMO_HOME"] = "/opt/homebrew/opt/sumo@1.19.0/share/sumo"  # Change if different

# Add SUMO tools to the Python path
tools = os.path.join(os.environ["SUMO_HOME"], "tools")
sys.path.append(tools)

# Path to your SUMO configuration file
sumo_cfg = "/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src/scenarios/4x4_grid/osm.sumocfg"

# Choose SUMO binary: sumo or sumo-gui
sumo_binary = "sumo"  # Use "sumo-gui" if you want to see the GUI

def run_sumo_example():
    print("[INFO] Starting SUMO simulation...")
    traci.start([sumo_binary, "-c", sumo_cfg])

    step = 0
    try:
        while step < 10:  # Run 10 simulation steps
            traci.simulationStep()
            vehicle_ids = traci.vehicle.getIDList()
            print(f"Step {step}: Vehicles in the simulation: {vehicle_ids}")
            step += 1
    except traci.exceptions.FatalTraCIError as e:
        print(f"[ERROR] SUMO connection failed: {e}")
    finally:
        traci.close()
        print("[INFO] SUMO simulation ended.")

if __name__ == "__main__":
    run_sumo_example()
