import pickle
from crossing import *
from streets import *
from settings import *
from car import *

class City:
    def __init__(self):
        self.crossings = []
        self.streets = []
        self.selectedobj = 0
        self.selcrossings = {}

    def get_cars(self):
        cars = []
        for s in self.streets:
            cars = cars + s.get_cars()
        for s in self.crossings:
            cars = cars + s.get_cars()
        return cars

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

    def update01(self):
        for obj in self.streets:
            if not obj.update01():
                self.streets.remove(obj)

    def draw(self,screen):
        for obj in self.streets + self.crossings:
            obj.draw(screen)

    def update(self):
        for obj in self.streets + self.crossings:
            obj.update()
        crashes = []
        cars = []
        for obj in self.streets + self.crossings:
            crashes += obj.crash
            cars += obj.get_cars()
        return cars, crashes
    
    def load(self, filename='city.pckl'):
        city = self
        try:
            with open(filename, 'rb') as cityfile:
                city = pickle.load(cityfile)
        except:
            print('no saved streets and crossings')
        return city
            

    def delete_cars(self):
        for obj in self.streets + self.crossings:
            obj.cars = []
    
    def save(self, filename='city.pckl'):
        self.delete_cars()
        with open('city.pckl', 'wb') as city:
            pickle.dump(self, city)
