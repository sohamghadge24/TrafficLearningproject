import torch.nn as nn
from config import STATE_DIM, DEVICE

class Critic(nn.Module):
    """
    Defines the Critic Network (Value Function).
    In C-PPO, it estimates both the Reward Value (V) and the Cost Value (V_c).
    """
    def __init__(self):
        super().__init__()
        
        # Shared feature extractor
        self.fc_common = nn.Sequential(
            nn.Linear(STATE_DIM, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU()
        ).to(DEVICE)
        
        # Reward Value head (V(s))
        self.value_head = nn.Linear(128, 1).to(DEVICE)
        
        # Cost Value head (V_c(s))
        self.cost_head = nn.Linear(128, 1).to(DEVICE)
        
    def forward(self, state):
        """
        Input: state (Tensor, shape: [NUM_AGENTS, STATE_DIM])
        Output: value (Tensor, shape: [NUM_AGENTS, 1]), cost_value (Tensor, shape: [NUM_AGENTS, 1])
        """
        x = self.fc_common(state)
        value = self.value_head(x)
        cost_value = self.cost_head(x)
        return value, cost_value