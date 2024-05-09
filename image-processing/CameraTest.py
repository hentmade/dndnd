import cv2
from imageProcessor import *
import pyautogui


# Bildpfad angeben
beamer_image_path = "Assets\\encounter.webp"
camera_image_path = "Assets\\map_with_figure.jpg"

# Instanz von ImageProcessor erstellen
beamer_imgProcessor = ImageProcessor(beamer_image_path)
camera_imgProcessor = ImageProcessor(camera_image_path)

# Bild um X Grad drehen
beamer_imgProcessor.rotate_image(90)
# Bild auf Beamergröße skalieren
beamer_imgProcessor.resize_image()
# Bild anzeigen in Window Main
beamer_imgProcessor.display_image("Main")

# Kamera-Bild transformieren und für Weiterverarbeitung vorbereiten
transformed_image = camera_imgProcessor.transform_image()

# Transformiertes Kamera-Bild in Window Channel anzeigen
cv2.imshow('Channel',transformed_image)

cv2.waitKey(0)
cv2.destroyAllWindows()