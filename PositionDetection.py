from BackgroundSubtraction import BackgroundSubtraction
from MomentsDetection import MomentsDetection
import math
import cv2
import numpy as np


class PositionDetection:
   def __init__(self, game_field_width, game_field_height):
      self.game_field_width = game_field_width
      self.game_field_height = game_field_height
      self.amount_threshold_2x2 = 0.0014   #value for distinguishing between 1x1 and 2x2 objects
      
   def detectPosition(self, img_foreground, img_background):
      backgroundSubtractor = BackgroundSubtraction()
      difference_img = backgroundSubtractor.subtract(img_foreground, img_background)

      cv2.imshow("Difference Image",difference_img)
      cv2.waitKey(0)
      
      diff_img_height, diff_img_width = difference_img.shape
      cell_width = diff_img_width/self.game_field_width
      cell_height = diff_img_height/self.game_field_height
      
      contours, index_biggest_contour, maximum_area = self.find_biggest_contour(difference_img)
      
      #TODO: remove, only for debugging:
      print("white pixel amount to determine threshold_2x2: ", (maximum_area/difference_img.size))

      #detect centroid:
      momentsDetector = MomentsDetection(contours[index_biggest_contour])
      #TODO error vom letzten Mal untersuchen, als Figur nicht bewegt wurde
      centerX = momentsDetector.detectX()
      centerY = momentsDetector.detectY()
      posX = math.floor((centerX / diff_img_width) * self.game_field_width)
      posY = math.floor((centerY / diff_img_height) * self.game_field_height)
      
      pixelpoints = self.create_list_of_white_pixels_position(difference_img.shape, contours, index_biggest_contour)
      
      if (maximum_area/difference_img.size) < self.amount_threshold_2x2:
         #object is 1x1
         cells_to_be_examined = [(posX-1,posY-1), (posX+0,posY-1), (posX+1,posY-1),
                                 (posX-1,posY+0), (posX+0,posY+0), (posX+1,posY+0),
                                 (posX-1,posY+1), (posX+0,posY+1), (posX+1,posY+1)]
         position = self.get_cell_with_most_white_pixels(cells_to_be_examined, cell_width, cell_height, pixelpoints)
      
      else:
         #object is 2x2
         cells_to_be_examined = [(posX-2,posY-2), (posX-1,posY-2), (posX+0,posY-2), (posX+1,posY-2), (posX+2,posY-2),
                                 (posX-2,posY-1), (posX-1,posY-1), (posX+0,posY-1), (posX+1,posY-1), (posX+2,posY-1),
                                 (posX-2,posY+0), (posX-1,posY+0), (posX+0,posY+0), (posX+1,posY+0), (posX+2,posY+0),
                                 (posX-2,posY+1), (posX-1,posY+1), (posX+0,posY+1), (posX+1,posY+1), (posX+2,posY+1),
                                 (posX-2,posY+2), (posX-1,posY+2), (posX+0,posY+2), (posX+1,posY+2), (posX+2,posY+2)]
         cells_with_most_white_pixels = []
         for _ in range(4):
            retval = self.get_cell_with_most_white_pixels(cells_to_be_examined, cell_width, cell_height, pixelpoints)
            cells_with_most_white_pixels.append(retval)
            cells_to_be_examined.remove(retval)
         
         sorted_tuple = tuple(sorted(cells_with_most_white_pixels, key=lambda x: (x[1], x[0])))
         if (sorted_tuple[0][0] + 1 == sorted_tuple[1][0]) and (sorted_tuple[0][0] == sorted_tuple[2][0]) and (sorted_tuple[0][1] + 1 == sorted_tuple[2][1]) and (sorted_tuple[2][1] == sorted_tuple[3][1]):
            position = (sorted_tuple[0], sorted_tuple[-1])
         else:
            print("Fehler: Figur bitte erneut platzieren")
            position = (0,0)
            #TODO check error behaviour

      return position
   
   
   
   def find_biggest_contour(self, binary_img):
      contours, _ = cv2.findContours(binary_img, 1, 2)
      maximum_area = 0
      index_biggest_contour = 0
      for i, cnt in enumerate(contours):
         if(cv2.contourArea(cnt) > maximum_area):
            maximum_area = cv2.contourArea(cnt)
            index_biggest_contour = i
      
      return contours, index_biggest_contour, maximum_area
         
   def create_list_of_white_pixels_position(self, shape, contours, idx):
      mask = np.zeros(shape, np.uint8)
      cv2.drawContours(mask, contours, idx, 1, -1)
      return cv2.findNonZero(mask)
   
   def get_cell_with_most_white_pixels(self, cells, cell_width, cell_height, pixels):
      cell_with_most_white_pixels = (0,0)
      max_number_of_white_pixels = 0
      for cell in cells:
         if cell[0] >= 0 and cell[1] >= 0 and cell[0] < self.game_field_width and cell[1] < self.game_field_height:
            xStart = (cell[0]*cell_width) + 1
            xEnd =   xStart + cell_width - 1
            yStart = (cell[1]*cell_height) + 1
            yEnd =   yStart + cell_height -1
            amount_white_pixels = 0
            for pixel in pixels:
               if pixel[0][0] >= xStart and pixel[0][0] <= xEnd and pixel[0][1] >= yStart and pixel[0][1] <= yEnd:
                  amount_white_pixels = amount_white_pixels + 1
            if amount_white_pixels > max_number_of_white_pixels:
               max_number_of_white_pixels = amount_white_pixels
               cell_with_most_white_pixels = cell
            
      return cell_with_most_white_pixels