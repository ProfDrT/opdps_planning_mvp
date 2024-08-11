import numpy as np
from typing import List, Dict

class RLModel:
    def __init__(self, state_size: int, action_size: int, learning_rate: float = 0.1, discount_factor: float = 0.95, epsilon: float = 0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((state_size, action_size))

    def train(self, data: List[Dict]):
        for episode in data:
            state = self._get_state(episode['initial_state'])
            for step in episode['steps']:
                action = self._choose_action(state)
                next_state = self._get_state(step['next_state'])
                reward = step['reward']
                
                # Q-learning update
                current_q = self.q_table[state, action]
                max_next_q = np.max(self.q_table[next_state])
                new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (reward + self.discount_factor * max_next_q)
                self.q_table[state, action] = new_q
                
                state = next_state

    def predict(self, state: Dict) -> int:
        state_index = self._get_state(state)
        return np.argmax(self.q_table[state_index])

    def _choose_action(self, state: int) -> int:
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.action_size)
        return np.argmax(self.q_table[state])

    def _get_state(self, state: Dict) -> int:
        # Convert state dictionary to a unique integer index
        # This is a simple hash function and might need to be improved for complex state spaces
        return hash(frozenset(state.items())) % self.state_size

    def save_model(self, filename: str):
        np.save(filename, self.q_table)

    def load_model(self, filename: str):
        self.q_table = np.load(filename)

# Example usage:
# rl_model = RLModel(state_size=1000, action_size=10)
# training_data = [
#     {
#         'initial_state': {'staff_available': 5, 'patients_waiting': 10},
#         'steps': [
#             {'next_state': {'staff_available': 4, 'patients_waiting': 9}, 'reward': 1},
#             {'next_state': {'staff_available': 3, 'patients_waiting': 8}, 'reward': 1},
#         ]
#     },
#     # ... more episodes ...
# ]
# rl_model.train(training_data)
# best_action = rl_model.predict({'staff_available': 5, 'patients_waiting': 10})