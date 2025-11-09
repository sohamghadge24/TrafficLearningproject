# Traffic MADRL - Multi-Agent Deep Reinforcement Learning for Traffic Control

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install torch numpy matplotlib tqdm tensorboard

# Optional: Install SUMO (for real simulation)
# Follow instructions at: https://sumo.dlr.de/docs/Installing/index.html
```

### Running the Training

```bash
# Start training (simulation mode, no SUMO required)
python src/main.py

# Monitor training with TensorBoard
tensorboard --logdir logs/tensorboard
```

## 📁 Project Structure

```
traffic-madrl/
├── src/
│   ├── agents/
│   │   ├── actor.py               # Policy network
│   │   └── critic.py              # Value network
│   ├── env/
│   │   ├── traffic_env.py         # Environment wrapper
│   │   └── sumo_interface.py      # SUMO integration (optional)
│   ├── madrl/
│   │   ├── ppo_trainer.py         # PPO algorithm with constraints
│   │   └── buffer.py              # Experience buffer
│   └── main.py                    # Training script
├── scenarios/
│   └── 4x4_grid/                  # SUMO network files (optional)
├── models/                        # Saved model checkpoints
├── logs/                          # Training logs and metrics
├── config.py                      # Hyperparameters
└── TrafficModel.ipynb            # Original notebook
```

## 🔧 Key Fixes Applied

### 1. **Dimension Mismatch Fix**
   - **Problem**: Batch advantages shape `(128,)` didn't match ratio shape `(128, 25)`
   - **Solution**: Properly flatten and expand advantages across agents

### 2. **Buffer Structure**
   - Changed from per-agent storage to global value estimation
   - Properly reshape data for batch training

### 3. **Actor-Critic Architecture**
   - Shared actor across all agents (parameter sharing)
   - Centralized critic evaluates global state
   - Proper dimension handling throughout

### 4. **Configuration Alignment**
   - STATE_DIM: 12 (matching notebook)
   - BATCH_SIZE: 128 (matching notebook)
   - NUM_AGENTS: 16 (4x4 grid)

## 📊 Training Outputs

### Models
- `models/actor_best.pt` - Best performing actor
- `models/critic_best.pt` - Best performing critic
- `models/lambda_best.pt` - Lagrange multiplier

### Logs
- `logs/tensorboard/` - TensorBoard training curves
- `logs/metrics.json` - Episode-by-episode metrics
- `logs/baseline_results.csv` - Baseline controller comparison

### Metrics Tracked
- Episode rewards
- Average queue lengths
- Constraint violations (pedestrian wait times)
- Lagrange multiplier evolution
- Policy and critic losses

## 🎯 Algorithm Details

### Constrained PPO (C-PPO)
- **Objective**: Maximize traffic throughput while respecting safety constraints
- **Constraint**: Maximum pedestrian wait time ≤ 60 seconds
- **Method**: Lagrangian relaxation with adaptive penalty

### Multi-Objective Reward
```python
reward = w1 * throughput + 
         w2 * (-waiting_time) + 
         w3 * (-queue_length²) +
         w4 * (-queue_variation) +
         w5 * (-switching_penalty) +
         coordination_bonus
```

### Architecture
- **Centralized Training, Decentralized Execution (CTDE)**
- Shared actor for all agents (parameter efficiency)
- Global critic for value estimation
- Local observations, decentralized actions

## 🧪 Running Without SUMO

The code automatically runs in simulation mode if SUMO is not available:
- Simulated traffic dynamics
- Queue length evolution
- Multi-agent coordination
- Safety constraint tracking

## 📈 Expected Results

After 200 episodes, you should see:
- **Travel time reduction**: 15-25% vs Fixed-Time
- **Queue length reduction**: 20-30% vs Fixed-Time
- **Constraint violations**: Near-zero after convergence
- **Lambda convergence**: Stabilizes around 5-10

## 🔍 Monitoring Training

### TensorBoard
```bash
tensorboard --logdir logs/tensorboard
```

View:
- Loss/Policy - Actor loss over time
- Loss/Critic - Critic loss over time
- Safety/Average_Cost - Constraint violation
- Safety/Lagrange_Multiplier - Penalty evolution
- Episode/Total_Reward - Performance per episode

### Console Output
```
Ep  100 | Scenario: medium | Reward: 45231.45 | Cost:   3.21 | Lambda: 5.2341
```

## 🛠️ Customization

### Adjust Hyperparameters
Edit `config.py`:
```python
TOTAL_EPISODES = 500        # More training
BATCH_SIZE = 256            # Larger batches
LEARNING_RATE_ACTOR = 1e-4  # Slower learning
COST_LIMIT = 45.0           # Stricter constraint
```

### Change Grid Size
```python
NUM_AGENTS = 25  # 5x5 grid
```

### Add SUMO Integration
1. Install SUMO
2. Create network files in `scenarios/4x4_grid/`
3. Set `SUMO_CONFIG_FILE` in `config.py`
4. Run with `use_sumo=True` in `traffic_env.py`

## 🐛 Troubleshooting

### "Buffer is full" Error
- Increase `BUFFER_SIZE` in config.py
- Or decrease `MAX_STEPS_PER_EPISODE`

### Out of Memory
- Reduce `BATCH_SIZE`
- Reduce `BUFFER_SIZE`
- Use smaller network (fewer hidden units)

### Slow Training
- Reduce `PPO_EPOCHS`
- Increase `BUFFER_SIZE` (update less frequently)
- Use GPU if available

### Poor Performance
- Train for more episodes (500-1000)
- Adjust reward weights
- Tune learning rates
- Check constraint limit is reasonable

## 📚 References

1. **PPO**: Schulman et al., "Proximal Policy Optimization Algorithms" (2017)
2. **C-PPO**: Ray et al., "Benchmarking Safe Exploration in Deep Reinforcement Learning" (2019)
3. **CTDE**: Lowe et al., "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments" (2017)

## 📝 Next Steps

1. **Scale Up**: Test on larger grids (10x10)
2. **Real Data**: Integrate with SUMO using real traffic patterns
3. **Transfer Learning**: Pre-train on diverse scenarios
4. **Advanced Features**: 
   - Emergency vehicle priority
   - Time-of-day adaptation
   - Weather conditions

## 🤝 Contributing

Feel free to:
- Report issues
- Suggest improvements
- Add new features
- Share results

## 📄 License

MIT License - See LICENSE file for details