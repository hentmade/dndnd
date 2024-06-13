import cv2 
from numpy import pi
import numpy as np
import math
import collections

class GitterErkennung:
    def __init__(self, list, image):
            self.list = list
            self.image = image    

            lines = test(image)   
            squareSize = sortLinesXY(lines)
            # Black color in BGR 
            color = (0, 0, 0) 
   
            # Line thickness of -1 px 
            # Thickness of -1 will fill the entire shape 
            thickness = -1

            # Start coordinate, here (100, 50) 
            # represents the top left corner of rectangle 
            start_point = (0, 0) 
            
            # Ending coordinate, here (125, 80) 
            # represents the bottom right corner of rectangle 
            end_point = (squareSize, squareSize) 

            image = cv2.rectangle(image, start_point, end_point, color, thickness) 
            
            height, width = image.shape[:2] 

            height = height - (height/squareSize)*1
            width = width - (width/squareSize)*1
            dimensions = [math.floor(height/squareSize),math.floor(width/squareSize)]
            print("Height, Width", height, width)
            print("Dimensions X,Y",dimensions[0],dimensions[1])
            cv2.imshow("Square", image)
            cv2.waitKey(0)
            """  binImage = binarize(image)
            cv2.imshow("binary", binImage)
            cv2.waitKey(0)

            contours = rectDetection(binImage)

            img = image
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
            
            img = cv2.resize(img,(0, 0), fx = 0.4, fy = 0.4)
            cv2.imshow("Shapes", img)
            cv2.waitKey(0) """
"""             cv2.imshow("binarized", image)
            cv2.waitKey(0) 
"""
            #img = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
           


def calculate_distance_occurrences(arr):
    # Calculate distances between consecutive elements
    distances = [abs(arr[i] - arr[i + 1]) for i in range(len(arr) - 1)]
    
    # Count occurrences of each distance
    distance_counts = collections.Counter(distances)
    
    # Convert the Counter object to a list of tuples
    result = list(distance_counts.items())
    
    return result

# Example usage
input_array = [1, 4, 2, 7, 4]
print(calculate_distance_occurrences(input_array))

def sort_tuples_by_first_element(tuples_list):
    # Sort the list of tuples by the first element
    sorted_list = sorted(tuples_list, key=lambda x: x[0])
    return sorted_list

def print_first_value_of_last_tuple(tuples_list):
    if not tuples_list:
        print("The list is empty.")
        return
    
    last_tuple = tuples_list[-1]
    first_value = last_tuple[0]
    print(first_value)
    return first_value

def sortLinesXY(lines):
    xLines = []
    yLines = []
    for i in range(0, len(lines)):
            l = lines[i][0]
            if l[0] == l[2]:
                xLines.append(l[0])
            elif l[1] == l[3]:
                yLines.append(l[1])
            #cv2.line(image, start_point, end_point, color, thickness) 
            #cv2.line(lines, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    xLines.sort()
    yLines.sort()
    print(len(xLines))
    print(len(yLines))
    print("X Lines")
    print (str(xLines)[1:-1] )
    print("Y Lines")
    print (str(yLines)[1:-1] )

    xLinesSorted = calculate_distance_occurrences(xLines)
    yLinesSorted = calculate_distance_occurrences(yLines)
    print("\n")
    print(xLinesSorted)
    print("\n")
    print(yLinesSorted)
    
    xLinesSorted  = sort_tuples_by_first_element(xLinesSorted)
    yLinesSorted = sort_tuples_by_first_element(yLinesSorted)
    print("\n")
    print(xLinesSorted)
    print("\n")
    print(yLinesSorted)

    print_first_value_of_last_tuple(xLinesSorted)
    
    return print_first_value_of_last_tuple(yLinesSorted)


def test(src):
     ## [edge_detection]
    # Edge detection
    dst = cv2.Canny(src, 50, 200, None, 3)
    ## [edge_detection]

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    """ 
    ## [hough_lines]
    #  Standard Hough Line Transform
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    ## [hough_lines]
    ## [draw_lines]
    # Draw the lines
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
    ## [draw_lines]
 """
    ## [hough_lines_p]
    # Probabilistic Line Transform
    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    ## [hough_lines_p]
    ## [draw_lines_p]
    # Draw the lines
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            #cv2.line(image, start_point, end_point, color, thickness) 
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    ## [draw_lines_p]
    ## [imshow]
    # Show results
    print(np.matrix(linesP))
    cv2.imshow("Source", src)
    #cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    ## [imshow]
    ## [exit]
    # Wait and Exit
    cv2.waitKey()
    return linesP
    ## [exit]

def binarize(image):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    'ret,binarized = cv2.threshold(image,200,255,cv2.THRESH_BINARY)'
    'binarized = cv2.Sobel(image,cv2.cv_64F,1,0,ksize=5)'
    #binarized = cv2.Canny(image,100,200)
    binarized = cv2.Laplacian(image,cv2.cv_64F)
    ret, binarized = cv2.threshold(binarized, 40, 255, cv2.THRESH_TOZERO)

    #cv2.cvtColor(binarized,cv2.Color_Gray2)

    #cv2.imshow("binarized", binarized)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return binarized

def rectDetection(image):
    #cv_32SC1
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
    #  cv2.cvtColor(binary_img, cv.cv_GRAY2RGB)
    #formfaktor 0,785 for rectangle => C= 4*pi*(A/U²)
    finalContours = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(approx)
        perimiter = cv2.arcLength(approx, True)
        if ((perimiter != 0)and(area !=0)) :
            C = 4 * pi * (area / (perimiter * perimiter))
            #print("C: ",C)
            if round(C,3) == 0.785:
                finalContours.append(approx)
                print("Area:" , area)
                print("C: ",C)
    print("END cont length: ",len(finalContours))
    return finalContours
"""   for cnt in contours:
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
    cv2.waitKey(0) """

