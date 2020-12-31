import pygame
from pygame.locals import *
import numpy as np
from crossing import *
from streets import *
from car import *
from crash import *
from settings import *






class game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.streets = []
        self.crossings = []
        self.cars = []
        self.mode = 0
        self.selectedobj = 0
        self.selcrossings = {}
        self.crashes = []
        self.shot = 0
        """
        0: create crossings
        1: create streets
        2: run game
        """

    def get_cars(self):
        self.cars = []
        for s in self.streets:
            self.cars = self.cars + s.get_cars()
        for s in self.crossings:
            self.cars = self.cars + s.get_cars()

    def select_crossing(self,pos):
        for obj in self.crossings:
            if obj.select(pos):
                self.selectedobj = obj
                break
        if self.selectedobj == 0:
            return False
        else:
            return True

    def select_street(self,pos):
        for obj in self.streets:
            if obj.select(pos):
                self.selectedobj = obj
                break
        if self.selectedobj == 0:
            return False
        else:
            return True


    def create_crossing(self,pos):
        self.selectedobj = Crossing(tuple(pos.astype(int)))
        self.crossings.append(self.selectedobj)

    def create_street(self, connections):
        self.selectedobj = Street(connections)
        connections[1].connect(len(connections[1].connections) + 1, self.selectedobj)
        connections[2].connect(len(connections[2].connections) + 1, self.selectedobj)
        self.streets.append(self.selectedobj)

    def remove_obj(self):
        print('sel', self.selectedobj)
        try:
            if self.selectedobj.type == "street":
                self.streets.remove(self.selectedobj)
            elif self.selectedobj.type == "crossing":
                self.crossings.remove(self.selectedobj)
            elif self.selectedobj.type == "car":
                self.selectedobj.location.emit(self.selectedobj)
        except:
            pass
        self.selectedobj = 0

    def handle_events_crossings(self, event):
        if event.type == QUIT:
            pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            pos = np.array(event.pos)
            if not self.select_crossing(pos):
                self.create_crossing(pos)
        elif event.type == MOUSEBUTTONUP:
            self.selectedobj = 0
        elif event.type == MOUSEMOTION and self.selectedobj!=0:
            self.selectedobj.change(event.pos)
        elif event.type == KEYDOWN:
            print(event.key)
            if event.key == 100: # press 'd'
                self.selectedobj.disconnect()
                self.remove_obj()
            elif event.key == 32:
                self.selectedobj = 0
                self.selcrossings = {}
                self.mode = 1
                print('street mode')
            elif event.key == 99: #press 'c'
                color = tuple([np.random.randint(255) for x in range(3)])
                Car(self.selectedobj, color=color) 
                

    def handle_events_streets(self, event):
        if event.type == QUIT:
            pygame.quit() 
        elif event.type == MOUSEBUTTONDOWN:
            pos = np.array(event.pos)
            if self.select_crossing(pos):
                if len(self.selcrossings)==0:
                    self.selcrossings[1] = self.selectedobj
                elif len(self.selcrossings)==1:
                    self.selcrossings[2] = self.selectedobj
                    print(self.selcrossings)
                    self.create_street(self.selcrossings)
                    self.selcrossings = {}
        elif event.type == MOUSEBUTTONUP:
            self.selectedobj = 0
        if event.type == KEYDOWN:
            print(event.key)
            if event.key == 100: # press 'd'
                self.remove_obj()
            elif event.key == 32: # press 'blank'
                self.selectedobj = 0
                self.selcrossings = {}
                self.mode = 2
                print('run mode')

    def handle_events_run(self,event):
        if event.type == QUIT:
            pygame.quit() 
        elif event.type == KEYDOWN:
            print(event.key)
            if event.key == 32: # 'blank'
                self.mode = 0 
                print('crossing mode')
       

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
        for obj in self.streets:
            if not obj.update01():
                self.streets.remove(obj)
    
        self.cars = []
        for obj in self.streets + self.crossings:
            self.cars += obj.get_cars()
            
        for obj in self.streets + self.crossings +self.cars:
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
            car.update()

        # animation
        for i in range(steps_between_decisions):
            self.screen.fill(screen_color)
            for obj in self.streets + self.crossings + self.crashes:
                obj.draw(self.screen)
            for c in self.cars:
                c.update(decide=False)
                c.draw(self.screen)
            self.clock.tick(int(steps_between_decisions/time_between_decisions))
#           pygame.image.save(self.screen, "{}.png".format(self.shot))
#           self.shot += 1

            pygame.display.flip()

        for obj in self.streets + self.crossings:
            obj.update()
        
       #for car in self.cars:
            # pass feedback to learner
            
         
        self.crashes = []
        self.cars = []
        for obj in self.streets + self.crossings:
            self.crashes = self.crashes + obj.crash
            self.cars += obj.get_cars()
              

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
