class street:
	def __init__(end1,end2,lanes):
		self.cars = {}
		self.lanes = []
		self.connections = {}
#
#	def direction(self,xing1,xing2)
#	"""
#	for every street, there is a default direction. Namely,
#	a car should only use this street to drive from xing1 to xing2.
#	If a car is involved in a crash when it is driving along a wrong
#	direction, it woul#	"""
#		if self.cross1 == xing1 and self.cross2 == xing2:
#			return True
#		else:
#			return False


	def count_cars(self):
		nums = 0
		for lane in self.lanes:
			nums += len(lane.cars)
		return nums

	def create_lanes(self,left,right):
		while left > 1:
			self.lanes.append(lane(end2,end1))
			left -= 1
		while right >1:
			self.lanes.append(lane(end1,end2))
			right -= 1

