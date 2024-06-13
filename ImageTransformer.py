import cv2
import numpy as np

class ImageTransformer:    
    def __init__(self):
        self.clicked_points = []     

    def click_event(self, event, x, y, flags, param):
        img_copy = param.copy()  # Create a copy of the original image

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

        #self.image = img_copy  # Update the original image with the modified copy
        cv2.imshow('Transformed Image', img_copy)

    def transform_image(self,image): 
        # Show image and get the clicked points for transformation
        
        if not self.clicked_points:
            cv2.imshow('Transformed Image', image)
            cv2.setMouseCallback('Transformed Image', self.click_event, param=image)
            cv2.waitKey(0)
            cv2.destroyWindow('Transformed Image')
        
        #Get Corners from Original picture by clicking from: LinksOben - RechtsOben - RechtsUnten - LinksUnten 
        original_pts = np.float32(self.clicked_points) 
        #Project clicked points 
        projected_pts = np.float32([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])

        # Calculate transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(original_pts, projected_pts)
        # Transform picture with transformation matrix
        image = cv2.warpPerspective(image, transformation_matrix, (image.shape[1], image.shape[0]))
    
        return image