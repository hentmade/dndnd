from Cell import *
from Terrain import *
from Figure import *
from Item import *
from Event import *
from imageprocessing.ImageProcessor import *

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
        return (Cell)(self.cells[x][y])        

    # ---------------------------------------- Figure ------------------------------------------------
    def add_figure(self,name,type, position,size=1):
        x,y = position
        return (Cell)(self.cells[x][y]).add_figure(name,type,size)
    
    def move_figure(self,figure,start_position,end_position):
        (Figure)(figure).position = end_position
        x,y = start_position
        cell = (Cell)(self.cells[x][y])
        cell.figure = None
        x,y = end_position
        cell = (Cell)(self.cells[x][y])
        cell.figure = figure 
        if cell.event is not None:
            self.trigger_event(end_position)
        
    def remove_figure(self,position):
        x,y = position
        (Cell)(self.cells[x][y]).remove_figure(position)


    # ------------------------------------------- Event -----------------------------------------------
    def add_event(self, type, position, size=1):
        x,y = position
        (Cell)(self.cells[x][y]).add_event(type,size)

    def trigger_event(self,position):
        x,y = position
        (Cell)(self.cells[x][y]).trigger_event()

    def remove_event(self,position):
        x,y = position
        (Cell)(self.cells[x][y]).remove_figure(position)

    # -------------------------------------------- Item ------------------------------------------------
    # ToDo: Muss Item heißen!
    def add_item(self, position, obj_type):
        x,y = position
        (Cell)(self.cells[x][y]).obj = Object(obj_type) 


    # ---------------------------------------- Visualisation --------------------------------------------
    def set_visu_state(self, position, visu_state):
        x,y = position
        (Cell)(self.cells[x][y]).set_visu_state(visu_state)

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


    def set_terrain(self, position, terrain_type):
        x,y = position
        (Cell)(self.cells[x][y]).terrain = Terrain(terrain_type)        
            
                


        


