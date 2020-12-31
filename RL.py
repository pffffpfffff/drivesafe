import numpy as np
import pandas as pd

class QLearning:
    def __init__(self,acts,learning_rate,discount,greedy = 0.9):
        self.acts = acts # list possible actions
        self.lr = learning_rate
        self.discount = discount # forgetting rate
        self.greedy = greedy
        self.q_table = build_qtable(acts)
    
    def bulid_qtable(self,actions):
        table = pd.DataFrame(columns = actions, dtype = np.float64)
        return table

    def choose_actions(self,state):
        if np.random.uniform() < self.greedy:
        #acts greedy
           weighted_actions = self.q_table.loc[state,:]
           action = np.random.choice(weighted_actions[weighted_actions == np.max(weighted_actions)].index)
        else:
            action = np.random.choice(self.acts)
        return action

    def learn(self,s,a,r,s_):
        q_predict = self.q_table.loc[s,a]
#        if s_ != 'terminal':
        q_target = r + self.gamma * self.q_table.loc[s_,:].max()
#        else:
#            q_target = r
        self.q_table.loc[s,a] += self.lr*(q_target - q_predict)
