#!/usr/bin/env python3
"""
Verification script to check the scenarios folder organization.
Run this to verify all required files are in place.
"""

import os
import sys

def check_scenarios():
    """Check if all required scenario files exist."""
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    scenarios_path = os.path.join(base_path, 'scenarios', '4x4_grid')
    
    print("=" * 80)
    print("SCENARIOS FOLDER VERIFICATION")
    print("=" * 80)
    print(f"\nBase path: {scenarios_path}\n")
    
    # Check core files
    core_files = [
        'osm.net.xml.gz',
        'osm.poly.xml.gz',
        'output.add.xml',
        'osm.view.xml',
        'README.md'
    ]
    
    print("✓ Checking core shared files...")
    all_core_exist = True
    for f in core_files:
        path = os.path.join(scenarios_path, f)
        exists = os.path.exists(path)
        status = "✓" if exists else "✗"
        print(f"  {status} {f}")
        all_core_exist = all_core_exist and exists
    
    # Check route files
    print("\n✓ Checking route files...")
    routes_path = os.path.join(scenarios_path, 'routes')
    route_files = [
        'low_traffic.rou.xml',
        'medium_traffic.rou.xml',
        'high_traffic.rou.xml'
    ]
    
    all_routes_exist = True
    if os.path.exists(routes_path):
        for f in route_files:
            path = os.path.join(routes_path, f)
            exists = os.path.exists(path)
            status = "✓" if exists else "✗"
            print(f"  {status} {f}")
            all_routes_exist = all_routes_exist and exists
    else:
        print(f"  ✗ routes/ directory not found")
        all_routes_exist = False
    
    # Check scenario configs
    print("\n✓ Checking scenario configuration files...")
    scenarios = ['low', 'medium', 'high']
    all_configs_exist = True
    
    for scenario in scenarios:
        config_name = f'{scenario}_traffic.sumocfg'
        config_path = os.path.join(scenarios_path, scenario, config_name)
        exists = os.path.exists(config_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {scenario}/{config_name}")
        all_configs_exist = all_configs_exist and exists
    
    # Summary
    print("\n" + "=" * 80)
    if all_core_exist and all_routes_exist and all_configs_exist:
        print("✓ ALL CHECKS PASSED - Scenarios folder is properly organized!")
        print("\nYou can now run training with:")
        print("  python src/main.py")
        print("\nOr use specific scenarios:")
        print("  env.reset(seed=42, scenario='low')")
        print("  env.reset(seed=42, scenario='medium')")
        print("  env.reset(seed=42, scenario='high')")
        return 0
    else:
        print("✗ SOME FILES ARE MISSING - Please check the errors above")
        print("\nTo fix:")
        print("1. Ensure all route files exist in routes/")
        print("2. Ensure all scenario configs exist in low/, medium/, high/")
        print("3. Check that shared files are in the 4x4_grid/ root")
        return 1

if __name__ == '__main__':
    exit_code = check_scenarios()
    sys.exit(exit_code)
