import cv2
import numpy as np


class Map:
    def __init__(self, image_path):
        self.background = cv2.imread(image_path)
        self.foreground = []
        self.num_cells_x = None
        self.num_cells_y = None

    
    def rotate_map(self, angle):
        h, w = self.background.shape[:2]
        center = (w // 2, h // 2)
        # Calculate the size of the new image
        abs_cos, abs_sin = abs(np.cos(np.radians(angle))), abs(np.sin(np.radians(angle)))
        bound_w = int(h * abs_sin + w * abs_cos)
        bound_h = int(h * abs_cos + w * abs_sin)
        # Adjust the rotation matrix to the center and apply the padding
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotation_matrix[0, 2] += bound_w / 2 - center[0]
        rotation_matrix[1, 2] += bound_h / 2 - center[1]
        rotated_img = cv2.warpAffine(self.background, rotation_matrix, (bound_w, bound_h))
        self.background = rotated_img
        return self.background
    

    def resize_map(self, width=None, height=None):
        #ToDo: Width und Height der Map müssen noch richtig erkannt und skaliert werden für die Anzeige        
        self.background = cv2.resize(self.background, (950,760))
        return self.background
    

    def put_foreground(self):
        if self.foreground:
            for image in self.foreground:
                factor = image["factor"]
                self.num_cells_x, self.num_cells_y = 50, 40 #ToDo: automatische Erkennung der Zellen-Anzahl! 

                # Berechne die Größe jeder Zelle
                cell_width = self.background.shape[1] // self.num_cells_x
                cell_height = self.background.shape[0] // self.num_cells_y

                overlay = cv2.imread(image["path"],cv2.IMREAD_UNCHANGED)
                overlay_resized = cv2.resize(overlay, (cell_width*factor, cell_height*factor), interpolation=cv2.INTER_LINEAR)

                # Prüfe, ob das PNG-Bild einen Alpha-Kanal hat
                if overlay_resized.shape[2] == 4:
                    # Extrahiere die Alpha-Maske des PNG-Bildes und die RGB-Farben
                    alpha_mask = overlay_resized[:, :, 3] / 255.0
                    overlay_colors = overlay_resized[:, :, :3]

                    # Bestimme die Region, wo das Overlay platziert werden soll
                    # Hier platzieren wir das Overlay in der ersten Zelle
                    x_offset, y_offset = image["position"]
                    y1, y2 = (y_offset-factor//2)*cell_height, (y_offset-factor//2)*cell_height + overlay_resized.shape[0]
                    x1, x2 = (x_offset-factor//2)*cell_width, (x_offset-factor//2)*cell_width + overlay_resized.shape[1]

                    # Mische die beiden Bilder
                    for c in range(0, 3):
                        try:
                            self.background[y1:y2, x1:x2, c] = (1. - alpha_mask) * self.background[y1:y2, x1:x2, c] + alpha_mask * overlay_colors[:, :, c]
                        except:
                            print("")
                        else:
                            print("")
                        
    
    def add_overlay(self,path,position,factor=1):
        self.foreground.append({"path": path, "position": position, "factor": factor})

    def remove_overlay(self,path,position,factor=1):
        self.foreground.remove({"path": path, "position": position, "factor": factor})
        self.background = original_background


    def display_map(self, window_name='Image',factor=1):        
        try:
            cv2.destroyWindow(window_name)
        except:
            #cv2.waitKey()
            self.put_foreground()    
            cv2.imshow(window_name, self.background)            
        else:        
            self.put_foreground()    
            cv2.imshow(window_name, self.background) 
            

    def figure_radius(self,position,size=1):    
        global original_background
        x,y = position
        original_background = self.background.copy()   
        i = 0 
        
        self.add_overlay("Assets\\player_radius.png",(x,y),factor=size*5)
     
        
        self.display_map("Map",factor=5*size)
        cv2.waitKey(0)
