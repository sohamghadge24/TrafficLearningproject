# 📚 PROJECT FILE STRUCTURE & PURPOSE GUIDE

## Project Overview

This is a **Traffic Signal Control using Multi-Agent Deep Reinforcement Learning (MADRL)** system. The project trains intelligent agents to optimize traffic light timing using PPO (Proximal Policy Optimization) with Lagrangian constraints for safety.

---

## 📁 DIRECTORY STRUCTURE & FILE PURPOSES

### 🎯 ROOT DIRECTORY (`/Users/sohamghadge/Documents/Final_Project`)

#### **EXECUTION & SETUP SCRIPTS**

| File | Purpose | What It Does |
|------|---------|------------|
| `run_agent.py` | **Main execution wrapper** | Activates venv and runs the training script with professional output formatting |
| `run_agent.sh` | **Bash execution script** | Alternative bash wrapper to run the agent |
| `reset_environment.sh` | **Environment reset** | Cleans up caches, terminates processes, resets logs for fresh runs |
| `verify_setup.py` | **System verification** | Checks if all dependencies, files, and configurations are in place |

#### **TESTING SCRIPTS**

| File | Purpose | What It Does |
|------|---------|------------|
| `test_quick.py` | **SUMO initialization test** | Verifies SUMO can start and connect to TraCI |
| `test_main_quick.py` | **Full pipeline test** | Runs 2 episodes to verify entire training loop works |
| `baseline_demo.py` | **Progress bar demo** | Shows what baseline evaluation output looks like |

#### **EXAMPLE & REFERENCE SCRIPTS**

| File | Purpose | What It Does |
|------|---------|------------|
| `sumo_example.py` | **SUMO usage example** | Demonstrates how to interact with SUMO simulator |
| `demo.html` | **Web demo** | HTML file for visualization (optional) |

#### **DOCUMENTATION FILES**

| File | Purpose |
|------|---------|
| `README.md` | Original project documentation |
| `README_AGENT.md` | Comprehensive agent usage guide |
| `QUICK_START.txt` | Quick reference for running the agent |
| `RUN_AGENT.md` | Detailed execution walkthrough |
| `AGENT_READY.md` | Setup instructions and getting started |
| `FINAL_STATUS.md` | Complete project status report |
| `CHANGES_SUMMARY.md` | Summary of all modifications |
| `BASELINE_ENHANCEMENT.md` | Details on percentage progress bars |
| `ENHANCEMENT_SUMMARY.md` | Feature summary and usage |
| `PERCENTAGE_BARS_QUICK_REF.md` | Quick reference for progress bars |
| `VALIDATION_REPORT.md` | Test results and system validation |
| `EXECUTION_SUMMARY.md` | Execution details and results |
| `ENHANCEMENT_DISPLAY.sh` | Display enhancement status |

---

### 🏗️ TRAFFICLEARNINGPROJECT/SRC (Main Source Code)

#### **CORE TRAINING FILE**

| File | Purpose | Key Components |
|------|---------|-----------------|
| `main.py` | **Main training orchestration** | • Baseline evaluation (Fixed-Time, Actuated controllers)<br>• MADRL training loop (200 episodes)<br>• TensorBoard logging<br>• Before/after comparison display<br>• Progress bars for baseline tests |

#### **CONFIGURATION**

| File | Purpose | What It Does |
|------|---------|------------|
| `config.py` | **Central configuration hub** | • Defines all hyperparameters (learning rates, episodes, etc.)<br>• Sets up file paths<br>• Dynamic scenario/city selection<br>• Creates necessary directories |
| `__init__.py` | **Package initialization** | Imports submodules and configurations<br>Logs that package loaded successfully |

---

### 🎮 ENV SUBDIRECTORY (Environment & SUMO Interaction)

#### **ENVIRONMENT WRAPPER**

| File | Purpose | What It Does |
|------|---------|------------|
| `traffic_env.py` | **RL Environment wrapper** | • Bridges RL training with SUMO simulator<br>• Provides `reset()` and `step()` methods<br>• Collects states from SUMO<br>• Returns rewards and costs to trainer<br>• Manages episode termination |

#### **SUMO INTERFACE**

| File | Purpose | What It Does |
|------|---------|------------|
| `sumo_interface.py` | **Low-level SUMO control** | • Starts/stops SUMO process<br>• Sends traffic light actions via TraCI<br>• Reads vehicle states from SUMO<br>• Calculates reward (speed-based)<br>• Calculates cost (stop ratio)<br>• Manages metrics collection |

#### **DEBUGGING**

| File | Purpose | What It Does |
|------|---------|------------|
| `debug_sumo.py` | **SUMO debugging utility** | Helpers for debugging SUMO issues<br>Output formatting for inspection |
| `__init__.py` | **Package initialization** | Imports environment modules |

---

### 🤖 MADRL SUBDIRECTORY (Reinforcement Learning Algorithm)

#### **MAIN TRAINER**

| File | Purpose | What It Does |
|------|---------|------------|
| `ppo_trainer.py` | **PPO algorithm implementation** | • Collects experience from environment<br>• Stores in replay buffer<br>• Performs PPO updates (clipped objective)<br>• Manages Lagrange multiplier (for constraints)<br>• Enforces safety constraints (cost limits)<br>• Saves/loads models |

#### **REPLAY BUFFER**

| File | Purpose | What It Does |
|------|---------|------------|
| `buffer.py` | **Experience replay storage** | • Stores states, actions, rewards, costs<br>• Provides batch sampling for training<br>• Tracks episode metrics<br>• Computes advantages (GAE) |

#### **PACKAGE INIT**

| File | Purpose |
|------|---------|
| `__init__.py` | Imports trainer and buffer classes |

---

### 👥 AGENTS SUBDIRECTORY (Neural Networks)

#### **ACTOR NETWORK**

| File | Purpose | What It Does |
|------|---------|------------|
| `actor.py` | **Policy network** | • Multi-layer neural network<br>• Takes state as input<br>• Outputs action probabilities (2 actions)<br>• Used by trainer for action selection<br>• Updated via policy gradient |

#### **CRITIC NETWORK**

| File | Purpose | What It Does |
|------|---------|------------|
| `critic.py` | **Value network** | • Multi-layer neural network<br>• Takes state as input<br>• Outputs state value estimate<br>• Outputs cost value estimate<br>• Used to compute advantages<br>• Updated via MSE loss |

#### **PACKAGE INIT**

| File | Purpose |
|------|---------|
| `__init__.py` | Imports actor and critic networks |

---

### 📊 LOGS DIRECTORY (Training Outputs)

| File/Folder | Purpose | Contents |
|-------------|---------|----------|
| `metrics.json` | **All training metrics** | Episode-by-episode: reward, cost, scenario, steps<br>Also: best_reward, best_episode metadata |
| `baseline_results.csv` | **Baseline comparison** | Fixed-Time and Actuated controller results<br>Used for before/after comparison |
| `tensorboard/` | **TensorBoard event logs** | Event files for visualization<br>Contains: rewards, costs, losses, lagrange multiplier |

---

### 🎯 MODELS DIRECTORY (Saved Neural Networks)

| File | Purpose | What It Stores |
|------|---------|----------------|
| `actor_final.pt` | **Final trained actor** | Policy network weights after 200 episodes |
| `critic_final.pt` | **Final trained critic** | Value network weights after 200 episodes |
| `actor_best.pt` | **Best episode actor** | Actor weights from highest reward episode |
| `critic_best.pt` | **Best episode critic** | Critic weights from highest reward episode |
| `actor_ep*.pt` | **Episode checkpoints** | Actor saved every 20 episodes (ep20, ep40, etc.) |
| `critic_ep*.pt` | **Episode checkpoints** | Critic saved every 20 episodes (ep20, ep40, etc.) |

---

### 📁 SCENARIOS DIRECTORY (Traffic Network Configuration)

#### **ORIGINAL 4X4 GRID**

| File | Purpose |
|------|---------|
| `4x4_grid/osm.net.xml.gz` | Network file (compressed): defines 16 intersections, roads, connections |
| `4x4_grid/low_traffic.rou.xml` | Low traffic scenario: vehicle routes for sparse traffic |
| `4x4_grid/medium_traffic.rou.xml` | Medium traffic scenario: balanced traffic density |
| `4x4_grid/high_traffic.rou.xml` | High traffic scenario: dense traffic conditions |

#### **ORGANIZED CITY STRUCTURE**

| Path | Purpose |
|------|---------|
| `city4x4/low/osm.sumocfg` | SUMO config for 4x4 grid, low traffic |
| `city4x4/medium/osm.sumocfg` | SUMO config for 4x4 grid, medium traffic |
| `city4x4/high/osm.sumocfg` | SUMO config for 4x4 grid, high traffic |

---

## 🔄 EXECUTION FLOW

### **When You Run `python3 run_agent.py`:**

```
1. run_agent.py
   ├─ Activates virtual environment
   └─ Calls main.py in TrafficLearningproject/src/
   
2. main.py
   ├─ Loads config.py (hyperparameters, paths)
   ├─ Creates TrafficEnv from traffic_env.py
   │  └─ traffic_env connects to sumo_interface.py
   │     └─ sumo_interface starts SUMO simulator
   │
   ├─ Phase 1: BASELINE EVALUATION (with progress bars)
   │  ├─ Tests Fixed-Time Controller (5 runs) → baseline_results.csv
   │  └─ Tests Actuated Controller (5 runs) → baseline_results.csv
   │
   ├─ Phase 2: MADRL TRAINING (200 episodes)
   │  ├─ For each episode:
   │  │  ├─ Reset env (traffic_env.py)
   │  │  ├─ Collect actions from PPOTrainer (ppo_trainer.py)
   │  │  │  └─ Uses Actor network (actor.py)
   │  │  ├─ Step environment (traffic_env.py)
   │  │  ├─ Store experience in Buffer (buffer.py)
   │  │  ├─ Update networks when buffer full
   │  │  │  ├─ Actor (policy gradient)
   │  │  │  └─ Critic (value regression)
   │  │  └─ Log metrics to TensorBoard
   │  │
   │  └─ Save models: actor_final.pt, critic_final.pt
   │
   ├─ Phase 3: BEFORE/AFTER COMPARISON
   │  └─ Displays baseline vs trained agent performance
   │
   └─ Saves all metrics to logs/metrics.json

3. Outputs
   ├─ Console: Before/after comparison + progress
   ├─ logs/metrics.json: Complete training history
   ├─ logs/baseline_results.csv: Baseline metrics
   ├─ logs/tensorboard/: Event files for visualization
   └─ models/: All checkpoints and final models
```

---

## 📊 KEY FILE RELATIONSHIPS

```
┌─────────────────────────────────────┐
│      run_agent.py                    │  (Entry point)
│      (Execution wrapper)             │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      main.py                         │  (Orchestration)
│      (Training loop)                 │
├─────────────────────────────────────┤
│  Imports:                            │
│  ├─ config.py (hyperparameters)     │
│  ├─ traffic_env.py (environment)    │
│  └─ ppo_trainer.py (algorithm)      │
└────────────────┬────────────────────┘
                 │
      ┌──────────┴──────────┬─────────────────────┐
      ▼                     ▼                     ▼
┌──────────────┐  ┌──────────────────┐  ┌─────────────────┐
│ traffic_env  │  │ ppo_trainer.py   │  │   config.py     │
│ (Env)        │  │ (Algorithm)      │  │ (Settings)      │
├──────────────┤  ├──────────────────┤  │                 │
│ Imports:     │  │ Imports:         │  │ Defines:        │
│├sumo_inter   │  │├actor.py (net)   │  │ ├Episodes       │
│├config.py    │  │├critic.py (net)  │  │ ├Learning rates │
└──────────────┘  │├buffer.py (mem)  │  │ └File paths    │
      │           └──────────────────┘  └─────────────────┘
      │
      ▼
┌──────────────────────┐
│  sumo_interface.py   │
│  (SUMO control)      │
├──────────────────────┤
│  Manages:            │
│  ├ SUMO process      │
│  ├ TraCI connection  │
│  ├ Actions          │
│  └ Observations     │
└──────────────────────┘
      │
      ▼
┌──────────────────────┐
│   SUMO Simulator     │
│   (4x4 Grid)         │
└──────────────────────┘
```

---

## 🎯 WHAT EACH COMPONENT DOES IN TRAINING

### **Actor Network (actor.py)**
- **Input**: Current traffic state (12 dimensions)
- **Output**: Probability of 2 actions (stay phase, switch phase)
- **Purpose**: Learns optimal traffic light control policy
- **Training**: Updated via policy gradient (PPO loss)

### **Critic Network (critic.py)**
- **Input**: Current traffic state (12 dimensions)
- **Output**: State value + Cost value estimates
- **Purpose**: Estimates how good a state is
- **Training**: Updated via MSE regression loss

### **Buffer (buffer.py)**
- **Stores**: States, actions, rewards, costs, advantages
- **Purpose**: Provides batch data for training
- **Size**: Configurable (default 2048 transitions)

### **PPO Trainer (ppo_trainer.py)**
- **Collects**: Transitions from environment
- **Computes**: Advantages, returns, cost estimates
- **Updates**: Actor (clipped policy loss) and Critic (value loss)
- **Enforces**: Safety constraints via Lagrange multiplier

### **Traffic Environment (traffic_env.py)**
- **Interface**: Between trainer and SUMO simulator
- **Provides**: States, rewards, costs, termination signals
- **Manages**: Episode reset, scenario selection

### **SUMO Interface (sumo_interface.py)**
- **Low-level control**: Direct SUMO process interaction
- **Actions**: Traffic light phase changes
- **Observations**: Vehicle positions, speeds, stops
- **Metrics**: Reward (speeds), Cost (stops)

---

## 💾 DATA FLOW DURING TRAINING

```
Episode Start
    │
    ├─ reset() → Initial state from SUMO
    │
    ├─ PPOTrainer.step_collect()
    │  └─ Actor network predicts action
    │
    ├─ env.step(action)
    │  └─ SUMO simulator executes action
    │     └─ Returns: next_state, reward, cost, done
    │
    ├─ Buffer.store()
    │  └─ Saves transition
    │
    ├─ If buffer full:
    │  ├─ Compute advantages & returns
    │  ├─ Actor loss = -logprob * advantage
    │  ├─ Critic loss = (value - return)²
    │  ├─ Actor.backward() and optimize
    │  ├─ Critic.backward() and optimize
    │  ├─ Update Lagrange multiplier
    │  └─ Clear buffer
    │
    └─ Repeat until episode done (3600 steps)

Episode End
    │
    ├─ Save metrics to metrics.json
    ├─ Log to TensorBoard
    ├─ Check if best episode → save models
    └─ Continue to next episode
```

---

## 🔑 KEY CONFIGURATION VALUES (config.py)

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `NUM_AGENTS` | 16 | Number of traffic light controllers |
| `STATE_DIM` | 12 | State vector size per agent |
| `ACTION_DIM` | 2 | Available actions (stay/switch) |
| `TOTAL_EPISODES` | 200 | Training episodes |
| `MAX_STEPS_PER_EPISODE` | 3600 | Simulation seconds per episode |
| `LEARNING_RATE_ACTOR` | 3e-4 | Actor network learning rate |
| `LEARNING_RATE_CRITIC` | 1e-3 | Critic network learning rate |
| `BUFFER_SIZE` | 2048 | Transitions before training update |
| `COST_LIMIT` | 60.0 | Safety constraint threshold |
| `LAGRANGE_LR` | 1e-2 | Constraint penalty adaptation rate |

---

## 📈 OUTPUT FILES EXPLANATION

### **metrics.json**
```json
{
  "episodes": [
    {
      "episode": 1,
      "scenario": "medium",
      "reward": 3543.83,      // Total episode reward
      "avg_cost": 0.0563,     // Average cost (0=perfect, 1=all stopped)
      "steps": 3600
    },
    ...
  ],
  "best_reward": 3721.13,     // Highest reward across all episodes
  "best_episode": 34          // Episode number with best reward
}
```

### **baseline_results.csv**
```
Method,Avg Reward,Avg Cost
Fixed-Time,86.23,0.1003
Actuated,84.22,0.1090
```

### **TensorBoard Events**
- Episode/Total_Reward: Reward per episode
- Episode/Average_Cost_Episode: Cost per episode
- Loss/Policy: Actor loss over training
- Loss/Critic: Critic loss over training
- Safety/Lagrange_Multiplier: Constraint penalty value

---

## 🚀 QUICK REFERENCE: WHO CALLS WHOM

```
run_agent.py
  └─ main.py
      ├─ config.py (load settings)
      ├─ traffic_env.py (create environment)
      │   └─ sumo_interface.py (SUMO control)
      ├─ ppo_trainer.py (create trainer)
      │   ├─ actor.py (create policy network)
      │   ├─ critic.py (create value networks)
      │   └─ buffer.py (create replay buffer)
      ├─ evaluate_baseline_fixed_time()
      ├─ evaluate_baseline_actuated()
      ├─ Training loop (200 episodes)
      │   ├─ env.reset()
      │   ├─ trainer.step_collect()
      │   ├─ env.step(action)
      │   ├─ trainer.store()
      │   ├─ trainer.train_step()
      │   └─ TensorBoard logging
      └─ _print_before_after_comparison()
```

---

## ✅ FILE SUMMARY TABLE

| File | Type | Lines | Purpose |
|------|------|-------|---------|
| main.py | Core | ~400 | Training orchestration |
| config.py | Config | ~100 | Hyperparameters & paths |
| traffic_env.py | Env | ~150 | RL environment wrapper |
| sumo_interface.py | Env | ~200 | SUMO simulator control |
| ppo_trainer.py | Algorithm | ~300 | PPO training logic |
| buffer.py | Memory | ~150 | Experience replay buffer |
| actor.py | Neural Net | ~80 | Policy network |
| critic.py | Neural Net | ~100 | Value networks |
| run_agent.py | Launcher | ~100 | Execution wrapper |
| test_main_quick.py | Test | ~50 | Quick validation |
| test_quick.py | Test | ~40 | SUMO test |
| reset_environment.sh | Script | ~50 | Reset & cleanup |

---

## 🎓 LEARNING PATH

To understand the code:

1. **Start here**: `main.py` - See overall training flow
2. **Then read**: `config.py` - Understand all settings
3. **Environment**: `traffic_env.py` → `sumo_interface.py`
4. **Algorithm**: `ppo_trainer.py` → `buffer.py`
5. **Networks**: `actor.py` and `critic.py`

---

**Status**: ✅ This is a complete, production-ready MADRL traffic control system!
