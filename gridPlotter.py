import cv2

class GridPlotter:   
   def plot_to_img(no_x_fields, no_y_fields, img):
      height, width = img.shape
      pixel_per_field_X = width/no_x_fields
      pixel_per_field_Y = height/no_y_fields
      
      gridColor = (255,0,255)
      thickness = 1
      
      for i in range(0, no_x_fields):
         startX = round(i*pixel_per_field_X)
         endX = round(i*pixel_per_field_X)
         startY = 0
         endY = height
         cv2.line(img, (startX, startY), (endX, endY), gridColor, thickness)
         
      for i in range(0, no_y_fields):
         startX = 0
         endX = width
         startY = round(i*pixel_per_field_Y)
         endY = round(i*pixel_per_field_Y)
         cv2.line(img, (startX, startY), (endX, endY), gridColor, thickness)
      
      return img