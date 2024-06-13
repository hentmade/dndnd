from enum import Enum

class Event_Type(Enum):
    TRAP = 'Trap'
    AMBUSH = 'Ambush'

class Event:
    def __init__(self,type,position,size=1):
        self.type = type
        self.position = position
        self.size=size
        self.triggered = False
    
    def trigger(self): 
        print("Event triggered")
        self.triggered=True





