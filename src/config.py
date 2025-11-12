import os
import torch

# --- IMPORTANT: Path Configuration ---
# Ensure the path below correctly points to your SUMO configuration file (.sumocfg)
# This path is set relative to this config module so it works regardless of
# the current working directory used to start the script.
import os

def get_sumo_config_file(scenario='medium', city='city4x4'):
    """
    Get the SUMO configuration file path for a given scenario and city.
    Args:
        scenario (str): One of 'low', 'medium', 'high'
        city (str): One of 'city2x2', 'city3x3', 'city4x4', 'city5x5', 'random'
    Returns:
        str: Path to the scenario-specific SUMO config file
    """
    scenario = scenario.lower()
    city = city.lower()
    if scenario not in ['low', 'medium', 'high']:
        scenario = 'medium'
    if city not in ['city2x2', 'city3x3', 'city4x4', 'city5x5', 'random']:
        city = 'city4x4'
    
    # Try new organized structure first
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'scenarios', city, scenario, 'osm.sumocfg')
    
    # Fallback to legacy config if new path doesn't exist
    if not os.path.exists(config_path):
        legacy_path = os.path.join(base_dir, 'scenarios', '4x4_grid', 'osm.sumocfg')
        if os.path.exists(legacy_path):
            return legacy_path
    
    return config_path

# Default to medium traffic scenario
SUMO_CONFIG_FILE = get_sumo_config_file('medium')

if not os.path.exists(SUMO_CONFIG_FILE):
    # Helpful warning only; training will still be able to run in mock mode
    # but real SUMO-based training requires the configuration file to exist.
    print(f"ERROR: SUMO configuration file not found at expected path: {SUMO_CONFIG_FILE}")

NUM_AGENTS = 16          # 4x4 grid -> 16 intersections
STATE_DIM = 12           # [phase, 4 queues, 4 speeds, 3 historical]
ACTION_DIM = 2           # [0=initial phase, 1=next phase]
MAX_STEPS_PER_EPISODE = 3600
SIM_SEED = 42

# --- PPO Hyperparameters ---
LEARNING_RATE_ACTOR = 3e-4
LEARNING_RATE_CRITIC = 1e-3
GAMMA = 0.99             # Discount factor
GAE_LAMBDA = 0.95        # GAE parameter
PPO_EPOCHS = 10          # Number of gradient steps per data collection
CLIP_EPSILON = 0.2       # PPO clipping parameter
BATCH_SIZE = 128
BUFFER_SIZE = 2048       # Size of the PPO buffer (steps collected per update)
MAX_GRAD_NORM = 0.5

# --- Lagrangian Constraints (Safety Layer for C-PPO) ---
COST_LIMIT = 60.0        # Max allowed pedestrian wait time (seconds) - defined as R_norm in your interface.
LAGRANGE_LR = 1e-2       # Learning rate for the Lagrange multiplier
LAGRANGE_INIT = 1.0      # Initial value for lambda
LAGRANGE_MAX = 100.0     # Maximum value for lambda

# --- Training Configuration ---
TOTAL_EPISODES = 200
SAVE_FREQ = 20
EVAL_FREQ = 50
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Directory Configuration ---
LOG_DIR = "logs/tensorboard"
MODEL_DIR = "models"
METRICS_PATH = "logs/metrics.json"
BASELINE_RESULTS_PATH = "logs/baseline_results.csv"

# Create directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

print(f"✅ Configuration loaded: {NUM_AGENTS} agents, device={DEVICE}")