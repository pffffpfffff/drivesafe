class crossing:
    def __init__(self):
        self.cars = [] # car: direction the car came from
        self.connections = {} # direction: streetname
      # self.strts = {v: k for k, v in self.connections}
        self.strts = {}  # street: direction
        self.rightlanes = {} # direction: which lane to take

    def emit(self, car):
        if car in self.cars:
            self.cars.remove(car)
        return None

    def accept(self, car):
        if len(self.cars)==0:
            self.cars.append(car)
            feedback = 1
        elif len(self.cars) > 1:
            feedback = self.police(car)
        return feedback
            
    def connect(self, direction, somestreet, ln):
        success = True
        if not (direction in self.connections) and not (somestreet in self.strts):
            self.connections[direction] = somestreet
            self.strts[somestreet] = direction
            self.rightlanes[direction] = ln
        else:
            success = False
            print("Connection could not be established")
        return success

    def disconnect(self, somestreet):
        key = self.strts[somestreet]
        self.strts.pop(somestreet)
        self.connections.pop(key)
        return None

    def police(self,car):
        feedback = 1
        if self.cars[0].source == self:
            del car
            feedback = -100
        elif self.strts[self.cars[0].source] < self.strts[car.position]:
            del car
            feedback = -100
        else:
            del self.cars[0]
            self.cars.append(car)
        return feedback
          
    

            
