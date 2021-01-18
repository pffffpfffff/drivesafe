import pygame
from env.crash import *
from env.settings import *
class Lane:
    def __init__(self, forward, coord):
        self.cars = []
        self.forward = forward 
        self.pnts = coord[0:4]
        self.coord = coord[4]
        self.color = lane_color
        # forward=True means that the preferred direction is from connection[1]
        # -> connection[2] of the parent street, otherwise it is reversed
        self.type = "lane"

    def add_car(self,car):
        if car not in self.cars:
            self.cars.append(car)
            car.container = self
        return len(self.cars)

    def emit(self,car):
        if car in self.cars:
            self.cars.remove(car)

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.pnts)
       #pygame.draw.circle(surface, (255,0,0), self.coord, 5)

    def change(self, coord):
        self.pnts = coord[0:4]
        self.coord = coord[4]
    
    def detect_crash(self):
        if len(self.cars) > 1:
            return Crash(self.cars)

    def get_coordinates(self):
        return self.coord

    

