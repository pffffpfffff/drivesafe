import pygame
from pygame.locals import *
import numpy as np
from crossing import *
from streets import *
from car import *
from crash import *
from settings import *
from city import *
#from RL import *

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
#       self.learner = QLearner()
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
#       pygame.image.save(self.screen, "{}.png".format(self.shot))
#       self.shot += 1
            
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
#           car.update(act=self.learner.choose_action(car.info())
            car.update()

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
    #           pygame.image.save(self.screen, "{}.png".format(self.shot))
    #           self.shot += 1

                pygame.display.flip()

        self.cars, self.crashes = self.city.update()
        
       #for car in self.cars:
            # pass feedback to learner
           #self.learner.learn(car.info(), car.last_action ,r,s_ 
            
         
              

    def run(self):
        while True:
            self.handle_events()
            if self.mode==0:
                self.run01()
            elif self.mode==1:
                self.run01()
            elif self.mode==2:
                self.run2()



game().run()
