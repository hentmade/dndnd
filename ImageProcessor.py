import cv2
import numpy as np
import pyautogui

class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)   

    
    def rotate_image(self, angle):
        h, w = self.image.shape[:2]
        center = (w // 2, h // 2)
        # Calculate the size of the new image
        abs_cos, abs_sin = abs(np.cos(np.radians(angle))), abs(np.sin(np.radians(angle)))
        bound_w = int(h * abs_sin + w * abs_cos)
        bound_h = int(h * abs_cos + w * abs_sin)
        # Adjust the rotation matrix to the center and apply the padding
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotation_matrix[0, 2] += bound_w / 2 - center[0]
        rotation_matrix[1, 2] += bound_h / 2 - center[1]
        rotated_img = cv2.warpAffine(self.image, rotation_matrix, (bound_w, bound_h))
        self.image = rotated_img

    def resize_image(self, width=None, height=None):
        # Scale image to needed resolution
        if width is None or height is None:
            width, height = pyautogui.size()
        
        self.image = cv2.resize(self.image, (width, height))

    def display_image(self, window_name='Image'):
        # Show image in window
        cv2.imshow(window_name, self.image)

    