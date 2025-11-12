#!/usr/bin/env python3
"""
Quick test of main.py with 100 episodes to verify the full pipeline works.
"""
import sys
import os

# Set working directory and paths
src_dir = '/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src'
sys.path.insert(0, src_dir)
os.chdir(src_dir)

# Temporarily override config for faster testing
import config
config.TOTAL_EPISODES = 100
config.MAX_STEPS_PER_EPISODE = 100  # Much shorter for quick test

print(f"Quick test configuration:")
print(f"  TOTAL_EPISODES: {config.TOTAL_EPISODES}")
print(f"  MAX_STEPS_PER_EPISODE: {config.MAX_STEPS_PER_EPISODE}")

# Now run main
from main import run_training

try:
    run_training()
    print("\n✅ Training completed successfully!")
except KeyboardInterrupt:
    print("\n⚠️ Training interrupted by user.")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
