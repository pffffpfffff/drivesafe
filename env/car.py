import numpy as np
import pygame
from env.crash import *
from env.settings import *

class Car:
    def __init__(self, location, color=car_color):
        # cars can only be initiated on crossings
        if location.type=="crossing":
            self.location = location
            self.container = location
            self.source = location
            self.destination = None
            self.choose_dest()
            self.cars = [] # directions from which other cars are coming
            self.coord = self.container.get_coordinates()
            self.floatcoord = np.array(self.coord)
            self.target_coord = np.array(self.coord)
            self.delta = np.array([0,0])
            self.color = color
            self.radius = car_size
            self.type = "car"
            self.priority = 100
            self.feedback = 0
            self.state = 0
            self.new_state = 0
            self.action = 0
            self.container.cars.append(self)
            self.highlight = False

        
    def dest_choices(self):
        all_choices = self.location.connections
        ac = dict(all_choices)
        if (self.source != None) and (len(all_choices)>1):
            for key in all_choices:
                if all_choices[key] == self.source:
                    ac.pop(key)
        return ac

    def choose_dest(self):
        ch = self.dest_choices()
        chlist = [x for x in ch]
       #print('chlist', chlist)
       #print('x', x)
        try:
            x = np.random.randint(len(chlist))
            self.destination = self.location.connections[chlist[x]]
        except:
            print('Error in choose_dest')
            print('chlist', chlist)
           #print('x', x)

    def chosen_action(self):
        return np.random.randint(4)

    def info(self):
        ownprior = 0
        self.cars = []
        if len(self.destination.get_cars()) > 0:
            self.cars.append(0)
        for x in self.destination.connections:
            for c in self.destination.connections[x].get_cars():
                if c.destination == self.destination:
                    if c==self:
                        ownprior = x
                    else:
                        self.cars.append(x)
        self.cars = list(set(self.cars))
        # car is on the right lane, if self.container.forward and
        # self.destination == self.location.connections[1] or if
        # not(self.container.forward) and self.destination ==
        # self.location.connections[0]
        # All this only applies on streets
        self.priority = ownprior
        if self.location.type == "street":
            fwfw = self.container.forward and (self.destination == self.location.connections[2])
            bwbw = not(self.container.forward) and (self.destination == self.location.connections[1])
            if fwfw or bwbw:
                self.priority = ownprior
                info = sum([10**x for x in self.cars]) + 2*10**ownprior
            else:
                self.priority = ownprior + 0.5
                info = sum([10**x for x in self.cars]) + 4*10**ownprior
        else:
            info = sum([10**x for x in self.cars]) + 2*10**ownprior
        return info
    
    def int2choices(self, i, leng=2):
        b = [bool(int(x)) for x in bin(i)[2:]]
        a = [False for x in range(leng - len(b))]
        return a + b
        

    def enter(self, lane):
        if self.destination.type == "crossing":
            self.container.emit(self)
            self.destination.accept(self)
        elif self.destination.type == "street":
            self.container.emit(self)
            self.destination.accept(self, lane)
        
    def update(self, act=None, decide=True):
        if decide:
            self.feedback = 0
            if act==None:
                act = self.chosen_action()
            a = self.int2choices(act)
            if a[0]:
                self.enter(a[1])
                self.feedback = reward_amount
            else:
                self.source = self.location
            self.choose_dest()
           #rv = [np.random.randint(100) for x in range(2)]
           #rv = (rv/np.linalg.norm(rv)*self.radius/2).astype(int)
            self.target_coord = np.array(self.container.get_coordinates(),dtype=int)# + rv
            self.delta = (self.target_coord - self.floatcoord)/steps_between_decisions
        else:
            self.floatcoord = self.floatcoord + self.delta
            self.coord = tuple(self.floatcoord.astype(int))
        
    def draw(self, surface):
        if self.highlight:
            pygame.draw.circle(surface, (255,0,0), self.coord, int(self.radius*1.1))
        pygame.draw.circle(surface, self.color, self.coord, self.radius)
         
        
        
                 
        
        
