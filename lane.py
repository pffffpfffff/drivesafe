class lane:
	def __init__(self,before,nexts):
        self.cars = {}
        self.before = before
        self.nexts = nexts

	def accept(self,car):
        if car.next == self:
            self.cars.append(car)
        else:
            pass

	def emit(self,car):
        if car in self.cars and car.next is not wait:
            self.cars.remove(car)
        else:
            pass

	def direction(self,car)
        if car in self.cars and car.next == self.nexts:
            return True
        else:
            return False

	def is_left(self,street)
		if self.nexts == street.end2 and self.before = street.end1:
			return False
		else:
			return True

	def police(self)
		if len(self.cars) > 1:
			print('CRASH!')
			return -1
		else:
			pass
	

