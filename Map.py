import cv2
import numpy as np
import pyautogui

class Map:
    def __init__(self, image_path):
        self.background = cv2.imread(image_path)
        self.foreground = []

    
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
        # Scale image to needed resolution
        #if width is None or height is None:
            #width, height = pyautogui.size()
            #width, height = 1920,1080
        
        self.background = cv2.resize(self.background, (1350,1080))
        return self.background
    

    def put_foreground(self):
        if self.foreground:
            for image in self.foreground:
                img = cv2.imread(image["path"])
                image_height, image_width, _ = img.shape
                x_offset, y_offset = image["position"]
                self.background[y_offset:y_offset+image_height, x_offset:x_offset+image_width] = img
        return self.background
        

    def add_overlay(self,path,position):
        self.foreground.append({"path": path, "position": position})


    def display_map(self, window_name='Image'):
        # Show image in window
        if self.foreground:
            cv2.destroyWindow(window_name)
        cv2.waitKey()
        self.put_foreground()    
        cv2.imshow(window_name, self.background)


    