import numpy as np
import pygame
from crash import *
from settings import *

class Car:
    def __init__(self, location, color=car_color):
        # cars can only be initiated on crossings
        if location.type=="crossing":
            self.location = location
            self.container = location
            self.source = None
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
            self.container.cars.append(self)

        
    def dest_choices(self):
        all_choices = self.location.connections
        ac = dict(all_choices)
        if self.source != None and len(all_choices)>1:
            for key in all_choices:
                if all_choices[key] == self.source:
                    ac.pop(key)
        return ac

    def choose_dest(self):
        ch = self.dest_choices()
        chlist = [x for x in ch]
       #print('chlist', chlist)
        x = np.random.randint(len(chlist))
       #print('x', x)
        self.destination = self.location.connections[chlist[x]]

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
        info = sum([3**x for x in self.cars]) + 2*3**ownprior
        self.priority = ownprior
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
        self.feedback = 0
        if decide:
            if act==None:
                act = self.chosen_action()
            a = self.int2choices(act)
            if a[0]:
                self.enter(a[1])
                self.feedback = reward_amount
            else:
                self.source = self.location
                self.feedback = 0
            self.choose_dest()
           #rv = [np.random.randint(100) for x in range(2)]
           #rv = (rv/np.linalg.norm(rv)*self.radius/2).astype(int)
            self.target_coord = np.array(self.container.get_coordinates(),dtype=int)# + rv
            self.delta = (self.target_coord - self.floatcoord)/steps_between_decisions
        else:
            self.floatcoord = self.floatcoord + self.delta
            self.coord = tuple(self.floatcoord.astype(int))
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.coord, self.radius)
         
        
        
                 
        
        
