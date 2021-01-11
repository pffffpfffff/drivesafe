resolution = (2800,1800)
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
red = (250,0,0)
darkgreen = (30,150,0)

crash_size = 150
crossing_size = int(crash_size/2)
lane_size = crossing_size
line_width = int(lane_size/3)
car_size = int(lane_size/2*1.1)

screen_color = black
car_color = (240, 50, 0)
crash_color = (240, 240, 0)
line_color = (210, 210, 210)
lane_color = (80, 80, 80)
crossing_color = (80, 80, 80)

steps_between_decisions = 30
time_between_decisions =0.6

spawn_cars = True
spawn_probability = 0.3
car_bound = 0.5 # max number of cars = car_bound*(numbofcrossings + numofstreets)
reward_amount = 1
punishment_amount = -100
train = False

animate = True
loadcity = True

loadlearner = True
qgreed = 0.8

video = False
