from Cell import *
from Terrain import *
from Figure import *
from Item import *
from Event import *

class GameField:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = [[Cell((x, y)) for y in range(height)] for x in range(width)]
        self.field_corners = []

    def initialize_GameField(self):
        for row in self.cells:
            for cell in row:
                cell.set_visu_state(None)
                

    def add_figure(self,name,type, position,size=1):
        x,y = position
        self.cells[x][y].add_figure(name,type,size)

    def add_event(self, type, position, size=1):
        x,y = position
        self.cells[x][y].add_event(type,size)

    def set_terrain(self, position, terrain_type):
        x,y = position
        self.cells[x][y].terrain = Terrain(terrain_type)

    
    def add_object(self, position, obj_type):
        x,y = position
        self.cells[x][y].obj = Object(obj_type)    

    def set_visu_state(self, position, visu_state):
        x,y = position
        self.cells[x][y].set_visu_state(visu_state)

    def visualize_GameField(self):
        for row in self.cells:
            for cell in row:
                if cell.figure is not None:
                    print(f"{cell.figure.type.value}",end=" ")
                elif cell.visu_state is not None:                    
                    print(f"{cell.visu_state}",end=" ")
                else:
                    print(".", end=" ")
            print()       
            
                


        


