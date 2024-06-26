import cv2
import numpy as np
from PIL import Image, ImageTk, ImageGrab


overlay_trap = "Assets\\overlay_trap.png"
overlay_fire = "Assets\\overlay_fire.png"


class Map:
    def __init__(self, image_path):
        self.background = cv2.imread(image_path)
        self.foreground = []
        self.num_cells_x = None
        self.num_cells_y = None
        self.original_background = None
        self.map_label = None

    def resize_map(self, scale_factor):
        height, width = self.background.shape[:2]
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        self.background = cv2.resize(self.background, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        return self.background
    


    #ToDO: Für Event noch anpassen!


    #ToDo: draw_event_overlay und draw_figure_radius ist genau dsaselbe nur dass wir den Faktor ausschalten müssen! --> figure_radius noch hier rüber ziehen
    def draw_overlay(self, overlay_path, background, position, size=None):
        #factor = 5 * factor  # Stretch factor

        if size is None:
            factor = 1 
        else: 
            factor = 5 * size
        # Read the overlay image
        overlay_image = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)
        if overlay_image is None:
            print(f"Error: Unable to read overlay image from {overlay_path}")
            return
        # Save the original background image
        if not hasattr(self, 'original_background') or self.original_background is None:
            self.original_background = background.copy()  # Background muss am Anfang unser scaled_image sein! StartKlick: scaled_image als background // NextRound: Bild mit Overlay als background
        # Calculate the size of each cell with higher precision
        cell_height = background.shape[0] / self.num_cells_y  # Number of cells in y-direction
        cell_width = background.shape[1] / self.num_cells_x   # Number of cells in x-direction
        print(f"Cell Height: {cell_height}")
        print(f"Cell Width: {cell_width}")
        # Resize the overlay image to the size of the factor * cell dimensions
        overlay_resized = cv2.resize(overlay_image, (int(cell_width * factor), int(cell_height * factor)), interpolation=cv2.INTER_LINEAR)
        # Get the position on the map
        x, y = position
        print(f"x, y: {x, y}")
        # Calculate the center position
        x_center = x * cell_width + (cell_width / 2)
        y_center = y * cell_height + (cell_height / 2)
        print(f"x_center: {x_center}")
        print(f"y_center: {y_center}")
        # Calculate the top-left corner of the overlay
        x_offset = int(x_center - (overlay_resized.shape[1] / 2))
        y_offset = int(y_center - (overlay_resized.shape[0] / 2))
        print(f"x_offset: {x_offset}")
        print(f"y_offset: {y_offset}")
        # Ensure the overlay fits within the background dimensions
        y1, y2 = y_offset, y_offset + overlay_resized.shape[0]
        x1, x2 = x_offset, x_offset + overlay_resized.shape[1]
        print(f"x1, x2: {x1, x2}")
        print(f"y1, y2: {y1, y2}")
        y1 = max(y1, 0)
        y2 = min(y2, background.shape[0])
        x1 = max(x1, 0)
        x2 = min(x2, background.shape[1])
        print(f"Clipped x1, x2: {x1, x2}")
        print(f"Clipped y1, y2: {y1, y2}")
        # Clip the overlay image if it goes out of the background boundaries
        overlay_clipped = overlay_resized[:y2 - y1, :x2 - x1]
        print(f"Overlay_clipped.shape: {overlay_clipped.shape}")
        # Check if the clipped overlay fits within the background
        if overlay_clipped.shape[0] != (y2 - y1) or overlay_clipped.shape[1] != (x2 - x1):
            print(f"Error: Overlay dimensions {overlay_clipped.shape[:2]} do not match the target area {y2 - y1, x2 - x1}")
            return
        if overlay_clipped.shape[2] == 4:  # If the overlay has an alpha channel
            alpha_mask = overlay_clipped[:, :, 3] / 255.0
            overlay_colors = overlay_clipped[:, :, :3]
            for c in range(0, 3):
                background[y1:y2, x1:x2, c] = (1. - alpha_mask) * background[y1:y2, x1:x2, c] + alpha_mask * overlay_colors[:, :, c]
        # Update the Tkinter window
        self.update_tkinter_image(background)

    def update_tkinter_image(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(rgb_image)
        image_tk = ImageTk.PhotoImage(image_pil)
        self.map_label.config(image=image_tk)
        self.map_label.image = image_tk


    def remove_overlay(self, background):
        if self.original_background is not None:
            background[:, :, :] = self.original_background[:, :, :]
        # Update the Tkinter window
        self.update_tkinter_image(background)
    

    # ------------------------------------------------------------------------------------DEPRECATED----------------------------------------------------------------------------------
    # def rotate_map(self, angle):
    #     h, w = self.background.shape[:2]
    #     center = (w // 2, h // 2)
    #     # Calculate the size of the new image
    #     abs_cos, abs_sin = abs(np.cos(np.radians(angle))), abs(np.sin(np.radians(angle)))
    #     bound_w = int(h * abs_sin + w * abs_cos)
    #     bound_h = int(h * abs_cos + w * abs_sin)
    #     # Adjust the rotation matrix to the center and apply the padding
    #     rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    #     rotation_matrix[0, 2] += bound_w / 2 - center[0]
    #     rotation_matrix[1, 2] += bound_h / 2 - center[1]
    #     rotated_img = cv2.warpAffine(self.background, rotation_matrix, (bound_w, bound_h))
    #     self.background = rotated_img
    #     print(f"Map rotated {angle}°")
    #     return self.background
    

    # def resize_map(self, width=None, height=None):
    #     #ToDo: Width und Height der Map müssen noch richtig erkannt und skaliert werden für die Anzeige        
    #     self.background = cv2.resize(self.background, (950,760))
    #     return self.background

    # def put_foreground(self):
    #     if self.foreground:
    #         for image in self.foreground:
    #             factor = image["factor"]
    #             self.num_cells_x, self.num_cells_y = 50, 40 #ToDo: automatische Erkennung der Zellen-Anzahl! 

    #             # Berechne die Größe jeder Zelle
    #             cell_width = self.background.shape[1] // self.num_cells_x
    #             cell_height = self.background.shape[0] // self.num_cells_y

    #             overlay = cv2.imread(image["path"],cv2.IMREAD_UNCHANGED)
    #             overlay_resized = cv2.resize(overlay, (cell_width*factor, cell_height*factor), interpolation=cv2.INTER_LINEAR)

    #             # Prüfe, ob das PNG-Bild einen Alpha-Kanal hat
    #             if overlay_resized.shape[2] == 4:
    #                 # Extrahiere die Alpha-Maske des PNG-Bildes und die RGB-Farben
    #                 alpha_mask = overlay_resized[:, :, 3] / 255.0
    #                 overlay_colors = overlay_resized[:, :, :3]

    #                 # Bestimme die Region, wo das Overlay platziert werden soll
    #                 # Hier platzieren wir das Overlay in der ersten Zelle
    #                 x_offset, y_offset = image["position"]
    #                 y1, y2 = (y_offset-factor//2)*cell_height, (y_offset-factor//2)*cell_height + overlay_resized.shape[0]
    #                 x1, x2 = (x_offset-factor//2)*cell_width, (x_offset-factor//2)*cell_width + overlay_resized.shape[1]

    #                 # Mische die beiden Bilder
    #                 for c in range(0, 3):
    #                     try:
    #                         self.background[y1:y2, x1:x2, c] = (1. - alpha_mask) * self.background[y1:y2, x1:x2, c] + alpha_mask * overlay_colors[:, :, c]
    #                     except:
    #                         print("")
    #                     else:
    #                         print("")
                        
    
    # def add_overlay(self,path,position,factor=1):
    #     self.foreground.append({"path": path, "position": position, "factor": factor})

    # def remove_overlay(self,path,position,factor=1):
    #     self.foreground.remove({"path": path, "position": position, "factor": factor})
    #     self.background = original_background


    # def display_map(self, window_name='Image',factor=1):        
    #     try:
    #         cv2.destroyWindow(window_name)
    #     except:
    #         #cv2.waitKey()
    #         self.put_foreground()    
    #         cv2.imshow(window_name, self.background)            
    #     else:        
    #         self.put_foreground()    
    #         cv2.imshow(window_name, self.background) 
            

    # def figure_radius(self,position,size=1):    
    #     global original_background
    #     x,y = position
    #     original_background = self.background.copy()   
    #     i = 0 
        
    #     self.add_overlay("Assets\\player_radius.png",(x,y),factor=size*5)
     
        
    #     self.display_map("Map",factor=5*size)
    #     cv2.waitKey(0)
    # ------------------------------------------------------------------------------------DEPRECATED----------------------------------------------------------------------------------