import pygame
from pygame.locals import *
import numpy as np
from crossing import *
from streets import *
from car import *
from crash import *
from settings import *
from city import *
from DQNagent import *
from ReplayBuffer import *
import matplotlib.pyplot as plt

class game():
    def __init__(self):
        pygame.init()
#       self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.mode = 0
        self.city = City()
        if loadcity:
            self.city = self.city.load()
            self.mode = 2
        self.cars = []
        self.crashes = []
        self.shot = 0
        self.agent = DQNagent()
        self.buffer = ReplayBuffer()
#        self.learner = QLearner()
        if loadlearner:
            print("loaded")
            self.agent.net = tf.keras.models.load_model('./tmp/nmqnet')
            self.agent.target_net = tf.keras.models.load_model('./tmp/nmtarget_net')
            if train:
                self.agent.greedy = qgreed
            else:
                self.agent.greedy = 1
#            self.learner = self.learner.load()
#            self.learner.set_greedy(qgreed)
        self.crashcounter = 0
#        self.agent.greedy = -1.9
        """
        0: create crossings
        1: create streets
        2: run game
        """

           
    def run2(self):
        """
        structure:
        1) update all objects, cars make their decision where to go next
        2) animate the movement of the cars
        3) when cars have reached their target, detect crashes and collect
           cars that are still there
        """ 
        
        # make decisions for cars
        for car in self.cars:
            car.state = np.array([int(x) for x in format(car.state,'05')])
            car.action = self.agent.choose_action(car.state)
            car.update(act=car.action)
#           car.update()


        cars_, self.crashes = self.city.update()
        self.crashcounter += len(self.crashes)
        
        for car in self.cars:
            # pass feedback to learner
            car.new_state = np.array([int(x) for x in format(car.info(),'05')])
 #           print('new state is',car.new_state)        
            self.buffer.store(car.state,car.action,car.feedback,car.new_state)
            car.state = car.new_state
        self.cars = cars_
        for car in self.cars:
            car.state = car.info()

    def get_experience(self, agent, RPbuffer):
        for car in self.cars:
            state =self.car.state
            action = agent.choose_action(state)
            reward, state_, = car.feedback, car.info()
            state = state_
 
    def train_model(self,max_episode=10000):
       loss_values = []
       for i in range(10000):
            self.run2()
            if i % 20 ==0:
                print(self.crashcounter)
       print('end')
#            print("lr:",self.agent.learning_rate)
       for episode in range(max_episode):
            self.agent.learning_rate = 0.005
            self.run2()          
            experience_batch = self.buffer.sample()
#            print(experience_batch)
#            print("lr:",self.agent.learning_rate)
            loss = self.agent.train(experience_batch)
        
            
            if episode % 20 == 0:
                self.agent.update_target_net()
                print(self.crashcounter)
                print('episode:',episode)
                loss_values.append(loss)
       plt.plot(np.array(loss_values),'r')
       plt.show()
       tf.saved_model.save(self.agent.net,'./tmp/nmqnet')
       tf.saved_model.save(self.agent.target_net,'./tmp/nmtarget_net')       
  
game().train_model()
