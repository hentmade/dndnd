import cv2

class MomentsDetection:
   def __init__(self, img):
      self.img = img
      
   def detectX(self):
      M = cv2.moments(self.img)
      if(M["m00"] != 0):
         centerX = int(M["m10"] / M["m00"])
      else:
         centerX = 0
      return centerX
   
   def detectY(self):
      M = cv2.moments(self.img)
      if(M["m00"] != 0):
         centerY = int(M["m01"] / M["m00"])
      else:
         centerY = 0
      return centerY
   
   def getM00(self):
      M = cv2.moments(self.img)
      return M["m00"]