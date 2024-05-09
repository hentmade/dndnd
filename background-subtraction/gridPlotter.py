import cv2

class GridPlotter:   
   def plot_to_img(no_x_fields, no_y_fields, img):
      height, width = img.shape
      pixel_per_field_X = int(width/no_x_fields)
      pixel_per_field_Y = int(height/no_y_fields)
      
      gridColor = (255,0,255)
      thickness = 1
      
      for i in range(0, width, pixel_per_field_X):
         startX = i
         endX = i
         startY = 0
         endY = height
         cv2.line(img, (startX, startY), (endX, endY), gridColor, thickness)
         
      for i in range(0, height, pixel_per_field_Y):
         startX = 0
         endX = width
         startY = i
         endY = i
         cv2.line(img, (startX, startY), (endX, endY), gridColor, thickness)
      
      return img