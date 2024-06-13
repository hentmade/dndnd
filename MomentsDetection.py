import cv2

class MomentsDetection:
   def __init__(self, img):
      self.img = img
      
   def detectX(self):
      M = cv2.moments(self.img)
      return int(M["m10"] / M["m00"])
   
   def detectY(self):
      M = cv2.moments(self.img)
      return int(M["m01"] / M["m00"])
   
   def getM00(self):
      M = cv2.moments(self.img)
      return M["m00"]