#!/usr/bin/env python3
"""
Verification script to check if all components are ready for running the agent.
"""

import os
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "TrafficLearningproject" / "src"

def check_file_exists(path, description=""):
    """Check if a file exists and print status."""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description or path}")
    return exists

def check_dir_exists(path, description=""):
    """Check if a directory exists and print status."""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description or path}")
    return exists

def main():
    print("\n" + "="*80)
    print("🔍 TRAFFIC MADRL AGENT - SYSTEM VERIFICATION")
    print("="*80)
    
    all_good = True
    
    # Check main components
    print("\n📁 MAIN FILES:")
    all_good &= check_file_exists(SRC_DIR / "main.py", "main.py (training script)")
    all_good &= check_file_exists(SRC_DIR / "config.py", "config.py (configuration)")
    all_good &= check_file_exists(SRC_DIR / "env" / "traffic_env.py", "traffic_env.py")
    all_good &= check_file_exists(SRC_DIR / "env" / "sumo_interface.py", "sumo_interface.py")
    
    # Check scenario structure
    print("\n🗺️  SCENARIO DIRECTORIES:")
    scenario_dirs = [
        "city2x2", "city3x3", "city4x4", "city5x5", "random"
    ]
    for city in scenario_dirs:
        city_path = SRC_DIR / "scenarios" / city
        all_good &= check_dir_exists(city_path, f"scenarios/{city}/")
        
        for traffic in ["low", "medium", "high"]:
            traffic_path = city_path / traffic
            all_good &= check_dir_exists(traffic_path, f"  └─ {traffic}/")
            
            config_file = traffic_path / "osm.sumocfg"
            if city == "city4x4":
                all_good &= check_file_exists(config_file, f"    └─ osm.sumocfg")
    
    # Check legacy config
    print("\n🔧 LEGACY CONFIG:")
    all_good &= check_file_exists(
        SRC_DIR / "scenarios" / "4x4_grid" / "osm.sumocfg",
        "4x4_grid/osm.sumocfg (fallback)"
    )
    
    # Check log directories
    print("\n📊 LOG DIRECTORIES:")
    logs_dir = PROJECT_ROOT / "logs"
    all_good &= check_dir_exists(logs_dir, "logs/")
    all_good &= check_dir_exists(logs_dir / "tensorboard", "logs/tensorboard/")
    
    # Check models directory
    print("\n🤖 MODELS DIRECTORY:")
    models_dir = PROJECT_ROOT / "models"
    all_good &= check_dir_exists(models_dir, "models/")
    
    # Check Python environment
    print("\n🐍 PYTHON ENVIRONMENT:")
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
    except ImportError:
        print("❌ PyTorch not found")
        all_good = False
    
    try:
        from torch.utils.tensorboard import SummaryWriter
        print("✅ TensorBoard (SummaryWriter)")
    except ImportError:
        print("❌ TensorBoard not found")
        all_good = False
    
    try:
        import traci
        print("✅ TraCI (SUMO Python API)")
    except ImportError:
        print("❌ TraCI not found - SUMO may not be installed correctly")
        all_good = False
    
    try:
        import sumolib
        print("✅ sumolib")
    except ImportError:
        print("❌ sumolib not found")
        all_good = False
    
    # Summary
    print("\n" + "="*80)
    if all_good:
        print("✅ ALL CHECKS PASSED - Ready to run the agent!")
        print("\nQuick start:")
        print("  cd /Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src")
        print("  python main.py")
    else:
        print("❌ SOME CHECKS FAILED - Please review the errors above")
        print("\nCommon fixes:")
        print("  1. Install SUMO: brew install sumo")
        print("  2. Activate venv: source .venv/bin/activate")
        print("  3. Install deps: pip install torch tensorboard traci sumolib")
    print("="*80 + "\n")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
