import cv2 

class GitterErkennung:
    def __init__(self, list, image):
            self.list = list
            self.image = image       
            image = binarize(image)
            cv2.imshow("binarized", image)
            cv2.waitKey(0)
            #img = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
            rectDetection(image)
    

def binarize(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    'ret,binarized = cv2.threshold(image,200,255,cv2.THRESH_BINARY)'
    'binarized = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=5)'
    #binarized = cv2.Canny(image,100,200)
    binarized = cv2.Laplacian(image,cv2.CV_64F)
    ret, binarized = cv2.threshold(binarized, 40, 255, cv2.THRESH_TOZERO)

    #cv2.cvtColor(binarized,cv2.Color_Gray2)

    #cv2.imshow("binarized", binarized)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return binarized

def rectDetection(image):
    #CV_32SC1
    #cv2.cvtColor
    #cv2.StartFindContours_Impl
    print("Image Data Type:", image.dtype)
    float64_image_uint8 = cv2.convertScaleAbs(image)

    contours, _ = cv2.findContours(float64_image_uint8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("Number of contours detected:", len(contours))
    img = image
    
    #img = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)   
    
    print("Image Data Type:", img.dtype)
    #  cv2.cvtColor(binary_img, cv.CV_GRAY2RGB)
    
    for cnt in contours:
        x1,y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)  
            ratio = float(w)/h
            if ratio >= 0.9 and ratio <= 1.1:
                img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
                cv2.putText(img, 'Square', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            else:
                cv2.putText(img, 'Rectangle', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                img = cv2.drawContours(img, [cnt], -1, (0,255,0), 3)

    cv2.imshow("Shapes", img)
    cv2.waitKey(0)

