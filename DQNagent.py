import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

class DQNagent:
    def __init__(self):
        self.greedy = 0.9
        self.learning_rate = 0.001  
        self.net = self.build_model(self.learning_rate)
        self.target_net = self.build_model(self.learning_rate)
    @staticmethod
    def build_model(lr):
        qnetz = Sequential()
        qnetz.add(Dense(10000,input_dim = 5, activation =
'relu',kernel_initializer = 'he_uniform'))
       # qnetz.add(Dense(2048,activation = 'relu',kernel_initializer = 'he_uniform'))
        qnetz.add(Dense(4,activation = 'linear',kernel_initializer = 'he_uniform'))
        qnetz.compile(optimizer=tf.optimizers.Adam(learning_rate=lr),loss='mse')

        return qnetz
 
    def choose_action(self,state):
        if np.random.random() < self.greedy:
            state_input = tf.convert_to_tensor(state[None,:],dtype = tf.float32)
         #   print(state_input)
            action = self.net(state_input)
            action = np.argmax(action.numpy()[0],axis = 0)
            return action
        else:
            return np.random.randint(0,4)
    
    def update_target_net(self):
        self.target_net.set_weights(self.net.get_weights())
    
    def train(self,batch):
        # train the network with a batch of experiences
        state_batch,action_batch,reward_batch,next_state_batch = batch
#        print(batch)
        current_q = self.net(state_batch).numpy()
        target_q = np.copy(current_q)
        next_q = self.target_net(next_state_batch).numpy()
#        print("next Q values are:",next_q)
        max_next_q = np.amax(next_q,axis =1)
        for i in range(state_batch.shape[0]):
            target_q_val = reward_batch[i]
            target_q_val += 0.95 * max_next_q[i]
            target_q[i][action_batch[i]] = target_q_val
        training_history = self.net.fit(x=state_batch,y=target_q,verbose=0)
        loss = training_history.history['loss']
        return loss
    
