from Figure import *
from enum import Enum
from Event import *
from Figure import *
import cv2


class VisuState(Enum):
    TRAP = 'Assets\\overlay_trap.png'
    AMBUSH = 'Assets\\overlay.png'


class Cell:
    def __init__(self, position):
        self.position = position
        self.figure = None
        self.event = None
        self.visu_state = None


    def add_figure(self,name,type,size=1):
        self.figure = Figure(name,type,self.position,size)
        return self.figure
    
    def remove_figure(self):
        self.figure = None        

    def add_event(self,type,size=1):
        self.event = Event(type,self.position,size)        

    def remove_event(self):
        self.event = None

    def trigger_event(self):
        if self.event is not None:
            self.event.trigger_event()                        

    def set_visu_state(self, state):
        if state is not None:
            if self.event.triggered:
                self.visu_state = state.value
        else: 
            self.visu_state=None

    def get_visu_state(self):
        return self.visu_state

        
        



        