import cv2
import numpy as np

class ImageTransformer:    
    def __init__(self, clicked_points):
        self.clicked_points = clicked_points    

    def transform_image(self, image): 
        # Get Corners from Original picture by clicking from: LinksOben - RechtsOben - RechtsUnten - LinksUnten 
        original_pts = np.float32(self.clicked_points) 
        # Project clicked points 
        projected_pts = np.float32([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])

        # Calculate transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(original_pts, projected_pts)
        # Transform picture with transformation matrix
        transformed_image = cv2.warpPerspective(image, transformation_matrix, (image.shape[1], image.shape[0]))
    
        return transformed_image

    def get_bounding_box(self):
        # Berechne das minimal umschließende Rechteck
        left = min(self.clicked_points, key=lambda x: x[0])[0]
        top = min(self.clicked_points, key=lambda x: x[1])[1]
        right = max(self.clicked_points, key=lambda x: x[0])[0]
        bottom = max(self.clicked_points, key=lambda x: x[1])[1]

        return {
            "left": left,
            "top": top,
            "width": right - left,
            "height": bottom - top
        }
