import pygame
from pygame.locals import *
import numpy as np
from env.crossing import *
from env.streets import *
from env.car import *
from env.crash import *
from env.settings import *
from env.city import *
from RL import *
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
        self.learner = QLearner()
        if loadlearner:
            print("loaded")
            self.agent.net = tf.keras.models.load_model('./tmp/nmqnet')
            self.agent.target_net = tf.keras.models.load_model('./tmp/nmtarget_net')
            self.agent.greedy = qgreed
            self.learner = self.learner.load()
            self.learner.set_greedy(qgreed)
        self.crashcounter = 0
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
            car.action = self.learner.choose_action(car.state)
            car.update(act=car.action)
#           car.update()


        cars_, self.crashes = self.city.update()
        self.crashcounter += len(self.crashes)
        
        for car in self.cars:
            # pass feedback to learner
            car.new_state = car.info()
            self.learner.learn(car.state, car.action ,car.feedback,car.new_state) 
            car.state = car.new_state
        
        self.cars = cars_
        for car in self.cars:
            car.state = car.info()

    def run2dqn(self):
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
#
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

              
    def run(self,method = 'dqn',max_episode = 2000):
        crashcount = []
        if method == 'ql':
            for i in range(max_episode):
                self.run2()
                if i % 20 == 0:
                    crashcount.append(self.crashcounter)
            self.learner.save()
        elif method == 'dqn':
            for i in range(10000):
                self.run2dqn()
                if i % 20 ==0:
                    crashcount.append(self.crashcounter)
                    print(self.crashcounter)
            for episode in range(max_episode):
                self.agent.learning_rate = 0.005
                self.run2()          
                experience_batch = self.buffer.sample()
                loss = self.agent.train(experience_batch)
        
            
                if episode % 20 == 0:
                    self.agent.update_target_net()
            tf.saved_model.save(self.agent.net,'./tmp/nmqnet')
            tf.saved_model.save(self.agent.target_net,'./tmp/nmtarget_net')       
        crashcount = np.array(crashcount)
        np.savez("dqn",crashcount)   

game().run(method = 'dqn',max_episode = 10000)

#dra = np.load("random.npz")
#drb = np.load("ql.npz")
#drc = np.load("dqn.npz")
#a = dra['arr_0']
#b = drb['arr_0']
#c = drc['arr_0']
#plt.figure()
#plt.plot(a,'r')
#plt.plot(b,'b')
#plt.plot(c,'g')
#plt.savefig('performence.png',dpi=1200)


