#!/usr/bin/env python3
"""
Run the Traffic MADRL Training Script with proper environment setup.
This script activates the virtual environment and runs main.py with enhanced monitoring.
"""

import subprocess
import sys
import os
import time
from datetime import datetime, timedelta

PROJECT_ROOT = "/Users/sohamghadge/Documents/Final_Project"
VENV_PATH = os.path.join(PROJECT_ROOT, ".venv")
SRC_DIR = os.path.join(PROJECT_ROOT, "TrafficLearningproject", "src")
PYTHON_BIN = os.path.join(VENV_PATH, "bin", "python3")

# Project Configuration
PROJECT_CONFIG = {
    "name": "Traffic MADRL Agent",
    "version": "1.0",
    "description": "Multi-Agent Deep Reinforcement Learning for Traffic Control",
    "framework": "PyTorch + PPO",
    "algorithm": "C-PPO (Constrained PPO with Lagrangian)",
    "agents": 16,
    "network": "4x4 Intersection Grid",
    "action_space": "2 discrete actions (stay/switch phase)",
    "state_space": "12 dimensions (phase + queues + speeds + history)",
    "episodes": 200,
    "steps_per_episode": 3600,
    "device": "CPU",
    "seed": 42
}

def print_header():
    """Print project header with ASCII art."""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + f"{'🚀 TRAFFIC MADRL AGENT - TRAINING LAUNCHER':^78}" + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝\n")

def print_project_info():
    """Print project configuration and details."""
    print("📋 PROJECT CONFIGURATION")
    print("─" * 80)
    
    config_items = [
        ("Project", PROJECT_CONFIG["name"]),
        ("Algorithm", PROJECT_CONFIG["algorithm"]),
        ("Framework", PROJECT_CONFIG["framework"]),
        ("Agents", f"{PROJECT_CONFIG['agents']} traffic light controllers"),
        ("Network", PROJECT_CONFIG["network"]),
        ("Action Space", PROJECT_CONFIG["action_space"]),
        ("State Space", PROJECT_CONFIG["state_space"]),
        ("Episodes", PROJECT_CONFIG["episodes"]),
        ("Steps/Episode", f"{PROJECT_CONFIG['steps_per_episode']:,} (simulation seconds)"),
        ("Device", PROJECT_CONFIG["device"]),
        ("Random Seed", PROJECT_CONFIG["seed"]),
    ]
    
    for label, value in config_items:
        print(f"  {label:.<25} {value}")
    print()

def print_system_check():
    """Check and display system configuration."""
    print("🔍 SYSTEM CHECK")
    print("─" * 80)
    
    checks = []
    
    # Check venv
    venv_ok = os.path.isdir(VENV_PATH)
    checks.append(("Virtual Environment", venv_ok, VENV_PATH))
    
    # Check Python binary
    python_ok = os.path.isfile(PYTHON_BIN)
    checks.append(("Python Binary", python_ok, PYTHON_BIN))
    
    # Check source directory
    src_ok = os.path.isdir(SRC_DIR)
    checks.append(("Source Directory", src_ok, SRC_DIR))
    
    # Check main.py
    main_py = os.path.join(SRC_DIR, "main.py")
    main_ok = os.path.isfile(main_py)
    checks.append(("Main Script", main_ok, main_py))
    
    # Check config.py
    config_py = os.path.join(SRC_DIR, "config.py")
    config_ok = os.path.isfile(config_py)
    checks.append(("Config File", config_ok, config_py))
    
    # Check scenarios
    scenario_files = [
    "/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src/scenarios/city4x4/low/osm.sumocfg",
    "/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src/scenarios/city4x4/medium/osm.sumocfg",
    "/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src/scenarios/city4x4/high/osm.sumocfg",
    "/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src/scenarios/4x4_grid/osm.sumocfg"
]



    for path in scenario_files:
        print(f"{'✅' if os.path.isfile(path) else '❌'} {path}")
    scenarios_dir = os.path.join(SRC_DIR, "scenarios")
    scenarios_ok = all(os.path.isfile(path) for path in scenario_files)
    checks.append(("Scenario Files", scenarios_ok, scenarios_dir))
    
    # Check logs directory
    logs_dir = os.path.join(SRC_DIR, "logs")
    logs_ok = os.path.isdir(logs_dir)
    checks.append(("Logs Directory", logs_ok, logs_dir))
    
    all_ok = all(check[1] for check in checks)
    
    for item, ok, path in checks:
        status = "✅" if ok else "❌"
        print(f"  {status} {item:.<25} {os.path.basename(path)}")
    
    print()
    return all_ok

def print_training_info():
    """Print training information and expected outputs."""
    print("📊 TRAINING INFORMATION")
    print("─" * 80)
    
    total_episodes = PROJECT_CONFIG["episodes"]
    steps_per_episode = PROJECT_CONFIG["steps_per_episode"]
    est_seconds_per_episode = 2  # Approximate
    est_total_seconds = total_episodes * est_seconds_per_episode
    est_total_min = est_total_seconds / 60
    
    print(f"  Total Episodes:      {total_episodes}")
    print(f"  Steps per Episode:   {steps_per_episode:,}")
    print(f"  Estimated Duration:  ~{est_total_min:.0f} minutes ({est_total_min/60:.1f} hours)")
    print()
    
    print("📁 OUTPUT FILES")
    print("  Models:              TrafficLearningproject/src/models/")
    print("    ├─ actor_final.pt")
    print("    ├─ critic_final.pt")
    print("    ├─ actor_best.pt")
    print("    └─ checkpoints/")
    print()
    print("  Metrics:             TrafficLearningproject/src/logs/")
    print("    ├─ metrics.json    (episode-level data)")
    print("    ├─ baseline_results.csv")
    print("    └─ tensorboard/    (interactive graphs)")
    print()

def print_progress_indicator(stage, total_stages):
    """Print progress bar and stage indicator."""
    progress = (stage / total_stages) * 100
    filled = int(progress / 2)
    bar = "█" * filled + "░" * (50 - filled)
    print(f"\n[{bar}] {progress:.0f}% - Stage {stage}/{total_stages}\n")

def main():
    """Main execution function."""
    print_header()
    print_project_info()
    
    # Stage 1: System Check
    print_progress_indicator(1, 5)
    all_ok = print_system_check()
    
    if not all_ok:
        print("❌ System check failed!")
        print("\nMissing components. Please verify your installation.")
        sys.exit(1)
    
    # Stage 2: Preparation
    print_progress_indicator(2, 5)
    print("⚙️  PREPARING TRAINING ENVIRONMENT")
    print("─" * 80)
    print(f"  Timestamp:           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Working Directory:   {SRC_DIR}")
    print(f"  Python Executable:   {PYTHON_BIN}")
    print()
    
    # Stage 3: Starting training
    print_progress_indicator(3, 5)
    print("🚀 STARTING TRAINING")
    print("─" * 80)
    print(f"  Algorithm:           {PROJECT_CONFIG['algorithm']}")
    print(f"  Total Episodes:      {PROJECT_CONFIG['episodes']}")
    print(f"  Start Time:          {datetime.now().strftime('%H:%M:%S')}")
    print()
    print("⏳ Training in progress...")
    print("(This may take several minutes. Monitor with TensorBoard in another terminal)")
    print()
    
    # Change to src directory
    os.chdir(SRC_DIR)
    
    # Record start time
    start_time = time.time()
    
    try:
        # Stage 4: Run training
        print_progress_indicator(4, 5)
        result = subprocess.run([PYTHON_BIN, "main.py"], check=False)
        exit_code = result.returncode
        
    except KeyboardInterrupt:
        print("\n⚠️ Training interrupted by user.")
        exit_code = 1
        
    except Exception as e:
        print(f"\n❌ Error running training: {e}")
        exit_code = 1
    
    # Stage 5: Completion
    print_progress_indicator(5, 5)
    
    # Calculate runtime
    end_time = time.time()
    total_seconds = int(end_time - start_time)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    print("=" * 80)
    print("📈 TRAINING SUMMARY")
    print("=" * 80)
    print()
    
    if exit_code == 0:
        print("✅ TRAINING COMPLETED SUCCESSFULLY!")
        print()
        print(f"  Duration:            {hours}h {minutes}m {seconds}s")
        print(f"  End Time:            {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        # Display output paths
        models_path = os.path.join(PROJECT_ROOT, "TrafficLearningproject/src/models")
        logs_path = os.path.join(PROJECT_ROOT, "TrafficLearningproject/src/logs")
        
        print("📁 OUTPUT LOCATIONS")
        print("─" * 80)
        print(f"  Models:              {models_path}")
        print(f"  Metrics:             {logs_path}/metrics.json")
        print(f"  Baseline:            {logs_path}/baseline_results.csv")
        print(f"  TensorBoard:         {logs_path}/tensorboard/")
        print()
        
        # View results instructions
        print("📊 VIEW RESULTS")
        print("─" * 80)
        print("  Option 1: View in TensorBoard (Recommended)")
        print(f"    tensorboard --logdir={os.path.join(PROJECT_ROOT, 'TrafficLearningproject/src/logs/tensorboard')}")
        print("    Then open: http://localhost:6006")
        print()
        print("  Option 2: Check metrics file")
        print(f"    cat {logs_path}/metrics.json")
        print()
        print("  Option 3: Check baseline results")
        print(f"    cat {logs_path}/baseline_results.csv")
        print()
        
        print("🎯 NEXT STEPS")
        print("─" * 80)
        print("  1. Review before/after comparison (shown above)")
        print("  2. Analyze TensorBoard graphs for learning curves")
        print("  3. Check metrics.json for detailed episode data")
        print("  4. Use trained models (actor_final.pt) for inference")
        print()
        
    else:
        print("❌ TRAINING FAILED")
        print()
        print(f"  Exit Code:           {exit_code}")
        print(f"  Duration:            {hours}h {minutes}m {seconds}s")
        print()
        print("⚠️  Please check the error messages above for details.")
        print()
    
    print("=" * 80)
    print()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
