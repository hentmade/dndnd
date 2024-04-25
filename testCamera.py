import cv2
from ImageProcessor import ImageProcessor
from ClickEventHandler import ClickEventHandler


# Bildpfad angeben
image_path = "Assets\\map_from_camera.jpg"

# Instanz von ImageProcessor erstellen
processor = ImageProcessor(image_path)

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
cv2.waitKey(0)
cv2.destroyAllWindows()