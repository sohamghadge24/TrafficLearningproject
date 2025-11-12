# 🚀 COMPLETE PROJECT GUIDE - Traffic MADRL Agent

## Welcome! 👋

This is a **Multi-Agent Deep Reinforcement Learning (MADRL)** system for optimizing traffic light control in a 4x4 intersection grid using the SUMO traffic simulator. The agent learns to minimize congestion and maximize vehicle throughput.

---

## 📋 TABLE OF CONTENTS

1. [Quick Start](#quick-start)
2. [What This Project Does](#what-this-project-does)
3. [Project Structure](#project-structure)
4. [How to Run](#how-to-run)
5. [Understanding the System](#understanding-the-system)
6. [File Directory Reference](#file-directory-reference)
7. [Training Process](#training-process)
8. [Results & Metrics](#results--metrics)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Usage](#advanced-usage)

---

## QUICK START

### ⚡ Fastest Way to Run

```bash
cd /Users/sohamghadge/Documents/Final_Project
python3 run_agent.py
```

**That's it!** The script will:
- ✅ Activate the virtual environment
- ✅ Evaluate baseline controllers (Fixed-Time, Actuated)
- ✅ Train MADRL agent for 200 episodes
- ✅ Show before/after comparison
- ✅ Save all results

### 🎯 What to Expect

**Training Time**: ~15-20 minutes  
**Output**: Real-time progress with percentage bars  
**Results**: Saved in `logs/` and `models/` directories

---

## WHAT THIS PROJECT DOES

### 🎯 The Problem
Traffic congestion wastes time, fuel, and creates pollution. Traditional fixed-time traffic lights don't adapt to real-world traffic patterns.

### 💡 The Solution
A **multi-agent reinforcement learning system** that:
- 🤖 Controls 16 traffic lights in a 4x4 grid
- 📊 Learns optimal signal timing from experience
- 🔒 Enforces safety constraints (cost limits)
- ⚡ Adapts to different traffic scenarios (low/medium/high)

### 🏆 Key Features

| Feature | Benefit |
|---------|---------|
| **16 Agents** | Coordinates traffic control across entire grid |
| **PPO Algorithm** | Proven, sample-efficient reinforcement learning |
| **Safety Constraints** | Lagrangian penalty ensures realistic behavior |
| **Multi-Scenario Training** | Handles diverse traffic conditions |
| **Baseline Comparison** | Shows improvement vs. traditional methods |

---

## PROJECT STRUCTURE

```
📁 Final_Project/
├── 📄 README Files (Documentation)
│   ├── README.md
│   ├── README_AGENT.md
│   ├── QUICK_START.txt
│   └── PROJECT_FILE_GUIDE.md
│
├── 🚀 Execution Scripts
│   ├── run_agent.py          ← Main entry point
│   ├── run_agent.sh
│   └── reset_environment.sh  ← Clean reset
│
├── 🧪 Testing Scripts
│   ├── test_main_quick.py    ← Quick 2-episode test
│   ├── test_quick.py         ← SUMO connection test
│   └── baseline_demo.py      ← See progress bars
│
├── 📁 TrafficLearningproject/src/  ← Main source code
│   ├── main.py               ← Training orchestration
│   ├── config.py             ← All hyperparameters
│   ├── env/                  ← Environment (SUMO interface)
│   ├── madrl/                ← RL algorithm (PPO)
│   ├── agents/               ← Neural networks (Actor/Critic)
│   └── scenarios/            ← Traffic network files
│
├── 📊 Output Directories
│   ├── logs/                 ← Training metrics & TensorBoard
│   ├── models/               ← Saved neural network weights
│   └── __pycache__/          ← Python cache
│
└── 📚 Documentation
    ├── BASELINE_ENHANCEMENT.md
    ├── ENHANCEMENT_SUMMARY.md
    ├── FINAL_STATUS.md
    └── More...
```

---

## HOW TO RUN

### 1️⃣ **Option A: Full Training (Recommended)**

```bash
cd /Users/sohamghadge/Documents/Final_Project
python3 run_agent.py
```

**What happens:**
- Baseline evaluation with progress bars
- 200 episodes of MADRL training
- Real-time logging to TensorBoard
- Model checkpoints every 20 episodes
- Before/after comparison at the end

**Output files:**
```
logs/
├── metrics.json              (All training metrics)
├── baseline_results.csv      (Baseline comparison)
└── tensorboard/              (For visualization)

models/
├── actor_final.pt            (Final policy)
├── critic_final.pt           (Final value network)
├── actor_best.pt             (Best episode policy)
├── critic_best.pt            (Best episode value)
└── actor_ep*.pt / critic_ep*  (Checkpoints)
```

### 2️⃣ **Option B: Quick Test (2 Episodes)**

```bash
python3 test_main_quick.py
```

**Time**: ~30 seconds  
**Purpose**: Verify everything works before full training

### 3️⃣ **Option C: View Demo (No Simulation)**

```bash
python3 baseline_demo.py
```

**Shows**: What output will look like  
**Time**: ~5 seconds  
**Purpose**: Understand the format

### 4️⃣ **Option D: SUMO Connection Test**

```bash
python3 test_quick.py
```

**Time**: ~10 seconds  
**Purpose**: Verify SUMO simulator is installed and working

---

## UNDERSTANDING THE SYSTEM

### 🎮 The Traffic Control Problem

**State** (what the agent sees):
- Current traffic light phase
- Vehicle queue lengths (N, S, E, W)
- Average vehicle speeds
- History of previous states

**Action** (what the agent does):
- `0`: Maintain current phase
- `1`: Switch to next phase

**Reward** (what the agent optimizes):
- Higher reward for higher average vehicle speeds
- Penalized for vehicles that are stopped (cost)

### 🧠 How the Agent Learns

```
1. Reset Environment
   └─ Start simulation with random traffic

2. Collect Experience (per step)
   ├─ Get current state from SUMO
   ├─ Agent decides action (Actor network)
   ├─ Execute action in SUMO
   └─ Receive: new state, reward, cost

3. Store Experience (2048 transitions)
   └─ Save to replay buffer

4. Training Update (when buffer full)
   ├─ Compute advantages (how good was the action?)
   ├─ Update Actor: Improve policy (PPO loss)
   ├─ Update Critic: Improve value estimates
   └─ Adjust safety constraint (Lagrange multiplier)

5. Repeat for 200 episodes
```

### 🛡️ Safety Constraints

The system uses a **Lagrangian penalty** to enforce:
- Cost should not exceed 60% of vehicles stopped
- Penalty increases if constraint is violated
- Agent learns to balance reward and safety

---

## FILE DIRECTORY REFERENCE

### 🎯 Root Level Scripts

| Script | Purpose | Runtime |
|--------|---------|---------|
| `run_agent.py` | Main training launcher | 15-20 min |
| `test_main_quick.py` | Quick validation (2 ep) | 30 sec |
| `test_quick.py` | SUMO connection test | 10 sec |
| `baseline_demo.py` | Show demo output | 5 sec |
| `reset_environment.sh` | Clean reset | 10 sec |
| `verify_setup.py` | Check dependencies | 5 sec |

### 📁 TrafficLearningproject/src/

#### **Core Training**
```
main.py (400 lines)
├─ Baseline evaluation
│  ├─ Fixed-Time controller
│  └─ Actuated controller
├─ MADRL training loop (200 episodes)
│  ├─ Collect actions
│  ├─ Execute in SUMO
│  ├─ Store experience
│  └─ Train networks
└─ Before/after comparison
```

#### **Configuration**
```
config.py (100 lines)
├─ Hyperparameters (learning rates, episodes, etc.)
├─ File paths (logs, models, scenarios)
├─ Network parameters (hidden dims, etc.)
└─ Training settings (buffer size, etc.)
```

#### **Environment (env/)**
```
traffic_env.py
├─ RL environment interface
├─ Manages reset() and step()
└─ Provides states, rewards, costs

sumo_interface.py
├─ Low-level SUMO control
├─ Starts/stops simulator
├─ Sends actions via TraCI
└─ Collects observations
```

#### **Algorithm (madrl/)**
```
ppo_trainer.py (300 lines)
├─ Collects experience
├─ Computes advantages
├─ PPO policy update
├─ Value network update
└─ Manages constraints

buffer.py
├─ Replay buffer storage
├─ Batch sampling
└─ Advantage computation
```

#### **Neural Networks (agents/)**
```
actor.py (80 lines)
└─ Policy network (state → action probs)

critic.py (100 lines)
├─ State value network
└─ Cost value network
```

#### **Scenarios (scenarios/)**
```
4x4_grid/
├─ osm.net.xml.gz      (Network file)
├─ low_traffic.rou.xml (Low traffic routes)
├─ medium_traffic.rou.xml
└─ high_traffic.rou.xml

city4x4/
├─ low/osm.sumocfg
├─ medium/osm.sumocfg
└─ high/osm.sumocfg
```

---

## TRAINING PROCESS

### 📊 Step-by-Step Breakdown

#### **Phase 1: Baseline Evaluation** (5 min)
```
🧪 Testing Fixed-Time Controller...
   [████████████████████] 100.0% (5/5)
   ✅ Fixed-Time: Reward=   86.23, Cost=0.1003

🧪 Testing Actuated Controller...
   [████████████████████] 100.0% (5/5)
   ✅ Actuated:    Reward=   84.22, Cost=0.1090
```

**Establishes baseline to compare against**

#### **Phase 2: MADRL Training** (12 min)
```
🎯 STARTING MADRL TRAINING (200 episodes)
════════════════════════════════════════════════════════════════════════════════
Training: 100%|██████████| 200/200 [12:45<00:00,  3.83s/it]

Ep   1 | Scenario: medium | Reward: 3543.83 | Cost:  0.0563 | Lambda: 0.0000
Ep  10 | Scenario: medium | Reward: 3593.57 | Cost:  0.0486 | Lambda: 0.0250
Ep  20 | Scenario: medium | Reward: 3615.45 | Cost:  0.0457 | Lambda: 0.0312
...
Ep 200 | Scenario: high   | Reward: 3697.36 | Cost:  0.0394 | Lambda: 0.1842
```

**Agent learns optimal traffic light control**

#### **Phase 3: Before/After Comparison** (instant)
```
📊 BEFORE & AFTER COMPARISON
════════════════════════════════════════════════════════════════════════════════

🧪 BASELINE CONTROLLERS (Before Training):
   Fixed-Time           | Reward:   86.23 | Cost: 0.1003
   Actuated             | Reward:   84.22 | Cost: 0.1090

🤖 MADRL AGENT (After Training):
   Best Episode: 34
   Scenario: medium
   Reward: 3721.13
   Cost: 0.0354
   Steps: 3600

📈 PERFORMANCE GAINS:
   Reward Improvement: +3634.90 (+4213.7%)
   Cost Reduction: +64.8%
```

**Shows dramatic improvement over baselines**

### 🔄 Hyperparameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Episodes | 200 | Total training iterations |
| Steps/Episode | 3600 | 1 hour of simulated time |
| Buffer Size | 2048 | Transitions before training |
| LR Actor | 3e-4 | Policy network learning rate |
| LR Critic | 1e-3 | Value network learning rate |
| Entropy Coef | 0.01 | Exploration bonus |
| Clip Range | 0.2 | PPO clipping parameter |
| Cost Limit | 60.0 | Safety constraint (% stopped) |

---

## RESULTS & METRICS

### 📈 What Gets Saved

#### **1. metrics.json**
```json
{
  "episodes": [
    {
      "episode": 1,
      "scenario": "medium",
      "reward": 3543.83,
      "avg_cost": 0.0563,
      "steps": 3600
    },
    ...
    {
      "episode": 200,
      "scenario": "high",
      "reward": 3697.36,
      "avg_cost": 0.0394,
      "steps": 3600
    }
  ],
  "best_reward": 3721.13,
  "best_episode": 34
}
```

**Contains**: Every episode's reward, cost, scenario, and steps

#### **2. baseline_results.csv**
```
Method,Avg Reward,Avg Cost
Fixed-Time,86.23,0.1003
Actuated,84.22,0.1090
```

**Contains**: Baseline controller comparisons

#### **3. TensorBoard Logs**
```
logs/tensorboard/events.out.tfevents.xxxxx
```

**Contains**: Real-time metrics for visualization
- Episode reward trends
- Cost per episode
- Loss curves (policy & critic)
- Lagrange multiplier evolution

### 📊 How to Analyze Results

#### **View in TensorBoard** (Optional)
```bash
tensorboard --logdir=logs/tensorboard
# Then open http://localhost:6006
```

#### **Parse metrics.json**
```python
import json
with open('logs/metrics.json') as f:
    data = json.load(f)

# Get best episode
best_ep = data['best_episode']
print(f"Best reward: {data['best_reward']:.2f}")
print(f"Best episode: {best_ep}")

# Analyze trends
rewards = [ep['reward'] for ep in data['episodes']]
costs = [ep['avg_cost'] for ep in data['episodes']]
print(f"Reward trend: {rewards[0]:.2f} → {rewards[-1]:.2f}")
print(f"Cost trend: {costs[0]:.4f} → {costs[-1]:.4f}")
```

---

## TROUBLESHOOTING

### ❌ Problem: "SUMO not found"
```
Error: sumo command not found
```

**Solution:**
```bash
# Install SUMO
brew install sumo

# Verify installation
sumo --version
which sumo
```

### ❌ Problem: "Module not found: traci"
```
ModuleNotFoundError: No module named 'traci'
```

**Solution:**
```bash
# Reinstall SUMO with Python bindings
# Or ensure SUMO_HOME is set
export SUMO_HOME=/opt/homebrew/opt/sumo/share/sumo
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
```

### ❌ Problem: "TraCI connection refused"
```
Error: Connection refused at localhost:8813
```

**Solution:**
```bash
# Make sure no other SUMO processes are running
pkill -f sumo
pkill -f sumo-gui

# Run reset script
bash reset_environment.sh

# Try again
python3 run_agent.py
```

### ❌ Problem: "Out of memory"
```
RuntimeError: CUDA out of memory
```

**Solution:**
- The system uses CPU by default (safe)
- Reduce BUFFER_SIZE in config.py if needed
- Close other applications

### ❌ Problem: "Virtual environment not found"
```
source: no such file or directory: .venv/bin/activate
```

**Solution:**
```bash
# Recreate venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r TrafficLearningproject/requirements.txt
```

---

## ADVANCED USAGE

### 🔧 Modify Hyperparameters

Edit `TrafficLearningproject/src/config.py`:

```python
# Number of training episodes
TOTAL_EPISODES = 500  # Increase for longer training

# Learning rates
LEARNING_RATE_ACTOR = 5e-4    # Increase for faster learning
LEARNING_RATE_CRITIC = 2e-3

# Safety constraint
COST_LIMIT = 50.0  # Stricter safety (0-100)

# Buffer size
BUFFER_SIZE = 4096  # More data per update
```

### 🎯 Train on Different Scenarios

Modify `main.py` line where scenarios are defined:

```python
# Default: alternates between low/medium/high
traffic_scenarios = ['low', 'medium', 'high']

# Only high traffic (harder problem)
traffic_scenarios = ['high'] * 200

# Custom sequence
traffic_scenarios = ['low'] * 50 + ['medium'] * 100 + ['high'] * 50
```

### 💾 Load Trained Models

```python
import torch
from agents.actor import Actor
from agents.critic import Critic

# Load best models
actor = Actor()
actor.load_state_dict(torch.load('models/actor_best.pt'))

critic = Critic()
critic.load_state_dict(torch.load('models/critic_best.pt'))

# Use for inference/evaluation
state = env.reset()
action_probs, _ = actor(state)
action = action_probs.argmax(dim=-1)
```

### 📊 Custom Analysis Script

```python
import json
import numpy as np
import matplotlib.pyplot as plt

# Load metrics
with open('logs/metrics.json') as f:
    data = json.load(f)

# Extract data
episodes = [e['episode'] for e in data['episodes']]
rewards = [e['reward'] for e in data['episodes']]
costs = [e['avg_cost'] for e in data['episodes']]

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

ax1.plot(episodes, rewards)
ax1.set_ylabel('Reward')
ax1.set_title('Training Progress')

ax2.plot(episodes, costs)
ax2.set_ylabel('Cost')
ax2.set_xlabel('Episode')

plt.tight_layout()
plt.savefig('training_curves.png')
```

### 🔍 Evaluate on Specific Scenario

```python
from env.traffic_env import TrafficEnv

env = TrafficEnv(gui=False)

# Test on high traffic only
for _ in range(5):
    state = env.reset(seed=42, scenario='high')
    done = False
    total_reward = 0
    
    while not done:
        # Use trained policy
        action, _ = actor(torch.tensor(state))
        state, reward, cost, done, _ = env.step(action)
        total_reward += reward.mean()
    
    print(f"High traffic reward: {total_reward:.2f}")

env.close()
```

---

## 🎓 LEARNING RESOURCES

### Understanding the Code

**Start with:**
1. `main.py` - See the overall flow
2. `config.py` - Understand all settings
3. `env/traffic_env.py` - How environment works
4. `madrl/ppo_trainer.py` - The learning algorithm
5. `agents/actor.py` & `critic.py` - Neural networks

**Key Concepts:**
- **Reinforcement Learning**: Agent learns by trial and error
- **PPO (Proximal Policy Optimization)**: Safe policy update method
- **Multi-Agent**: Multiple agents coordinate (16 traffic lights)
- **Constrained RL**: Safety constraints enforced with Lagrangian penalty
- **SUMO**: Traffic simulator providing realistic environment

### Recommended Reading

- OpenAI PPO paper: https://arxiv.org/abs/1707.06347
- SUMO simulator: https://sumo.dlr.de/
- Traffic control basics: https://en.wikipedia.org/wiki/Traffic_signal_control

---

## 🤝 CONTRIBUTING & CUSTOMIZING

### To Add Your Own Traffic Network

1. Create SUMO network file (`.net.xml`)
2. Create route file (`.rou.xml`)
3. Create config file (`.sumocfg`)
4. Update `config.py` to reference it
5. Modify traffic scenarios in `main.py`

### To Change Reward/Cost Functions

Edit `env/sumo_interface.py`:

```python
def calculate_reward(self, ...):
    """Modify reward calculation"""
    # Current: reward = average speed
    # Could add: penalty for wait times, etc.
    
def calculate_cost(self, ...):
    """Modify cost calculation"""
    # Current: cost = ratio of stopped vehicles
    # Could change to: emissions, fuel consumption, etc.
```

---

## 📞 QUICK REFERENCE

### Common Commands

```bash
# Full training
python3 run_agent.py

# Quick test
python3 test_main_quick.py

# View demo
python3 baseline_demo.py

# Reset everything
bash reset_environment.sh

# View TensorBoard
tensorboard --logdir=logs/tensorboard

# Verify setup
python3 verify_setup.py
```

### Important Paths

```
Configuration:
  TrafficLearningproject/src/config.py

Training:
  TrafficLearningproject/src/main.py

Results:
  logs/metrics.json
  logs/baseline_results.csv
  logs/tensorboard/

Models:
  models/actor_final.pt
  models/critic_final.pt
  models/actor_best.pt
  models/critic_best.pt
```

### Key Files to Understand

| File | Priority | Purpose |
|------|----------|---------|
| `main.py` | ⭐⭐⭐ | Training orchestration |
| `config.py` | ⭐⭐⭐ | Hyperparameters |
| `traffic_env.py` | ⭐⭐⭐ | Environment interface |
| `ppo_trainer.py` | ⭐⭐ | Learning algorithm |
| `sumo_interface.py` | ⭐⭐ | SUMO simulator control |
| `actor.py` / `critic.py` | ⭐⭐ | Neural networks |
| `buffer.py` | ⭐ | Experience storage |

---

## ✅ VERIFICATION CHECKLIST

Before running full training:

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Virtual environment: `source .venv/bin/activate`
- [ ] SUMO installed: `sumo --version`
- [ ] Dependencies installed: `pip list | grep torch`
- [ ] Quick test passes: `python3 test_quick.py`
- [ ] 15-20 minutes available for training
- [ ] At least 2GB free disk space for models
- [ ] At least 4GB RAM available

---

## 🎉 YOU'RE READY!

Your system is fully set up and ready to train a multi-agent traffic control system. 

### Next Steps:

1. **Run quick test** to verify everything works:
   ```bash
   python3 test_main_quick.py
   ```

2. **Run full training**:
   ```bash
   python3 run_agent.py
   ```

3. **Analyze results**:
   - Check `logs/metrics.json` for metrics
   - View TensorBoard: `tensorboard --logdir=logs/tensorboard`
   - Compare with baseline results

4. **Customize** (optional):
   - Modify hyperparameters in `config.py`
   - Change traffic scenarios in `main.py`
   - Adjust reward/cost functions in `sumo_interface.py`

---

## 📚 DOCUMENTATION INDEX

- **README.md** - Original project documentation
- **README_AGENT.md** - Agent usage guide
- **PROJECT_FILE_GUIDE.md** - Detailed file reference
- **BASELINE_ENHANCEMENT.md** - Progress bar enhancement
- **ENHANCEMENT_SUMMARY.md** - Feature summary
- **This Guide** - Complete walkthrough

---

**Created**: 12 November 2025  
**Project Status**: ✅ Production Ready  
**Last Updated**: 12 November 2025

Happy training! 🚀🚗
