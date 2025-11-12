import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from agents.actor import Actor
from agents.critic import Critic
from madrl.buffer import ExperienceBuffer
from config import NUM_AGENTS, LEARNING_RATE_ACTOR, LEARNING_RATE_CRITIC, PPO_EPOCHS, CLIP_EPSILON, BATCH_SIZE, DEVICE,COST_LIMIT, LAGRANGE_LR, LAGRANGE_INIT, LAGRANGE_MAX, MODEL_DIR,MAX_GRAD_NORM



class PPOTrainer:
    """
    Implements the Constrained Proximal Policy Optimization (C-PPO) algorithm.

    The method alternates between policy optimization (θ update) and
    Lagrange multiplier update (λ update) to enforce safety constraints.
    """

    def __init__(self):
        # Actor–Critic initialization
        self.actor = Actor().to(DEVICE)
        self.critic = Critic().to(DEVICE)

        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=LEARNING_RATE_ACTOR)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=LEARNING_RATE_CRITIC)

        # Experience replay buffer for multi-agent collection
        self.buffer = ExperienceBuffer(NUM_AGENTS)

        # Lagrange multiplier (λ) – learnable constraint coefficient
        self.lagrange_multiplier = torch.tensor(
            LAGRANGE_INIT, dtype=torch.float32, device=DEVICE, requires_grad=True
        )
        self.lagrange_optimizer = optim.Adam([self.lagrange_multiplier], lr=LAGRANGE_LR)

        # Episode-level cost tracking
        self.current_episode_cost_sum = 0.0
        self.current_episode_steps = 0

    # ---------------------------------------------------------------------- #
    #  ACTION SELECTION AND EXPERIENCE STORAGE
    # ---------------------------------------------------------------------- #
    def step_collect(self, states, deterministic: bool = False):
        """
        Collects (action, log_prob, value, cost_value) tuples for all agents.

        Returns:
            actions: Tensor [N_agents]
            log_probs: Tensor [N_agents]
            values, cost_values: Critics’ outputs
        """
        with torch.no_grad():
            values, cost_values = self.critic(states)

            actions, log_probs = [], []
            for i in range(NUM_AGENTS):
                action, log_prob, _ = self.actor.get_action_and_log_prob(
                    states[i], deterministic=deterministic
                )
                actions.append(action)
                log_probs.append(log_prob)

            actions = torch.stack(actions)
            log_probs = torch.stack(log_probs).unsqueeze(-1)

        return actions, log_probs, values, cost_values

    def store(self, state, action, log_prob, reward, cost, value, cost_value, done):
        """Stores transitions in buffer and accumulates cost for constraint evaluation."""
        self.buffer.store(state, action, log_prob, reward, cost, value, cost_value, done)
        # Note: reward and cost tensors have shape (NUM_AGENTS, 1)
        self.current_episode_cost_sum += cost.mean().item()
        self.current_episode_steps += 1

    # ---------------------------------------------------------------------- #
    #  LAGRANGE MULTIPLIER UPDATE
    # ---------------------------------------------------------------------- #
    def update_lagrange_multiplier(self):
        """
        Updates the Lagrange multiplier λ to enforce cost constraint.
        """
        # Average cost over the whole buffer (Buffer_Size * NUM_AGENTS steps)
        avg_cost = self.buffer.costs.mean()
        
        # Loss function L_λ = −λ (E[C(τ)] − C_limit)
        lagrange_loss = -(self.lagrange_multiplier * (avg_cost - COST_LIMIT))

        self.lagrange_optimizer.zero_grad()
        lagrange_loss.backward()
        self.lagrange_optimizer.step()

        # Project λ into [0, LAGRANGE_MAX]
        with torch.no_grad():
            self.lagrange_multiplier.data.clamp_(0.0, LAGRANGE_MAX)

        return avg_cost.item()

    # ---------------------------------------------------------------------- #
    #  TRAINING STEP (C-PPO UPDATE)
    # ---------------------------------------------------------------------- #
    def train_step(self, next_states, done):
        """
        Executes one full optimization step of the Constrained PPO algorithm.
        """
        # 1. Bootstrapping final value estimates
        with torch.no_grad():
            next_v, next_cv = self.critic(next_states)
            if done:
                # If episode ended, terminal state value is 0
                next_v = torch.zeros_like(next_v)
                next_cv = torch.zeros_like(next_cv)

        # 2. Compute advantages (GAE) and returns
        self.buffer.compute_advantages_and_returns(next_v, next_cv)

        # 3. Lagrange update (constraint enforcement)
        avg_cost_buffer = self.update_lagrange_multiplier()
        current_lambda = self.lagrange_multiplier.item()

        # 4. PPO optimization epochs
        for epoch in range(PPO_EPOCHS):
            for (
                    states, actions, old_log_probs,
                    advantages, returns,
                    cost_advantages, cost_returns
                ) in self.buffer.get(BATCH_SIZE):

                # Normalize advantages for stability
                advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
                cost_advantages = (cost_advantages - cost_advantages.mean()) / (cost_advantages.std() + 1e-8)

                # ---------- POLICY LOSS (C-PPO Objective) ----------
                
                # Reshape actions/states for policy input: [Batch_Size * N_agents] -> [Batch_Size]
                # Note: The buffer flattens everything, so states/actions are already flattened.
                
                # states: (batch, STATE_DIM), actions: (batch, 1)
                new_log_probs = self.actor.get_log_prob(states, actions.squeeze(-1)).unsqueeze(-1)

                ratio = torch.exp(new_log_probs - old_log_probs)

                surr1 = ratio * advantages
                surr2 = torch.clamp(ratio, 1.0 - CLIP_EPSILON, 1.0 + CLIP_EPSILON) * advantages

                # Constrained objective: J(θ) = min(surr1, surr2) − λ * cost_advantage
                # The gradient w.r.t λ is handled by the Lagrange update, here λ is treated as a constant factor.
                policy_loss = -(torch.min(surr1, surr2) - current_lambda * cost_advantages).mean()

                # ---------- VALUE LOSS (Critic Update) ----------
                values, cost_values = self.critic(states)
                value_loss = F.mse_loss(values, returns)
                cost_value_loss = F.mse_loss(cost_values, cost_returns)
                critic_loss = value_loss + cost_value_loss

                # Gradient updates
                self.actor_optimizer.zero_grad()
                # Apply gradient clipping before stepping the optimizer
                policy_loss.backward(retain_graph=True)
                nn.utils.clip_grad_norm_(self.actor.parameters(), MAX_GRAD_NORM)
                self.actor_optimizer.step()

                self.critic_optimizer.zero_grad()
                critic_loss.backward()
                nn.utils.clip_grad_norm_(self.critic.parameters(), MAX_GRAD_NORM)
                self.critic_optimizer.step()

        # Clear buffer after each update cycle
        self.buffer.clear()

        return {
            "policy_loss": policy_loss.item(),
            "critic_loss": critic_loss.item(),
            "avg_cost": avg_cost_buffer,
            "lagrange_multiplier": current_lambda,
        }

    # ---------------------------------------------------------------------- #
    #  EPISODE METRICS AND MODEL SAVE
    # ---------------------------------------------------------------------- #
    def get_episode_metrics(self):
        """Computes average episode cost (for logging) and resets counters."""
        if self.current_episode_steps == 0:
            return 0.0
        avg_episode_cost = self.current_episode_cost_sum / self.current_episode_steps
        self.current_episode_cost_sum = 0.0
        self.current_episode_steps = 0
        return avg_episode_cost

    def save_models(self, path_prefix="final"):
        """Saves trained Actor and Critic model weights."""
        torch.save(self.actor.state_dict(), f"{MODEL_DIR}/actor_{path_prefix}.pt")
        torch.save(self.critic.state_dict(), f"{MODEL_DIR}/critic_{path_prefix}.pt")