from Figure import *
from enum import Enum
from Event import *
from Figure import Figure
import cv2


class VisuState(Enum):
    EARTH = 'e'
    WATER = 'w'
    FIRE = 'f'
    MOUNTAIN = 'm'   


class VisuState_Img(Enum):
    TRAP = 'Assets\\overlay.png'


class Cell:
    def __init__(self, position):
        self.position = position
        self.figure = None
        self.obj = None
        self.event = None
        self.terrain = None
        self.visu_state = None
        self.visu_img = None

    def set_visu_state(self,state):
        if state is not None:
            self.visu_state = VisuState(state).value
        else:
            self.visu_state=None

    def set_visu_img(self, state):
        if state is not None:
            self.visu_img = VisuState_Img(state).value
            #self.visu_img = cv2.imread(visu_img_path)
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

    def trigger_event(self):
        if self.event is not None:
            self.event.trigger
            self.remove_event


        
        



        