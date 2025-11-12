# Traffic MADRL Agent - Complete Setup & Usage Guide

## Quick Start

### Option 1: Using Python Script (Recommended)
```bash
cd /Users/sohamghadge/Documents/Final_Project
python3 run_agent.py
```

### Option 2: Using Bash Script
```bash
cd /Users/sohamghadge/Documents/Final_Project
bash run_agent.sh
```

### Option 3: Manual Setup
```bash
cd /Users/sohamghadge/Documents/Final_Project
source .venv/bin/activate
cd TrafficLearningproject/src
python main.py
```

## What the Agent Does

The training script performs a complete MADRL (Multi-Agent Deep Reinforcement Learning) training pipeline:

### Phase 1: Baseline Evaluation
Evaluates two baseline traffic control strategies:
- **Fixed-Time Controller**: Alternates between phases on a fixed schedule
- **Actuated Controller**: Queue-based heuristic that responds to traffic demand

These baselines establish the **BEFORE** performance metrics.

### Phase 2: MADRL Training  
Trains a policy-gradient agent (PPO with Lagrangian constraints) over 200 episodes with:
- Alternating traffic scenarios (low, medium, high)
- Safety constraint enforcement via Lagrange multipliers
- Model checkpoints saved every 20 episodes
- Real-time TensorBoard logging

### Phase 3: Results & Comparison
Displays comprehensive **BEFORE & AFTER** comparison showing:
- Baseline performance metrics
- Best trained agent performance
- Performance improvements (reward gain, cost reduction)
- Training progress trends

## Output Files

After running, you'll find:

```
logs/
├── metrics.json              # Episode-level metrics (reward, cost, steps)
├── baseline_results.csv      # Baseline controller results
└── tensorboard/
    └── events.out.tfevents.* # TensorBoard event logs

models/
├── actor_best.pt             # Best actor network weights
├── critic_best.pt            # Best critic network weights  
├── actor_final.pt            # Final actor network weights
├── critic_final.pt           # Final critic network weights
└── actor_ep*.pt, critic_ep*.pt  # Checkpoint files
```

## Viewing Results

### TensorBoard Dashboard
After training completes, view interactive graphs:
```bash
tensorboard --logdir=/Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src/logs/tensorboard
```
Then open: **http://localhost:6006**

**Available metrics:**
- `Episode/Total_Reward` - Per-episode cumulative reward
- `Episode/Average_Cost_Episode` - Safety metric (lower is better)
- `Episode/Length` - Simulation steps per episode
- `Loss/Policy` - Actor network loss
- `Loss/Critic` - Critic network loss
- `Safety/Lagrange_Multiplier` - Constraint penalty weight

### Metrics File
Review detailed metrics in:
```bash
cat TrafficLearningproject/src/logs/metrics.json
```

## Understanding the Metrics

### Reward
- **Baseline**: Typically -10 to 50 (inefficient control)
- **MADRL Agent**: Should improve to 80-150+ (efficient control)
- **Direction**: Higher is better ⬆️

### Cost (Safety Metric)
- **Baseline**: 0.3-0.7 (vehicles stopped frequently)
- **MADRL Agent**: Should reduce to 0.1-0.3 (smoother flow)
- **Direction**: Lower is better ⬇️

### Performance Gain
- **Reward Improvement**: % gain over best baseline
- **Cost Reduction**: % reduction in vehicles stopped
- Shows how much the agent has learned

## Configuration

Edit `TrafficLearningproject/src/config.py` to customize:

```python
TOTAL_EPISODES = 200           # Number of training episodes
MAX_STEPS_PER_EPISODE = 3600   # Simulation steps per episode
LEARNING_RATE_ACTOR = 3e-4     # Actor network learning rate
LEARNING_RATE_CRITIC = 1e-3    # Critic network learning rate
COST_LIMIT = 60.0              # Safety constraint threshold
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'torch'"
**Solution**: Virtual environment not activated
```bash
source /Users/sohamghadge/Documents/Final_Project/.venv/bin/activate
```

### Issue: "SUMO binary not found"
**Solution**: Install SUMO
```bash
brew install sumo
```

### Issue: "Config file not found"
**Solution**: Ensure scenario configs exist
```bash
ls /Users/sohamghadge/Documents/Final_Project/TrafficLearningproject/src/scenarios/city4x4/{low,medium,high}/osm.sumocfg
```

### Issue: "Connection closed by SUMO"
**Solution**: This usually means invalid config paths. Check that all file paths in the .sumocfg files are absolute and correct.

### Training is very slow
**Solutions:**
- Reduce `MAX_STEPS_PER_EPISODE` in config (e.g., 1800)
- Reduce `TOTAL_EPISODES` for testing (e.g., 10)
- Check system resources (CPU/Memory)

## Architecture Overview

```
TrafficLearningproject/
├── src/
│   ├── main.py                 # Training script
│   ├── config.py               # Configuration
│   ├── env/
│   │   ├── traffic_env.py      # Environment wrapper
│   │   └── sumo_interface.py   # SUMO integration
│   ├── madrl/
│   │   ├── ppo_trainer.py      # PPO algorithm
│   │   └── networks.py         # Actor/Critic networks
│   └── scenarios/
│       ├── 4x4_grid/           # Base network files
│       ├── city2x2,3x3,4x4,5x5/  # City folders
│       └── random/             # Random scenarios
└── models/                      # Trained models (output)
└── logs/                        # Metrics and TensorBoard (output)
```

## Action Space

The agent controls traffic lights with 2 actions:
- **Action 0**: Stay in current phase
- **Action 1**: Switch to next phase

This allows the agent to learn optimal phase timing and duration.

## State Space

Each agent observes:
- Current traffic light phase
- Queue lengths (vehicles waiting) for each approach (N, S, E, W)
- Average vehicle speeds for each approach
- Historical state information

Total: 12-dimensional state vector per agent

## Next Steps

1. **Run training** with `python3 run_agent.py`
2. **Monitor progress** with TensorBoard
3. **Analyze results** - compare before/after metrics
4. **Experiment** - adjust hyperparameters and re-run
5. **Deploy** - use trained models for inference

## Support

- Check `CHANGES_SUMMARY.md` for recent modifications
- See `RUN_AGENT.md` for detailed execution guide
- Review `config.py` for all configuration options

---

**Happy training! 🚦🤖**
