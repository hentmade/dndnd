import cv2
import numpy as np

#DEPRECATED
class ClickEventHandler:

    def __init__(self,img,refPt):
        self.refPt = refPt  
        self.img = img
        refPt = []    #This variable we use to store the pixel location

   
    #click event function
    def click_event(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x,",",y)
            self.refPt.append([x,y])
            font = cv2.FONT_HERSHEY_SIMPLEX
            strXY = str(x)+", "+str(y)
            cv2.putText(self.img, strXY, (x,y), font, 0.5, (255,255,0), 2)
            cv2.imshow("image", self.img)

        if event == cv2.EVENT_RBUTTONDOWN:
            blue = self.img[y, x, 0]
            green = self.img[y, x, 1]
            red = self.img[y, x, 2]
            font = cv2.FONT_HERSHEY_SIMPLEX
            strBGR = str(blue)+", "+str(green)+","+str(red)
            cv2.putText(self.img, strBGR, (x,y), font, 0.5, (0,255,255), 2)
            cv2.imshow("image", self.img)


    #Here, you need to change the image name and it's path according to your directory
    


    