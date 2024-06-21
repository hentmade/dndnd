from Cell import *
from Figure import *
from Item import *
from Event import *
from Map import *

class GameField:
    # ---------------------------------------- Field -------------------------------------------------
    def __init__(self, height, width,map):
        self.height = height
        self.width = width
        self.map = map
        self.cells = [[Cell((x, y)) for y in range(height)] for x in range(width)]
        self.initialize_GameField
        self.field_corners = []
        self.overlay = None
    
    def initialize_GameField(self):
        for row in self.cells:
            for cell in row:
                cell.set_visu_state(None)
        self.map.num_cells_x = self.width
        self.map.num_cells_y = self.height        
                
    def get_cell(self,position):
        x,y = position
        return self.cells[x][y]       

    # ---------------------------------------- Figure ------------------------------------------------
    def add_figure(self,name,type, position,size=1):
        return self.get_cell(position).add_figure(name,type,size)
    
    def move_figure(self,figure,start_position,end_position):
        figure.position = end_position
        start_cell = self.get_cell(start_position)
        end_cell = self.get_cell(end_position)
        start_cell.figure = None
        end_cell.figure = figure 
        if end_cell.event is not None:
            self.trigger_event(end_position)
            self.set_visu_state(end_position, end_cell.event.type)
            self.remove_event(end_position)
        
    def remove_figure(self,position):
        self.get_cell(position).remove_figure(position)


    # ------------------------------------------- Event -----------------------------------------------
    def add_event(self, type, position, size=1):
        self.get_cell(position).add_event(type,size)

    def trigger_event(self,position):
        self.get_cell(position).trigger_event()

    def remove_event(self,position):
        self.get_cell(position).remove_event()

    # -------------------------------------------- Item ------------------------------------------------
    # ToDo: Muss Item heißen // Item noch nicht implementiert
    def add_item(self, position, obj_type):
        self.get_cell(position).obj = Object(obj_type) 

    # ---------------------------------------- Visualisation --------------------------------------------
    def set_visu_state(self, position, visu_state):
        cell = self.get_cell(position)
        cell.set_visu_state(visu_state)
        self.map.add_overlay(cell.visu_state,position)




                


        


