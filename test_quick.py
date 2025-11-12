#!/usr/bin/env python3
"""Quick test to verify SUMO configs work"""
import sys
import os

# Add paths
src_dir = '/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src'
sys.path.insert(0, src_dir)

from config import get_sumo_config_file
from env.traffic_env import TrafficEnv

print("🔧 Testing SUMO Configuration...")
cfg = get_sumo_config_file('medium', 'city4x4')
print(f"Config path: {cfg}")
print(f"Config exists: {os.path.exists(cfg)}")

print("\n🏗️  Creating TrafficEnv...")
try:
    env = TrafficEnv(gui=False, use_sumo=True, scenario='medium')
    print("✅ TrafficEnv created")
except Exception as e:
    print(f"❌ Failed to create TrafficEnv: {e}")
    sys.exit(1)

print("\n🔄 Resetting environment...")
try:
    states = env.reset(seed=42, scenario='medium')
    print(f"✅ Environment reset successfully")
    print(f"   States shape: {states.shape}")
    print(f"   Num agents: {env.num_agents}")
except Exception as e:
    print(f"❌ Failed to reset environment: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ ALL TESTS PASSED")
env.close()
