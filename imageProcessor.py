import cv2
import numpy as np
import matplotlib.pyplot as plt
from ClickEventHandler import ClickEventHandler

class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.clicked_points = []

    def rotate_image(self):
        # Rotate image by 90° clockwise --> ToDo: Other angels       
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)    


    def resize_image(self, width, height):
        # Scale image to needed resolution
        self.image = cv2.resize(self.image, (width, height))

    def display_image(self, window_name='Image'):
        # Show image in window
        cv2.imshow(window_name, self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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
        cv2.destroyAllWindows()
        
        #Get Corners from Original picture by clicking from: LinksOben - LinksUnten - RechtsUnten - RechtsOben 
        original_pts = np.float32(self.clicked_points) 
        #Project clicked points 
        projected_pts = np.float32([[0, 0], [self.image.shape[1], 0], [self.image.shape[1], self.image.shape[0]], [0, self.image.shape[0]]])

        # Calculate transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(original_pts, projected_pts)
        # Transform picture with transformation matrix
        #before_image = self.image
        self.image = cv2.warpPerspective(self.image, transformation_matrix, (self.image.shape[1], self.image.shape[0]))
        
        # Plotting - for testing --> needs before image
        #plt.subplot(121), plt.imshow(before_image), plt.title('Input')
        #plt.subplot(122), plt.imshow(dst), plt.title('Output')
        #plt.show()