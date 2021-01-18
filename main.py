import pygame
from pygame.locals import *
import numpy as np
from env.streets import *
from env.car import *
from env.crash import *
from env.settings import *
from env.city import *
from RL import *
from DQNagent import *
from ReplayBuffer import *

class game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
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
            self.agent.net = tf.keras.models.load_model('./tmp/nmqnet')
            self.agent.target_net = tf.keras.models.load_model('./tmp/nmtarget_net')
            self.learner = self.learner.load()
            if train:
                self.learner.set_greedy(qgreed)
                self.agent.greedy = qgreed
            else:
                print('no training')
                self.learner.set_greedy(1)
                self.agent.greedy = 1
        """
        0: create crossings
        1: create streets
        2: run game
        """

    def handle_events_crossings(self, event):
        if event.type == QUIT:
            pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            pos = np.array(event.pos)
            if not self.city.select_crossing(pos):
                self.city.create_crossing(pos)
        elif event.type == MOUSEBUTTONUP:
            self.city.selectedobj = 0
        elif event.type == MOUSEMOTION and self.city.selectedobj!=0:
            self.city.selectedobj.change(event.pos)
        elif event.type == KEYDOWN:
            print(event.key)
            if event.key == 100: # press 'd'
                self.city.selectedobj.disconnect()
                self.city.remove_obj()
            elif event.key == 32:
                self.city.selectedobj = 0
                self.city.selcrossings = {}
                self.mode = 1
                print('street mode')
            elif event.key == 99: #press 'c'
                color = tuple([np.random.randint(255) for x in range(3)])
                Car(self.city.selectedobj, color=color) 
            elif event.key == 115: # press 's'
                self.city.save()
                

    def handle_events_streets(self, event):
        if event.type == QUIT:
            pygame.quit() 
        elif event.type == MOUSEBUTTONDOWN:
            pos = np.array(event.pos)
            if self.city.select_crossing(pos):
                if len(self.city.selcrossings)==0:
                    self.city.selcrossings[1] = self.city.selectedobj
                elif len(self.city.selcrossings)==1:
                    self.city.selcrossings[2] = self.city.selectedobj
                    print(self.city.selcrossings)
                    self.city.create_street(self.city.selcrossings)
                    self.city.selcrossings = {}
        elif event.type == MOUSEBUTTONUP:
            self.city.selectedobj = 0
        if event.type == KEYDOWN:
            print(event.key)
            if event.key == 100: # press 'd'
                self.city.remove_obj()
            elif event.key == 115: # press 's'
                self.city.save()
            elif event.key == 32: # press 'blank'
                self.city.selectedobj = 0
                self.city.selcrossings = {}
                self.mode = 2
                print('run mode')

    def handle_events_run(self,event):
        global animate
        if event.type == QUIT:
            self.learner.save()
            pygame.quit() 
        elif event.type == KEYDOWN:
            print(event.key)
            if event.key == 32: # 'blank'
                self.mode = 0 
                print('crossing mode')
            elif event.key == 97: # 'a'
                animate = not(animate)
       

    def handle_events(self):
        for event in pygame.event.get():
            if self.mode==0:
                self.handle_events_crossings(event)
            elif self.mode==1:
                self.handle_events_streets(event)
            elif self.mode==2:
                self.handle_events_run(event)

    def run01(self):
        self.screen.fill(screen_color)
        self.city.update01() 
        self.cars = self.city.get_cars()
        self.city.draw(self.screen)    
        for obj in self.cars:
            obj.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(int(steps_between_decisions/time_between_decisions))
        if video:
            pygame.image.save(self.screen, "{}.png".format(self.shot))
            self.shot += 1
            
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

        if animate:
            # animation
            for i in range(steps_between_decisions):
                self.screen.fill(screen_color)
                self.city.draw(self.screen)
                for crash in self.crashes:
                    crash.draw(self.screen)
                for c in self.cars:
                    c.update(decide=False)
                    c.draw(self.screen)
                self.clock.tick(int(steps_between_decisions/time_between_decisions))
                if video:
                    pygame.image.save(self.screen, "{}.png".format(self.shot))
                    self.shot += 1

                pygame.display.flip()

        cars_, self.crashes = self.city.update()
        
#       # DEBUG
#       try:
#           print('INFO: ', self.cars[0].state, self.cars[0].action, 'feedback: ', self.cars[0].feedback, self.cars[0].new_state)
#           print(self.learner.q_table)
#           self.cars[0].highlight = True
#           self.cars[0].draw(self.screen)
#           pygame.display.flip()
#           self.clock.tick(1) 
#           if self.cars[0].state == 747:
#               print('cars', self.cars[0].cars)
#               print('priority', self.cars[0].priority)
#               input('press any key')
#           self.cars[0].highlight = False
#       except:
#           print('No cars')

        if train:
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
        if animate:
            # animation
            for i in range(steps_between_decisions):
                self.screen.fill(screen_color)
                self.city.draw(self.screen)
                for crash in self.crashes:
                    crash.draw(self.screen)
                for c in self.cars:
                    c.update(decide=False)
                    c.draw(self.screen)
                self.clock.tick(int(steps_between_decisions/time_between_decisions))
                if video:
                    pygame.image.save(self.screen, "{}.png".format(self.shot))
                    self.shot += 1

                pygame.display.flip()

        cars_, self.crashes = self.city.update()
        
#       # DEBUG
#       try:
#           print('INFO: ', self.cars[0].state, self.cars[0].action, 'feedback: ', self.cars[0].feedback, self.cars[0].new_state)
#           print(self.learner.q_table)
#           self.cars[0].highlight = True
#           self.cars[0].draw(self.screen)
#           pygame.display.flip()
#           self.clock.tick(1) 
#           if self.cars[0].state == 747:
#               print('cars', self.cars[0].cars)
#               print('priority', self.cars[0].priority)
#               input('press any key')
#           self.cars[0].highlight = False
#       except:
#           print('No cars')
        for car in self.cars:
            # pass feedback to learner
            car.new_state = np.array([int(x) for x in format(car.info(),'05')])
 #           print('new state is',car.new_state)        
            self.buffer.store(car.state,car.action,car.feedback,car.new_state)
            car.state = car.new_state
        self.cars = cars_
        for car in self.cars:
            car.state = car.info()

             
    def run(self,method):
        if method =='QL':
             while True:
                self.handle_events()
                if self.mode==0:
                    self.run01()
                elif self.mode==1:
                    self.run01()
                elif self.mode==2:
                    self.run2()
        elif method == 'DQN':
            while True:
                self.handle_events()
                self.run2dqn()

           


game().run(method='DQN') # Available methods: 'QL' and 'DQN'
