import cv2
from ImageProcessor import *
import pyautogui

from ImageTransformer import ImageTransformer


# Bildpfad angeben
beamer_image_path = "Assets\\encounter.webp"
background_image_path = "Assets\\background.jpg"
camera_image_path = "Assets\\background_with_figure.jpg"

# Instanz von ImageProcessor erstellen
beamer_imgProcessor = ImageProcessor(beamer_image_path)

# Bild um X Grad drehen
beamer_imgProcessor.rotate_image(90)
# Bild auf Beamergröße skalieren
beamer_imgProcessor.resize_image()
# Bild anzeigen in Window Main
beamer_imgProcessor.display_image("Main")


# Kamera-Bild transformieren und für Weiterverarbeitung vorbereiten
camera_imgTransformer = ImageTransformer()
transformed_image1 = camera_imgTransformer.transform_image(background_image_path)
transformed_image2 = camera_imgTransformer.transform_image(camera_image_path)



# Transformiertes Kamera-Bild in Window Channel anzeigen
cv2.imshow('Channel1',transformed_image1)
cv2.imshow('Channel2',transformed_image2)

cv2.waitKey(0)
cv2.destroyAllWindows()