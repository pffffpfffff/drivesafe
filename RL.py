import numpy as np
import pickle
import pandas as pd
from settings import *

class QLearner:
    def __init__(self,acts=[0,1,2,3],learning_rate=0.1,discount=0.9,greedy = qgreed):
        self.acts = acts # list possible actions
        self.lr = learning_rate
        self.discount = discount # forgetting rate
        self.greedy = greedy
        self.q_table = self.build_qtable(acts)
    
    def build_qtable(self,actions):
        table = pd.DataFrame(columns = actions, dtype = np.float64)
        #table.append(pd.Series([0]*len(self.acts),index = actions,name=0))
        return table

    def choose_action(self,state):
        self.add_new_state(state)
        if np.random.uniform() < self.greedy:
        #acts greedy
           weighted_actions = self.q_table.loc[state,:]
           action = np.random.choice(weighted_actions[weighted_actions == np.max(weighted_actions)].index)
        else:
            action = np.random.choice(self.acts)
        return action

    def add_new_state(self,state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                    pd.Series([0]*len(self.acts),index = self.q_table.columns,name=state))

    def learn(self,s,a,r,s_):
        """
        s: state
        a: action leading to s_
        r: reward
        s_: the next state after picking the action "a"
        """

        self.add_new_state(s)
        self.add_new_state(s_)
        q_predict = self.q_table.loc[s,a]
#        if s_ != 'terminal':
        q_target = r + self.discount * self.q_table.loc[s_,:].max()
#        else:
#            q_target = r
        self.q_table.loc[s,a] += self.lr*(q_target - q_predict)

    def save(self,name = "qlearner.pkl"):
        with open(name, "wb") as qt:
            pickle.dump(self, qt)

    def load(self,name = "qlearner.pkl"):
        ql = self
        try:
            with open(name, "rb") as qt:
                ql = pickle.load(qt)
        except:
            pass
        return ql
