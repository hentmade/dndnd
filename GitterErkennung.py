import cv2 

class GitterErkennung:
    def __init__(self, list, image):
            self.list = list
            self.image = image
            binarize(image)
    

def binarize(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,binarized = cv2.threshold(image,200,255,cv2.THRESH_BINARY)
    cv2.imshow("binarized", binarized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()