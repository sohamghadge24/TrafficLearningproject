import numpy as np
import torch
from src.config import BUFFER_SIZE, STATE_DIM, DEVICE, GAMMA, GAE_LAMBDA

class ExperienceBuffer:
    """PPO Buffer for storing trajectories of multiple agents."""
    def __init__(self, num_agents):
        # All tensors stored in shape: (BUFFER_SIZE, NUM_AGENTS, *)
        self.states = torch.zeros((BUFFER_SIZE, num_agents, STATE_DIM), dtype=torch.float32, device=DEVICE)
        self.actions = torch.zeros((BUFFER_SIZE, num_agents, 1), dtype=torch.long, device=DEVICE)
        self.log_probs = torch.zeros((BUFFER_SIZE, num_agents, 1), dtype=torch.float32, device=DEVICE)
        self.rewards = torch.zeros((BUFFER_SIZE, num_agents, 1), dtype=torch.float32, device=DEVICE)
        self.costs = torch.zeros((BUFFER_SIZE, num_agents, 1), dtype=torch.float32, device=DEVICE)
        self.values = torch.zeros((BUFFER_SIZE, num_agents, 1), dtype=torch.float32, device=DEVICE)
        self.cost_values = torch.zeros((BUFFER_SIZE, num_agents, 1), dtype=torch.float32, device=DEVICE)
        self.dones = torch.zeros((BUFFER_SIZE, num_agents, 1), dtype=torch.bool, device=DEVICE) 
        
        self.ptr = 0
        self.num_agents = num_agents

    def store(self, state, action, log_prob, reward, cost, value, cost_value, done):
        """Stores a single step for all agents."""
        if self.ptr < BUFFER_SIZE:
            # State has shape (NUM_AGENTS, STATE_DIM), we store it as (1, NUM_AGENTS, STATE_DIM) implicitly
            self.states[self.ptr] = state
            # Ensure action, log_prob are correctly shaped (NUM_AGENTS, 1)
            self.actions[self.ptr] = action.unsqueeze(-1) if action.dim() == 1 else action
            self.log_probs[self.ptr] = log_prob.unsqueeze(-1) if log_prob.dim() == 1 else log_prob
            
            self.rewards[self.ptr] = reward
            self.costs[self.ptr] = cost
            self.values[self.ptr] = value
            self.cost_values[self.ptr] = cost_value
            self.dones[self.ptr] = torch.full((self.num_agents, 1), done, device=DEVICE)
            self.ptr += 1
        else:
            raise IndexError("Buffer is full!")

    def compute_advantages_and_returns(self, next_v, next_cv):
        """Calculates GAE Advantages and Returns (R_t, C_t)."""
        # Only compute over the filled portion of the buffer
        T = self.ptr
        if T == 0:
            # Nothing to compute
            self.returns = torch.zeros_like(self.values, device=DEVICE)
            self.cost_returns = torch.zeros_like(self.cost_values, device=DEVICE)
            self.advantages = torch.zeros_like(self.rewards, device=DEVICE)
            self.cost_advantages = torch.zeros_like(self.costs, device=DEVICE)
            return

        # Slice to valid entries
        values = torch.cat([self.values[:T], next_v.unsqueeze(0)], dim=0)
        cost_values = torch.cat([self.cost_values[:T], next_cv.unsqueeze(0)], dim=0)

        not_dones = ~self.dones[:T]
        deltas = self.rewards[:T] + GAMMA * values[1:] * not_dones - values[:-1]
        cost_deltas = self.costs[:T] + GAMMA * cost_values[1:] * not_dones - cost_values[:-1]

        advantages = torch.zeros_like(deltas, device=DEVICE)
        cost_advantages = torch.zeros_like(cost_deltas, device=DEVICE)

        # Generalized Advantage Estimation (GAE)
        last_lambda = torch.zeros((self.num_agents, 1), device=DEVICE)
        last_cost_lambda = torch.zeros((self.num_agents, 1), device=DEVICE)

        for t in reversed(range(T)):
            advantages[t] = deltas[t] + GAMMA * GAE_LAMBDA * not_dones[t] * last_lambda
            last_lambda = advantages[t]

            cost_advantages[t] = cost_deltas[t] + GAMMA * GAE_LAMBDA * not_dones[t] * last_cost_lambda
            last_cost_lambda = cost_advantages[t]

        # Returns = Advantage + Value
        self.returns = advantages + self.values[:T]
        self.cost_returns = cost_advantages + self.cost_values[:T]
        self.advantages = advantages
        self.cost_advantages = cost_advantages
        
    def get(self, batch_size):
        """Flattens the data and yields minibatches for optimization."""
        def flatten(data, T):
            # Reshape from (T, NUM_AGENTS, *) to (T * NUM_AGENTS, *)
            return data[:T].reshape(-1, data.shape[-1])

        T = self.ptr
        if T == 0:
            return

        flat_states = flatten(self.states, T)
        flat_actions = flatten(self.actions, T)
        flat_log_probs = flatten(self.log_probs, T)
        flat_advantages = flatten(self.advantages, T)
        flat_returns = flatten(self.returns, T)
        flat_cost_advantages = flatten(self.cost_advantages, T)
        flat_cost_returns = flatten(self.cost_returns, T)

        dataset_size = flat_states.shape[0]
        indices = np.arange(dataset_size)
        np.random.shuffle(indices)

        for start in range(0, dataset_size, batch_size):
            batch_indices = indices[start:start + batch_size]

            yield (
                flat_states[batch_indices],
                flat_actions[batch_indices],
                flat_log_probs[batch_indices],
                flat_advantages[batch_indices],
                flat_returns[batch_indices],
                flat_cost_advantages[batch_indices],
                flat_cost_returns[batch_indices],
            )
            
    def clear(self):
        self.ptr = 0