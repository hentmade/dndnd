from enum import Enum

class Event_Type(Enum):
    Trap = 'Assets\\overlay_trap.png'
    Fire = 'Assets\\overlay_fire.png'

class Event:
    def __init__(self,type,position,size=1):
        self.type = type
        self.position = position
        self.size=size
        self.triggered = False
    
    def trigger_event(self): 
        print(f"{self.type.name} triggered")
        self.triggered=True






