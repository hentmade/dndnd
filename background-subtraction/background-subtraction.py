import numpy as np
import cv2

file_path_background = './background.jpg'
file_path_foreground = './img1.jpg'

img_background = cv2.imread(file_path_background)
img_foreground = cv2.imread(file_path_foreground)

fgbg2 = cv2.createBackgroundSubtractorMOG2()

fgbg2.apply(img_background)
img = fgbg2.apply(img_foreground)
cv2.imwrite("./output.jpg",img)

""" scale_down = 0.2
#scaled_f_down = cv2.resize(image, None, fx= scale_down, fy= scale_down, interpolation= cv2.INTER_LINEAR)

resized_down = cv2.resize(img, None, fx= scale_down, fy= scale_down, interpolation= cv2.INTER_LINEAR)
#resized_background= cv2.resize(img_background, down_points, interpolation= cv2.INTER_LINEAR)
#resized_foreground = cv2.resize(img_foreground, down_points, interpolation= cv2.INTER_LINEAR)
resized_background = cv2.resize(img_background, None, fx= scale_down, fy= scale_down, interpolation= cv2.INTER_LINEAR)
resized_foreground = cv2.resize(img_foreground, None, fx= scale_down, fy= scale_down, interpolation= cv2.INTER_LINEAR)
#resized_masked_img = cv2.resize(masked_img, None, fx= scale_down, fy= scale_down, interpolation= cv2.INTER_LINEAR)

cv2.imshow("resized_down",resized_down)
cv2.imshow("resized_background",resized_background)
cv2.imshow("resized_foreground",resized_foreground) """
""" cv2.imshow("resized_masked_img",masked_img) """

""" cv2.waitKey(0)
cv2.destroyAllWindows() """