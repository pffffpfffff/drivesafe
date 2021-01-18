import pygame
import numpy as np
from env.lane import *
from env.settings import *

class Street:
    def __init__(self, connections, lanesfw = 1, lanesbw = 1, lanewidth=lane_size):
        self.connections = connections
    #   self.priorities = {v:k for k,v in self.connections}
    #   key cannot be object reference
        self.end1, self.end2, self.mid = [(0,0),(0,0),(0,0)]
        self.set_coordinates()
        self.lanewidth = lanewidth
      # self.lanes = \
      #     {1:{i: Lane(True, self.lane_coord(i,1)) for i in range(lanesfw)},  \
      #      -1:{i: Lane(False, self.lane_coord(i,-1)) for i in range(lanesbw)}}
        self.fwlanes = [Lane(True, self.lane_coord(i,1)) for i in range(lanesfw)]
        self.bwlanes = [Lane(False, self.lane_coord(i,-1)) for i in range(lanesbw)]
        self.type = "street"
        self.crash = []

    def connect(self, connections):
        self.connections = connections

    def disconnect(self):
        for i in self.connections:
            updconns = dict(self.connections[i].connections)
            for j in self.connections[i].connections:
                if self.connections[i].connections[j]==self:
                    print('connection found')
                    updconns.pop(j)
            self.connections[i].connections = updconns
        self.connections = {}



    def lane_coord(self, i, dirc):
        end1 = np.array(self.end1) 
        end2 = np.array(self.end2) 
        mid = np.array(self.mid) 
        dirv = end2 - end1  # direction vector
        nv = np.array([dirv[1], -dirv[0]])
        nv = nv/np.linalg.norm(nv)
        p1 = tuple((i*self.lanewidth*nv*dirc+ end1).astype(int))
        p2 = tuple((i*self.lanewidth*nv*dirc+ end1 + dirc*nv*self.lanewidth).astype(int))
        p3 = tuple((i*self.lanewidth*nv*dirc+ end2 + dirc*nv*self.lanewidth).astype(int))
        p4 = tuple((i*self.lanewidth*nv*dirc+ end2).astype(int))
        p5 = tuple(((i+0.5)*self.lanewidth*nv*dirc + mid).astype(int))
        return p1, p2, p3, p4, p5
        

    def set_coordinates(self):
        end1 = self.connections[1].get_coordinates()
        end2 = self.connections[2].get_coordinates()
        mid = tuple((0.5*(np.array(end1) + np.array(end2))).astype(int))
        self.end1 = end1
        self.end2 = end2
        self.mid = mid

    def get_coordinates(self):
        return self.mid

    def update01(self):
        if len(self.connections)<2:
            self.disconnect()
            return False
        else:
            self.set_coordinates()
            self.update_lanes()
            return True

    def update(self):
        self.crash = []
        for l in self.fwlanes:
            c = l.detect_crash()
            if c!=None:
                self.crash.append(c)
        for l in self.bwlanes:
            c = l.detect_crash()
            if c!=None:
                self.crash.append(c)
        
        
    def update_lanes(self):
        i = 0
        for l in self.fwlanes:
            l.change(self.lane_coord(i,1))
            i += 1
        i = 0
        for l in self.bwlanes:
            l.change(self.lane_coord(i,-1))
            i+=1

    def count_cars(self):
        nums = 0
        for lane in self.fwlanes:
            nums += len(lane.cars)
        for lane in self.bwlanes:
            nums += len(lane.cars)
        return nums
    
    def get_cars(self):
        cars = [] 
        for l in self.fwlanes:
            cars = cars + l.cars
        for l in self.bwlanes:
            cars = cars + l.cars
        return cars


### def police(self, car, lane):
###     feedback = 1
###     if lane.cars[0].source == self:
###         self.emit(car, lane)
###         feedback = -100
###     elif lane.forward:
###         if self.priorities[lane.cars[0].source] < \
###     self.priorities[car.source]: 
###             self.emit(car,lane)
###     elif not(lane.forward):
###         if self.priorities[lane.cars[0].source] < \
###     self.priorities[car.source]: 
###             self.emit(lane.cars[0])

###     return feedback
 
    def accept(self, car, sideofroad):
        # for now only use one lane in either direction
        car.source = car.location
        car.location = self
       #car.feedback = 1
        # do feedback in car class when entering
        if car.source == self.connections[1]:
            if sideofroad:
                chlane = self.fwlanes[0]
            else:
                chlane = self.bwlanes[0] 

        if car.source == self.connections[2]:
            if sideofroad:
                chlane = self.bwlanes[0]
            else:
                chlane = self.fwlanes[0] 
        chlane.add_car(car)


    def draw(self, surface):
        for l in self.fwlanes:
            l.draw(surface)
        for l in self.bwlanes:
            l.draw(surface)
        pygame.draw.line(surface,line_color, self.end1, self.end2,line_width)

    def select(self, x):
        sel = False
        mid = np.array(self.mid)
        if np.linalg.norm(mid - x) < 30:
            sel = True
        return sel




    
