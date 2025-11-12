import torch
import torch.nn as nn
from torch.distributions import Categorical
from config import STATE_DIM, ACTION_DIM, DEVICE

class Actor(nn.Module):
    """
    Defines the Actor Network (Policy) for one agent.
    Outputs action logits for a Categorical distribution.
    """
    def __init__(self):
        super().__init__()
        
        self.network = nn.Sequential(
            nn.Linear(STATE_DIM, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, ACTION_DIM)
        ).to(DEVICE)
        
    def forward(self, state):
        """Input: state (Tensor, shape: [STATE_DIM]) -> Output: action_logits (Tensor, shape: [ACTION_DIM])"""
        return self.network(state)

    def get_action_and_log_prob(self, state, action=None, deterministic: bool = False):
        """
        Samples an action and calculates its log probability and the distribution's entropy.
        
        Note: The deterministic flag is added for clean evaluation/testing.
        """
        logits = self.forward(state)
        dist = Categorical(logits=logits)
        
        if action is None:
            if deterministic:
                # Select action with max probability (used for evaluation)
                action = torch.argmax(logits, dim=-1)
            else:
                # Sample action (used for training)
                action = dist.sample()
        
        log_prob = dist.log_prob(action)
        entropy = dist.entropy()
        
        return action, log_prob, entropy
    
    def get_log_prob(self, state, action):
        """Calculates log_prob for a specific action (used during PPO update)."""
        logits = self.forward(state)
        dist = Categorical(logits=logits)
        return dist.log_prob(action)