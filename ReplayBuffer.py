import numpy as np
from collections import deque
import random

class ReplayBuffer:

    def __init__(self,size=10000):
        self.size = size # the maximal size of the buffer
        self.experience = deque(maxlen = size)

    def store(self,state,action,reward,state_):
        #store the record
        self.experience.append((state, action, reward, state_))

    def get_volume(self):
        #basically tells the length of stored experience
        volume = len(self.experience)
        return volume

    def sample(self):
        batch_size = min(150,self.get_volume())
        sampled_batch = random.sample(self.experience,batch_size)
       # print(sampled_batch)
        state_batch = []
        action_batch = []
        reward_batch = []
        next_state_batch = []
        for experience in sampled_batch:
#            print('experience is',experience)
            state_batch.append(experience[0])
            action_batch.append(experience[1])
            reward_batch.append(experience[2])
            next_state_batch.append(experience[3])
        return np.array(state_batch), np.array(action_batch), np.array(reward_batch), np.array(next_state_batch)
