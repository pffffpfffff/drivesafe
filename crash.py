import pygame
from settings import *

class Crash:
    def __init__(self,cars,size=crash_size):
        self.cars = cars
        self.location = cars[0].location
        self.coord = self.location.get_coordinates()
        self.color = crash_color
        self.size = size
        self.give_feedback()
        self.clean_up()

    def give_feedback(self):
        innocent = 0
        lowpr = 100
        for i in range(len(self.cars)):
            if self.cars[i].priority < lowpr:
                innocent = i
                lowpr = self.cars[i].priority
        for c in self.cars:
            c.feedback = -100
        self.cars[innocent].feedback = 1

    def clean_up(self):
       #for c in self.cars:
       #    c.container.emit(c)
        self.cars[0].container.cars = []
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.coord, self.size)
        
            
        