import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyautogui

class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.clicked_points = []

    
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


    def click_event(self, event, x, y, flags, param):
        img_copy = self.image.copy()  # Create a copy of the original image

        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.clicked_points) < 4:
                self.clicked_points.append((x, y))
                cv2.circle(img_copy, (x, y), 5, (0, 255, 0), -1)
            else:
                print("Already four points set!")
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.clicked_points:
                self.clicked_points.pop()
                # Redraw all points
                for point in self.clicked_points:
                    cv2.circle(img_copy, point, 5, (0, 255, 0), -1)

        self.image = img_copy  # Update the original image with the modified copy
        cv2.imshow('Transformed Image', self.image)

    def transform_image(self): 
        # Show image and get the clicked points for transformation
        cv2.imshow('Transformed Image', self.image)
        cv2.setMouseCallback('Transformed Image', self.click_event, param=self.image)
        cv2.waitKey(0)
        cv2.destroyWindow('Transformed Image')
        
        #Get Corners from Original picture by clicking from: LinksOben - RechtsOben - RechtsUnten - LinksUnten 
        original_pts = np.float32(self.clicked_points) 
        #Project clicked points 
        projected_pts = np.float32([[0, 0], [self.image.shape[1], 0], [self.image.shape[1], self.image.shape[0]], [0, self.image.shape[0]]])

        # Calculate transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(original_pts, projected_pts)
        # Transform picture with transformation matrix
        self.image = cv2.warpPerspective(self.image, transformation_matrix, (self.image.shape[1], self.image.shape[0]))
        transformed_image = self.image
        return transformed_image