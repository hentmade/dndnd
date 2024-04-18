import cv2
from ImageProcessor import ImageProcessor
from clickEventHandler import clickEventHandler


# Bildpfad angeben
image_path = "Assets\\map.jpg"

# Instanz von ImageProcessor erstellen
processor = ImageProcessor(image_path)

#Instanz von Click EventHandler
click_event = clickEventHandler(image_path,refPt) 
refPt = []

# Bild um 90 Grad drehen
processor.rotate_image()

# Bild auf Beamergröße skalieren
processor.resize_image(width=1920, height=1080)

# Bild transformieren
processor.transform_image()

# Bild anzeigen
processor.display_image()

# Clicks entgegennehmen
#calling the mouse click event
cv2.setMouseCallback("image", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()



