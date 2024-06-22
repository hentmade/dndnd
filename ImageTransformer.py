import cv2
import numpy as np

class ImageTransformer:    
    def __init__(self,clicked_points):
        self.clicked_points = clicked_points    

    def transform_image(self,image): 
        #Get Corners from Original picture by clicking from: LinksOben - RechtsOben - RechtsUnten - LinksUnten 
        original_pts = np.float32(self.clicked_points) 
        #Project clicked points 
        projected_pts = np.float32([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])

        # Calculate transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(original_pts, projected_pts)
        # Transform picture with transformation matrix
        image = cv2.warpPerspective(image, transformation_matrix, (image.shape[1], image.shape[0]))
    
        return image