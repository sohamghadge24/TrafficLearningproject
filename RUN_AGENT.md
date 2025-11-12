# Running the Traffic MADRL Agent

This guide explains how to run your traffic control agent with full before/after performance comparison.

## Overview

The training script (`main.py`) now:
1. **Evaluates baseline controllers** (Fixed-Time and Actuated) - *BEFORE*
2. **Trains the MADRL agent** using PPO with safety constraints
3. **Displays comprehensive before/after comparison** - *AFTER*
4. **Shows TensorBoard event trends** (reward/cost progression)

## Quick Start

### 1. Ensure Virtual Environment is Activated

```bash
cd /Users/sohamghadge/Documents/Final_Project
source .venv/bin/activate
```

### 2. Run the Training Script

```bash
cd TrafficLearningproject/src
python main.py
```

## What the Script Does

### Phase 1: Configuration & Initialization
- Loads TrafficEnv with SUMO simulation
- Initializes PPO trainer with actor/critic networks
- Creates TensorBoard writer for logging

### Phase 2: Baseline Evaluation (BEFORE)
```
🧪 Testing Fixed-Time Controller...
   Fixed-Time: Reward=-12.34, Cost=0.5432

🧪 Testing Actuated Controller...
   Actuated: Reward=-8.76, Cost=0.4321
```

These baselines represent the performance **without learning**.

### Phase 3: MADRL Training
The agent learns over 200 episodes with:
- Alternating traffic scenarios (low, medium, high)
- PPO policy gradient updates
- Constrained optimization via Lagrange multiplier
- Model checkpoints saved every 20 episodes

### Phase 4: Before/After Comparison (AFTER)

After training completes, you'll see:

```
================================================================================
📊 BEFORE & AFTER COMPARISON
================================================================================

🧪 BASELINE CONTROLLERS (Before Training):
--------------------------------------------------------------------------------
  Fixed-Time          | Reward:    -12.34 | Cost: 0.5432
  Actuated            | Reward:     -8.76 | Cost: 0.4321

🤖 MADRL AGENT (After Training):
--------------------------------------------------------------------------------
  Best Episode: 195
  Scenario: medium
  Reward:     125.67
  Cost: 0.1234
  Steps: 3600

📈 PERFORMANCE GAINS:
--------------------------------------------------------------------------------
  Reward Improvement: +134.43 (+1534.1%)
  Cost Reduction: +77.4%

📊 TRAINING PROGRESS SUMMARY:
--------------------------------------------------------------------------------
  Initial Episode Reward:     -45.23
  Final Episode Reward:      125.67
  Trend: +170.90

  Initial Episode Cost:     0.6543
  Final Episode Cost:       0.1234
  Trend: -0.5309
================================================================================
```

## Output Files

After each run, the following files are created/updated:

### 1. **Metrics & Results**
```
logs/
├── metrics.json              # Episode-level rewards, costs, lengths
├── baseline_results.csv      # Baseline controller performance
└── tensorboard/
    └── events.out.tfevents.* # TensorBoard event files
```

### 2. **Trained Models**
```
models/
├── actor_best.pt            # Best actor network
├── critic_best.pt           # Best critic network
├── actor_final.pt           # Final actor network
├── critic_final.pt          # Final critic network
└── actor_ep*.pt, critic_ep*.pt  # Checkpoints every 20 episodes
```

## Viewing Results in TensorBoard

After training completes, view interactive graphs:

```bash
cd /Users/sohamghadge/Documents/Final_Project
tensorboard --logdir=TrafficLearningproject/src/logs/tensorboard
```

Then open: **http://localhost:6006**

### Available Metrics in TensorBoard:

- **Episode/Total_Reward** - Per-episode cumulative reward
- **Episode/Average_Cost_Episode** - Per-episode safety cost
- **Episode/Length** - Episode duration (steps)
- **Loss/Policy** - Actor network loss
- **Loss/Critic** - Critic network loss
- **Safety/Average_Cost_Buffer** - Buffer average cost
- **Safety/Lagrange_Multiplier** - Constraint penalty weight
- **WaitingTime/ErrorBars** - Waiting time comparison (if experiment files available)

## Understanding the Metrics

### Reward
- **Baseline**: Typically negative (-50 to -10) due to inefficient control
- **MADRL Agent**: Should improve significantly through learning (ideally +100 or higher)
- **Interpretation**: Higher is better

### Cost
- **Baseline**: Typically 0.3-0.7 (vehicles stopped frequently)
- **MADRL Agent**: Should reduce to 0.1-0.3 (smoother flow)
- **Interpretation**: Lower is better (safety constraint)

### Improvement Metrics
- **Reward Improvement**: Shows % gain over best baseline
- **Cost Reduction**: Shows % decrease in safety metric

## Configuration Customization

Edit `config.py` to adjust:

```python
TOTAL_EPISODES = 200           # Number of training episodes
MAX_STEPS_PER_EPISODE = 3600   # Simulation steps per episode
LEARNING_RATE_ACTOR = 3e-4     # Actor network learning rate
COST_LIMIT = 60.0              # Safety constraint threshold
```

## Troubleshooting

### Issue: "SUMO binary not found"
**Solution**: Ensure SUMO is installed via Homebrew:
```bash
brew install sumo
```

### Issue: "Config file not found"
**Solution**: Ensure scenario configs exist in:
```
TrafficLearningproject/src/scenarios/city4x4/{low,medium,high}/osm.sumocfg
```

### Issue: Training is very slow
**Solution**: 
- Reduce `MAX_STEPS_PER_EPISODE` in `config.py`
- Reduce `TOTAL_EPISODES` for quick testing
- Check that GPU is being used (DEVICE in config should show `cuda`)

## Next Steps

1. **Analyze Results**: Use TensorBoard to identify learning patterns
2. **Tune Hyperparameters**: Adjust learning rates, epochs, constraint limits
3. **Test on Different Scenarios**: Run with different cities (city2x2, city5x5, etc.)
4. **Deploy Agent**: Use trained models for real-time control

## Support

For issues or questions, check the main project README and config documentation.
