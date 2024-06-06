from Object import *
from enum import Enum
from Cell import *

class Figure_Type(Enum):
    PLAYER = 'Player'
    ALLY = 'Ally'
    ENEMY = 'Enemy'
    NPC = 'NPC'


class Figure(Object):
    id_counters = {type: 0 for type in Figure_Type}
    def __init__(self,name,type,position,size):
        super().__init__(type,position,size)
        self.name = name
        self.id = f"{type.value}{Figure.id_counters[type]:03d}"
        Figure.id_counters[type] += 1

    def move(self, new_position):
        self.position = new_position
        return self.position
        

    
        