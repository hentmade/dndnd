import cv2
import numpy as np

# Lade das ursprüngliche Bild
background = cv2.imread('Assets\\encounter.webp')

# Lade das PNG-Bild (mit Alpha-Kanal)
overlay = cv2.imread('Assets\\overlay_trap.png', cv2.IMREAD_UNCHANGED)

# Prüfe, ob das PNG-Bild einen Alpha-Kanal hat
if overlay.shape[2] == 4:
    # Extrahiere die Alpha-Maske des PNG-Bildes und die RGB-Farben
    alpha_mask = overlay[:, :, 3] / 255.0
    overlay_colors = overlay[:, :, :3]

    # Bestimme die Region, wo das Overlay platziert werden soll
    y_offset = 0
    x_offset = 0
    y1, y2 = y_offset, y_offset + overlay.shape[0]
    x1, x2 = x_offset, x_offset + overlay.shape[1]

    # Mische die beiden Bilder
    for c in range(0, 3):
        background[y1:y2, x1:x2, c] = (1. - alpha_mask) * background[y1:y2, x1:x2, c] + alpha_mask * overlay_colors[:, :, c]

# Zeige das Ergebnis an
cv2.imshow('Overlayed Image', background)
cv2.waitKey(0)
cv2.destroyAllWindows()
