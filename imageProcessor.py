import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)

    def rotate_image(self):
        # Bild um den angegebenen Winkel drehen        
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)    


    def resize_image(self, width, height):
        # Bild auf die angegebenen Dimensionen skalieren
        self.image = cv2.resize(self.image, (width, height))

    def display_image(self, window_name='Image'):
        # Bild in einem Fenster anzeigen
        cv2.imshow(window_name, self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def transform_image(self): 
        image = self.image
        rows,cols,ch = self.image.shape
        print(image.shape[0])
        print(image.shape[1])
        original_pts = np.float32([[0, 100], [520, 0], [520, 420], [0,520]]) #ToDo: Klickbar machen!
        projected_pts = np.float32([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]]) #shape[0] = 1080 shape[1] = 1920
        #pts2 = np.float32([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])
        # Berechnen der Transformationsmatrix
        M = cv2.getPerspectiveTransform(original_pts,projected_pts)
        # Bild perspektivisch transformieren
        dst = cv2.warpPerspective(self.image,M,(image.shape[1], image.shape[0]))
        self.image = dst
        plt.subplot(121),plt.imshow(self.image),plt.title('Input')
        plt.subplot(122),plt.imshow(dst),plt.title('Output')
        plt.show()
    

