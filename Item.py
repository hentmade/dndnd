from Object import *
from enum import Enum

class Item_Type(Enum):
    TORCH = 'TO'
    TREASURE = 'TR'    
    
class Item(Object):
    id_counters = {type: 0 for type in Item_Type}
    def __init__(self,name,type,position,size):
        super().__init__(type,position,size)
        self.name = name
        self.id = f"{type.value}{Item.id_counters[type]:03d}"
        Item.id_counters[type] += 1

    def move(self, new_position):
        self.position = new_position
        