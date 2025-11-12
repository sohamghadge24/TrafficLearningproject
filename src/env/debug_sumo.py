import os
import sys
import traci
import sumolib

def debug_sumo_setup():
    """Debug SUMO configuration and setup."""
    
    # 1. Check SUMO_HOME
    sumo_home = os.environ.get('SUMO_HOME')
    print(f"\n1. SUMO_HOME environment variable: {sumo_home}")
    
    # 2. Check for SUMO binary
    try:
        sumo_bin = sumolib.checkBinary('sumo')
        sumo_gui_bin = sumolib.checkBinary('sumo-gui')
        print(f"\n2. SUMO binaries found:")
        print(f"   sumo: {sumo_bin}")
        print(f"   sumo-gui: {sumo_gui_bin}")
    except Exception as e:
        print(f"\n2. Error finding SUMO binaries: {e}")
    
    # 3. Locate config file
    cfg_path = "/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src/scenarios/4x4_grid/osm.sumocfg"
    print(f"\n3. Checking SUMO config file: {cfg_path}")
    print(f"   Exists: {os.path.exists(cfg_path)}")
    
    if os.path.exists(cfg_path):
        # 4. Try to start SUMO
        print("\n4. Attempting to start SUMO...")
        try:
            cmd = [sumo_bin, 
                   "-c", cfg_path,
                   "--no-step-log", "true",
                   "--no-warnings", "true"]
            
            traci.start(cmd)
            
            # Get traffic light info
            tls_ids = traci.trafficlight.getIDList()
            print(f"\n5. Traffic lights found: {len(tls_ids)}")
            for tls in tls_ids:
                print(f"   TLS ID: {tls}")
                print(f"   - Controlled lanes: {traci.trafficlight.getControlledLanes(tls)}")
                print(f"   - Programs: {traci.trafficlight.getCompleteRedYellowGreenDefinition(tls)}")
                print(f"   - Current phase: {traci.trafficlight.getPhase(tls)}")
            
            # Test one simulation step
            print("\n6. Testing simulation step...")
            traci.simulationStep()
            
            # Get vehicle info
            vehicles = traci.vehicle.getIDList()
            print(f"\n7. Vehicles in simulation: {len(vehicles)}")
            for v in vehicles[:5]:  # Show first 5 vehicles only
                print(f"   Vehicle {v}:")
                print(f"   - Speed: {traci.vehicle.getSpeed(v):.2f} m/s")
                print(f"   - Waiting time: {traci.vehicle.getWaitingTime(v):.2f} s")
            
            traci.close()
            print("\nSUMO test completed successfully!")
            
        except Exception as e:
            print(f"\nError during SUMO test: {e}")
            if 'traci' in sys.modules and traci.isConnected():
                traci.close()

if __name__ == "__main__":
    debug_sumo_setup()