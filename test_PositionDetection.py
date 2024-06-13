from PositionDetection import *
from ImageTransformer import ImageTransformer
import cv2

""" transf_img_background = cv2.imread("..\\Assets\\background_2305.jpg")
transf_img_foreground = cv2.imread("..\\Assets\\figur1_2305.jpg") """

camera_imgTransformer = ImageTransformer()
transf_img_background = camera_imgTransformer.transform_image("..\\Assets\\background_2305.jpg")
transf_img_foreground = camera_imgTransformer.transform_image("..\\Assets\\figur1_2305.jpg")

posDetector = PositionDetection(50, 40)

position = posDetector.detectPosition(transf_img_foreground, transf_img_background)

cv2.waitKey(0)
cv2.destroyAllWindows()

print(position)