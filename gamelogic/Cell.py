from Figure import *
from enum import Enum
from Event import *
from Figure import Figure


class VisuState(Enum):
    EARTH = 'e'
    WATER = 'w'
    FIRE = 'f'
    MOUNTAIN = 'm'



class Cell:
    def __init__(self, position):
        self.position = position
        self.figure = None
        self.obj = None
        self.event = None
        self.terrain = None
        self.visu_state = None

    def set_visu_state(self,state):
        if state is not None:
            self.visu_state = VisuState(state).value
        else:
            self.visu_state=None

    def add_figure(self,name,type,size=1):
        self.figure = Figure(name,type,self.position,size)
        return self.figure
    
    def remove_figure(self):
        self.figure = None
        

    def add_event(self,type,size=1):
        if(type =="TRAP"):
            self.event = Trap(type,self.position,size)
        elif(type =="AMBUSH"): 
            self.event = Ambush(type,self.position,size)

    def remove_event(self):
        self.event = None


        
        



        