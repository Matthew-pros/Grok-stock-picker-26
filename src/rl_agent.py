import numpy as np
import pandas as pd
from collections import defaultdict
import json
import os
from datetime import datetime

class QLearningAgent:
    def __init__(self, actions=20, learning_rate=0.1, discount=0.95, epsilon=0.1):
        self.q_table = defaultdict(lambda: np.zeros(actions))
        self.lr = learning_rate
        self.gamma = discount
        self.epsilon = epsilon
        self.actions = actions  # Počet akcií k výběru (0-20)
        self.history_file = 'data/portfolio_history.json'
    
    def get_state(self, features):
        # State: Vektor [edge_mean, momentum_mean, sentiment_mean] – zjednodušené
        return tuple(np.round(features, 2))
    
    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.randint(0, self.actions)  # Explore
        return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        next_max_q = np.max(self.q_table[next_state])
        new_q = current_q + self.lr * (reward + self.gamma * next_max_q - current_q)
        self.q_table[state][action] = new_q
    
    def rebalance(self, screened_df):
        # Simulace: State z průměrných features, akce = vybrat top N (N=action)
        features = screened_df[['edge', 'er']].mean().values  # Placeholder features
        state = self.get_state(features)
        action = self.choose_action(state)  # Vyber počet akcií
        top_picks = screened_df.head(action).to_dict('records')
        
        # Ulož historii
        history = self.load_history()
        history[datetime.now().isoformat()] = {'picks': top_picks, 'action': action}
        with open(self.history_file, 'w') as f:
            json.dump(history, f)
        
        return top_picks
    
    def learn_from_past(self):
        # Reward: Historické returny z yfinance
        history = self.load_history()
        for date, data in history.items():
            if len(data['picks']) > 0:
                # Fetch return pro první pick (simplifikováno)
                ticker = data['picks'][0]['ticker']
                # Použij yfinance pro return od data do teď
                reward = np.random.normal(0.05, 0.02)  # Placeholder – implementuj real return
                features = np.array([0.05, 0.07])  # Past features
                state = self.get_state(features)
                next_features = np.array([0.06, 0.08])  # Hypotetické next
                next_state = self.get_state(next_features)
                self.update(state, data['action'], reward, next_state)
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {}
