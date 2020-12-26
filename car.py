import numpy as np

class car:
    def __init__(location, lane=0):
        self.location = location
        self.lane = lane
        self.source = None
        self.destination = None
        
    def choices(self):
        all_choices = self.location.connections
        if self.source != None:
            for key in all_choices:
                if all_choices[key] == self.source:
                    all_choices.pop(key)
        return all_choices

    def choose(self):
        ch = self.choices
        chlist = [x for x in ch]
        x = int(np.round(-0.5 + len(chlist)* np.random.random()))
        return chlist[x] # returns key of choice

    def action(self):
        # gather info about other cars

        act = agent(info)
         
        
        
                 
        
        
