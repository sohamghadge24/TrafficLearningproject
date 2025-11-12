import os
import time
import numpy as np
import traci
import sumolib
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.config import get_sumo_config_file, STATE_DIM, NUM_AGENTS




class SUMOInterface:
    """
    SUMOInterface
    -------------
    Connects the SUMO traffic simulator with the Multi-Agent Reinforcement Learning environment.

    Features:
        - SUMO startup and shutdown via TraCI
        - Automatic SUMO binary path detection (macOS compatible)
        - State extraction for each traffic light agent
        - Reward and cost computation based on traffic performance
    """

    def __init__(self, sumo_cfg_path=None, gui=False, scenario='medium'):
        if sumo_cfg_path is None:
            sumo_cfg_path = get_sumo_config_file(scenario)
        self.sumo_cfg_path = os.path.abspath(sumo_cfg_path)
        self.gui = gui
        self.route_file = None
        self.tls_ids = []
        self._initialize_metrics()
        self.step_count = 0

        # macOS-specific SUMO binary resolution
        self.sumo_binary = self._find_sumo_binary(gui)
        print(f"[INFO] Using SUMO binary: {self.sumo_binary}")

    # --------------------------------------------------------------------------
    # Binary path resolution
    # --------------------------------------------------------------------------
    def _find_sumo_binary(self, gui=False):
        """Detect SUMO binary path for macOS."""
        try:
            # Try standard SUMO detection
            binary = sumolib.checkBinary('sumo-gui' if gui else 'sumo')
            if os.path.exists(binary):
                return binary
        except Exception:
            pass

        # Try Homebrew + common macOS install locations
        sumo_home = os.environ.get("SUMO_HOME", "")
        candidate_paths = [
            os.path.join(sumo_home, "bin", "sumo-gui" if gui else "sumo"),
            "/opt/homebrew/bin/sumo-gui" if gui else "/opt/homebrew/bin/sumo",
            "/usr/local/bin/sumo-gui" if gui else "/usr/local/bin/sumo",
            "/Applications/sumo-gui.app/Contents/MacOS/sumo-gui" if gui else "/Applications/sumo.app/Contents/MacOS/sumo",
        ]

        for path in candidate_paths:
            if os.path.exists(path):
                return path

        raise FileNotFoundError(
            "SUMO binary not found. Please ensure SUMO is installed via Homebrew or set $SUMO_HOME."
        )

    # --------------------------------------------------------------------------
    # Initialization
    # --------------------------------------------------------------------------
    def _initialize_metrics(self):
        """Initialize global performance metrics."""
        self.total_waiting_time = 0.0
        self.total_vehicles = 0
        self.stopped_vehicles = 0
        self.total_speed = 0.0
        self.step_count = 0

    def update_route_file(self, route_file):
        """Assign a route file for custom traffic demand generation."""
        self.route_file = os.path.abspath(route_file)

    # --------------------------------------------------------------------------
    # SUMO Startup and Shutdown
    # --------------------------------------------------------------------------
    def start(self, seed=None):
        """Start the SUMO simulation."""
        if not os.path.exists(self.sumo_cfg_path):
            raise FileNotFoundError(f"SUMO configuration not found: {self.sumo_cfg_path}")

        sumo_cmd = [
            self.sumo_binary,
            "-c", self.sumo_cfg_path,
            "--step-length", "1.0",
            "--no-step-log", "true",
            "--waiting-time-memory", "1000",
            "--no-warnings", "true",
            "--duration-log.disable", "true",
            "--time-to-teleport", "300",
            "--collision.action", "warn",
            "--emergencydecel.warning-threshold", "4.0",
        ]

        if self.route_file:
            sumo_cmd.extend(["-r", self.route_file])
        if seed is not None:
            sumo_cmd.extend(["--seed", str(seed)])

        print(f"[INFO] Starting SUMO simulation with config: {self.sumo_cfg_path}")
        traci.start(sumo_cmd, label=str(time.time()))
        self.tls_ids = traci.trafficlight.getIDList()
        print(f"[INFO] Detected {len(self.tls_ids)} traffic lights: {self.tls_ids}")

        self._initialize_metrics()

    def end(self):
        """Terminate SUMO safely."""
        try:
            traci.close()
        except Exception as e:
            print(f"[WARN] Error closing TraCI: {e}")

    # --------------------------------------------------------------------------
    # Environment Interaction
    # --------------------------------------------------------------------------
    def apply_action(self, tls_id, action):
        """
        Apply an action to the traffic light. Actions are:
        0 = Stay in current phase
        1 = Switch to next phase
        """
        try:
            if action == 1:  # Switch to next phase
                current_phase = traci.trafficlight.getPhase(tls_id)
                total_phases = len(traci.trafficlight.getAllProgramLogics(tls_id)[0].phases)
                if total_phases > 0:  # Only switch if we have valid phases
                    next_phase = (current_phase + 1) % total_phases
                    traci.trafficlight.setPhase(tls_id, next_phase)
            # For action 0, we do nothing (stay in current phase)
        except Exception as e:
            print(f"[ERROR] Failed to apply action on {tls_id}: {e}")

    def get_state(self, tls_id):
        """Retrieve the state vector S_i(t) for intersection 'tls_id'."""
        try:
            state_features = []
            current_phase = float(traci.trafficlight.getPhase(tls_id))
            state_features.append(current_phase)

            controlled_lanes = traci.trafficlight.getControlledLanes(tls_id)
            approaches = {'N': [], 'S': [], 'E': [], 'W': []}

            for lane in controlled_lanes:
                if lane.endswith('N'):
                    approaches['N'].append(lane)
                elif lane.endswith('S'):
                    approaches['S'].append(lane)
                elif lane.endswith('E'):
                    approaches['E'].append(lane)
                elif lane.endswith('W'):
                    approaches['W'].append(lane)
                else:
                    approaches['N'].append(lane)  # default if unclear

            for direction in ['N', 'S', 'E', 'W']:
                lanes = approaches[direction]
                queue = sum(traci.lane.getLastStepHaltingNumber(l) for l in lanes)
                state_features.append(float(queue))

                total_speed = 0.0
                num_vehicles = 0
                for lane in lanes:
                    speed = traci.lane.getLastStepMeanSpeed(lane)
                    num_veh = traci.lane.getLastStepVehicleNumber(lane)
                    total_speed += speed * num_veh
                    num_vehicles += num_veh

                avg_speed = total_speed / max(1.0, num_vehicles)
                state_features.append(float(avg_speed))

            if len(state_features) < STATE_DIM:
                state_features.extend([0.0] * (STATE_DIM - len(state_features)))

            assert len(state_features) == STATE_DIM, \
                f"Expected state dimension {STATE_DIM}, got {len(state_features)} for TLS {tls_id}"

            return state_features

        except Exception as e:
            print(f"[ERROR] Failed to retrieve state for {tls_id}: {e}")
            return [0.0] * STATE_DIM

    # --------------------------------------------------------------------------
    # Metrics and Reward Calculation
    # --------------------------------------------------------------------------
    def _update_metrics(self):
        """Update internal traffic performance metrics."""
        try:
            vehicles = traci.vehicle.getIDList()
            total_waiting = 0.0
            stopped = 0
            total_speed = 0.0
            current_step_vehicle_count = len(vehicles)

            if current_step_vehicle_count == 0:
                self.step_count += 1
                return

            for vid in vehicles:
                speed = traci.vehicle.getSpeed(vid)
                waiting = traci.vehicle.getWaitingTime(vid)
                total_waiting += waiting
                total_speed += speed
                if speed < 0.1:
                    stopped += 1

            self.total_waiting_time += total_waiting
            self.stopped_vehicles += stopped
            self.total_speed += total_speed
            self.total_vehicles += current_step_vehicle_count
            self.step_count += 1

        except Exception as e:
            print(f"[ERROR] Metric update failed: {e}")

    def get_global_metrics(self):
        """Compute global reward (R) and cost (C)."""
        if self.total_vehicles == 0:
            return 0.0, 0.0

        try:
            avg_wait = self.total_waiting_time / self.total_vehicles
            avg_stop_ratio = self.stopped_vehicles / self.total_vehicles
            avg_speed = self.total_speed / self.total_vehicles

            MAX_SPEED = 13.89  # 50 km/h in m/s
            MAX_WAIT = 60.0    # 60 seconds

            W_norm = np.clip(avg_wait / MAX_WAIT, 0, 10)
            S_norm = np.clip(avg_speed / MAX_SPEED, 0, 1)
            R_norm = np.clip(avg_stop_ratio, 0, 1)

            reward = (2.0 * S_norm) - (1.5 * W_norm) - (1.0 * R_norm)
            cost = R_norm

            if self.step_count >= 100:
                self._initialize_metrics()

            return float(reward), float(cost)

        except Exception as e:
            print(f"[ERROR] Failed to compute metrics: {e}")
            return 0.0, 0.0

    # --------------------------------------------------------------------------
    # Simulation Step
    # --------------------------------------------------------------------------
    def step(self):
        """Advance the SUMO simulation by one step."""
        try:
            traci.simulationStep()
            self._update_metrics()
        except Exception as e:
            print(f"[ERROR] Simulation step failed: {e}")
