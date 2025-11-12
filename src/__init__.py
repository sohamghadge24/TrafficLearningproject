# src/__init__.py
import os
print("✅ TrafficLearningproject package loaded")

from .config import NUM_AGENTS, MAX_STEPS_PER_EPISODE, DEVICE, STATE_DIM, SUMO_CONFIG_FILE

print(f"🔧 Config parameters: NUM_AGENTS={NUM_AGENTS}, MAX_STEPS_PER_EPISODE={MAX_STEPS_PER_EPISODE}, DEVICE={DEVICE}, STATE_DIM={STATE_DIM} , SUMO_CONFIG_FILE ={SUMO_CONFIG_FILE}")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"📁 Base directory set to: {BASE_DIR}")

__all__ = ['env', 'madrl', 'utils']

from .env import *
from .madrl import *
# from .utils import *
print("✅ Submodules imported: env, madrl, utils")

