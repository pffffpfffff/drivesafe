import pygame
import numpy as np
from crash import *
from car import *

class Crossing:
    def __init__(self, coord = (0,0), radius=crossing_size, color=crossing_color):
        self.cars = [] # car: direction the car came from
        self.connections = {} # direction: streetname
        self.x = coord[0]
        self.y = coord[1]
        self.radius = radius
        self.color=color
        self.type = "crossing"
        self.crash = []
        self.spawn = spawn_cars

    def emit(self, car):
        if car in self.cars:
            self.cars.remove(car)
        return None

    def get_cars(self):
        return self.cars

    def get_coordinates(self):
        return (self.x, self.y)

    def disconnect(self):
        for i in self.connections:
            updconns = dict(self.connections[i].connections)
            for j in self.connections[i].connections:
                if self.connections[i].connections[j]==self:
                    print('connection found')
                    updconns.pop(j)
            self.connections[i].connections = updconns
        self.connections = {}

    def accept(self, car):
    #   print('crossing ', self, ' car accepted')
        self.cars.append(car)
    #   print('#cars: ', len(self.cars))
        car.source = car.location
        car.location = self
        car.container = self
            
    def connect(self, direction, somestreet):
        success = True
        newstreet = True
        for d in self.connections:
            newstreet = newstreet and not(somestreet==self.connections[d])
        if not (direction in self.connections) and newstreet:
            self.connections[direction] = somestreet
        else:
            success = False
            print("Connection could not be established")
        return success

  # def disconnect(self, somestreet):
  #     key = self.strts[somestreet]
  #     self.strts.pop(somestreet)
  #     self.connections.pop(key)
  #     return None

####def police(self,car):
####    feedback = 1
####    if self.cars[0].source == self:
####        feedback = -100
####    elif self.priorities[self.cars[0].source] < self.priorities[car.position]:
####        feedback = -100
####    else:
####        del self.cars[0]
####        self.cars.append(car)
####    return feedback
          
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
    
    def select(self, x):
        sel = False
        pos = np.array([self.x, self.y])
        if np.linalg.norm(pos - x) < 30:
            sel = True
        return sel

    def unselect(self):
        self.selected = False

    def update(self):
        self.crash = []
    #   print('crossing update: {} car(s)'.format(len(self.cars)), self)
        if len(self.cars) > 1:
            self.crash.append(Crash(self.cars))
        if self.spawn:
            nearcars = len(self.cars)
            for con in self.connections:
                nearcars += len(self.connections[con].get_cars())
            if nearcars == 0 and np.random.random() < spawn_probability:
                Car(self, tuple([np.random.randint(256) for i in range(3)]))

    def change(self, coord):
        self.x, self.y = coord


            
