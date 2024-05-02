import cv2
from backgroundSubtraction import BackgroundSubtraction
from momentsDetection import MomentsDetection

file_path_background = './background.jpg'
file_path_foreground = './img1.jpg'

img_background = cv2.imread(file_path_background)
img_foreground = cv2.imread(file_path_foreground)

output = BackgroundSubtraction.subtract(img_foreground, img_background)
cX = MomentsDetection.detectX(output)
cY = MomentsDetection.detectY(output)


cv2.imshow("background", img_background)
cv2.imshow("foreground", img_foreground)
cv2.imshow("output", output)

cv2.waitKey(0)
cv2.destroyAllWindows()