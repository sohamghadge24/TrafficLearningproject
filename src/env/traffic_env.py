import os
import torch
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.config import NUM_AGENTS, MAX_STEPS_PER_EPISODE, DEVICE, STATE_DIM, get_sumo_config_file
from src.env.sumo_interface import SUMOInterface


class TrafficEnv:
    """Multi-Agent Traffic Environment wrapper."""
    def __init__(self, gui=False, use_sumo=True, scenario='medium'):
        self.use_sumo = use_sumo
        self.scenario = scenario
        if use_sumo:
            self.sumo = SUMOInterface(gui=gui, scenario=scenario)
        # Track whether SUMO is currently running for safe restarts
        self.sumo_running = False
        self.current_step = 0
        self.num_agents = NUM_AGENTS
        self._scenario = None
        
    def reset(self, seed=None, scenario='medium'):
        """
        Resets the environment.
        Args:
            seed (int): Random seed for the simulation
            scenario (str): Traffic scenario ('low', 'medium', 'high')
        """
        self.current_step = 0
        
        if self.use_sumo:
            if hasattr(self, 'sumo') and self.sumo_running:
                try:
                    self.sumo.end()
                except Exception:
                    pass
                self.sumo_running = False
            
            # 1. Determine scenario configuration
            self._scenario = scenario
            
            try:
                # 2. Start SUMO with the scenario-specific config
                self.sumo.start(seed=seed)
                self.sumo_running = True
            except Exception as e:
                print(f"Error starting SUMO: {e}")
                raise
                
        return self._get_all_agent_states()

    def _get_all_agent_states(self):
        """Collects and stacks states for all traffic light agents."""
        if not self.use_sumo:
            # Return dummy states for testing
            return torch.zeros((self.num_agents, STATE_DIM), device=DEVICE)
        
        states = []
        try:
            for tls_id in self.sumo.tls_ids:
                raw_state = self.sumo.get_state(tls_id)
                state_tensor = torch.tensor(raw_state, dtype=torch.float32, device=DEVICE)
                states.append(state_tensor)
        except Exception as e:
            print(f"Error getting states: {e}")
            raise
            
        # Stack to a single tensor: (NUM_AGENTS, STATE_DIM)
        return torch.stack(states)

    def step(self, actions):
        """
        Performs a simulation step.
        actions: (NUM_AGENTS) tensor of action indices.
        """
        self.current_step += 1
        
        if not self.use_sumo:
            # Return dummy values for testing
            next_states = torch.zeros((self.num_agents, STATE_DIM), device=DEVICE)
            rewards = torch.zeros((self.num_agents, 1), device=DEVICE)
            costs = torch.zeros((self.num_agents, 1), device=DEVICE)
            done = self.current_step >= MAX_STEPS_PER_EPISODE
            return next_states, rewards, costs, done, {}
            
        try:
            # 1. Apply actions to SUMO
            for i, tls_id in enumerate(self.sumo.tls_ids):
                # Ensure action is an integer for TraCI
                phase_index = actions[i].item() 
                self.sumo.apply_action(tls_id, phase_index)
                
            # 2. Advance simulation and update metrics
            self.sumo.step()
            
            # 3. Get new states
            next_states = self._get_all_agent_states()
            
            # 4. Get rewards and costs (Global metrics applied to all agents)
            # The reward and cost are global metrics calculated over the entire network.
            global_reward, global_cost = self.sumo.get_global_metrics()

            # Rewards/Costs are applied to all agents: (NUM_AGENTS, 1)
            rewards = torch.full((self.num_agents, 1), global_reward, device=DEVICE)
            costs = torch.full((self.num_agents, 1), global_cost, device=DEVICE)
            
            # 5. Check if episode is done
            # Check for expected vehicles in the network. Import TraCI lazily
            # so that the module can be imported even when TraCI is not installed.
            min_expected = None
            try:
                import traci as _traci
                min_expected = _traci.simulation.getMinExpectedNumber()
            except Exception:
                # If TraCI isn't available or the call fails, we don't
                # use the min_expected criterion to end the episode.
                min_expected = None

            if min_expected is None:
                done = self.current_step >= MAX_STEPS_PER_EPISODE
            else:
                done = self.current_step >= MAX_STEPS_PER_EPISODE or min_expected == 0
            
            info = {
                'global_reward': global_reward,
                'global_cost': global_cost,
                'scenario': self._scenario
            }
            
            return next_states, rewards, costs, done, info
            
        except Exception as e:
            print(f"Error during simulation step: {e}")
            raise

    def close(self):
        """Closes the environment and SUMO simulation."""
        if self.use_sumo:
            try:
                self.sumo.end()
                self.sumo_running = False
            except Exception as e:
                print(f"Error closing SUMO: {e}")
                
    def get_global_metrics(self):
        """Return global reward and cost from the SUMO interface or dummy values.

        Returns:
            (reward: float, cost: float)
        """
        if not self.use_sumo:
            return 0.0, 0.0

        try:
            return self.sumo.get_global_metrics()
        except Exception as e:
            print(f"Error retrieving global metrics from SUMO: {e}")
            return 0.0, 0.0