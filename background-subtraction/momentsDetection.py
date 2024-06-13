import cv2

class MomentsDetection:
   def detectX(img):
      M = cv2.moments(img)
      return int(M["m10"] / M["m00"])
   
   def detectY(img):
      M = cv2.moments(img)
      return int(M["m01"] / M["m00"])