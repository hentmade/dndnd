from BackgroundSubtraction import BackgroundSubtraction
from MomentsDetection import MomentsDetection
import math

# only for testing:
from gridPlotter import GridPlotter
import cv2
# END only for testing


class PositionDetection:
   def __init__(self, game_field_width, game_field_height):
      self.game_field_width = game_field_width
      self.game_field_height = game_field_height
      
   def detectPosition(self, img_foreground, img_background):
      backgroundSubtractor = BackgroundSubtraction()
      difference_img = backgroundSubtractor.subtract(img_foreground, img_background)
      
      momentsDetector = MomentsDetection(difference_img)
      #TODO avoid finding other contours
      centerX = momentsDetector.detectX()
      centerY = momentsDetector.detectY()
      
      # only for testing:
      #difference_img = GridPlotter.plot_to_img(50, 40, difference_img)
      #cv2.line(difference_img, (centerX-5, centerY), (centerX+5, centerY), (255,0,255), 1)
      """  cv2.line(difference_img, (centerX, centerY-5), (centerX, centerY+5), (255,0,255), 1)
      cv2.imshow("output", difference_img)
      cv2.waitKey(0)
      cv2.imwrite("Assets\\test_PositionDetection.jpg", difference_img) """
      #print(difference_img.shape)
      #print(centerX, centerY)
      #print(momentsDetector.getM00()/255)
      # END only for testing
      
      diff_img_height, diff_img_width = difference_img.shape
      relativeX = centerX / diff_img_width
      relativeY = centerY / diff_img_height
      
      positionX = math.ceil(relativeX * self.game_field_width)
      positionY = math.ceil(relativeY * self.game_field_height)
      
      return (positionX, positionY)