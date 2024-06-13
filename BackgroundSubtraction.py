import cv2

class BackgroundSubtraction:
   def subtract(self, img_foreground, img_background):
      #grayscale images
      img_background_gray = cv2.cvtColor(img_background, cv2.COLOR_BGR2GRAY)
      img_foreground_gray = cv2.cvtColor(img_foreground, cv2.COLOR_BGR2GRAY)

      #invert
      cv2.bitwise_not(img_background_gray, img_background_gray)
      cv2.bitwise_not(img_foreground_gray, img_foreground_gray)

      #subtract
      output = cv2.subtract(img_foreground_gray, img_background_gray)

      #blur
      kernelSize = 7
      output = cv2.medianBlur(output, kernelSize)

      #binary
      thresholdValue = 35
      maxValue = 255
      thresholdType = 0;      # 0: Binary, 1: Binary Inverted, 2: Truncate, 3: To Zero, 4: To Zero Inverted
      cv2.threshold(output, thresholdValue, maxValue, thresholdType, output)
      
      return output