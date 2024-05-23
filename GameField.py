from Cell import *
from Terrain import *
from Figure import *
from Item import *
from Event import *
from ImageProcessor import *

class GameField:
    # ---------------------------------------- Field -------------------------------------------------
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = [[Cell((x, y)) for y in range(height)] for x in range(width)]
        self.field_corners = []
        self.overlay_imgs = []

    def initialize_GameField(self):
        for row in self.cells:
            for cell in row:
                cell.set_visu_state(None)
                
    def get_cell(self,position):
        x,y = position
        return self.cells[x][y]       

    # ---------------------------------------- Figure ------------------------------------------------
    def add_figure(self,name,type, position,size=1):
        return self.get_cell(position).add_figure(name,type,size)
        #x,y = position
        #return (Cell)(self.cells[x][y]).add_figure(name,type,size)
    
    def move_figure(self,figure,start_position,end_position):
        figure.position = end_position
        start_cell = self.get_cell(start_position)
        end_cell = self.get_cell(end_position)
        start_cell.figure = None
        end_cell.figure = figure 
        if end_cell.event is not None:
            self.trigger_event(end_position)
        
    def remove_figure(self,position):
        self.get_cell(position).remove_figure(position)


    # ------------------------------------------- Event -----------------------------------------------
    def add_event(self, type, position, size=1):
        self.get_cell(position).add_event(type,size)

    def trigger_event(self,position):
        self.get_cell(position).trigger_event()

    def remove_event(self,position):
        self.get_cell(position).remove_event(position)

    # -------------------------------------------- Item ------------------------------------------------
    # ToDo: Muss Item heißen // Item noch nicht implementiert
    def add_item(self, position, obj_type):
        self.get_cell(position).obj = Object(obj_type) 


    # ---------------------------------------- Visualisation --------------------------------------------
    def set_visu_state(self, position, visu_state):
        self.get_cell(position).set_visu_state(visu_state)

    def get_overlay_img(self):
        for row in self.cells:
            for cell in row:
                self.overlay_imgs.append({"pfad": f"{cell.visu_img}", "position": cell.position})

    def visualize_GameField(self,imageProcessor):
        for overlay_info in self.overlay_imgs:
            overlay_img = cv2.imread(overlay_info["pfad"])
            # Die Größe des Overlay-Bildes erhalten
            overlay_höhe, overlay_breite, _ = overlay_img.shape
            # Position des Overlay-Bildes
            x_offset, y_offset = overlay_info["position"]
            background = (ImageProcessor)(imageProcessor).image

            # Overlay-Bild auf dem Hintergrundbild platzieren
            background[y_offset:y_offset+overlay_höhe, x_offset:x_offset+overlay_breite] = overlay_img

        # Ergebnis anzeigen
        cv2.imshow("Overlay-Ergebnis", background)

    def visualize_GameField_Terminal(self):
        for row in self.cells:
            for cell in row:
                if cell.figure is not None:
                    print(f"{cell.figure.type.value}",end=" ")
                elif cell.visu_state is not None:                    
                    print(f"{cell.visu_state}",end=" ")
                else:
                    print(".", end=" ")
            print()   


# ToDo Terrain nicht implementiert
    def set_terrain(self, position, terrain_type):
        self.get_cell(position).terrain = Terrain(terrain_type)        
            
                


        


