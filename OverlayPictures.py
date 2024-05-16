import cv2

# Hintergrundbild laden
hintergrund = cv2.imread("Assets\\hintergrund.jpg")

# Liste der Overlay-Bilder mit ihren Positionen
overlay_bilder = [
    {"pfad": "Assets\\overlay.png", "position": (100, 50)},
    {"pfad": "Assets\\overlay.png", "position": (200, 150)},
    # Weitere Overlay-Bilder und ihre Positionen hier hinzufügen...
]

# Overlay-Bilder auf dem Hintergrundbild platzieren
for overlay_info in overlay_bilder:
    overlay_bild = cv2.imread(overlay_info["pfad"])

    # Die Größe des Overlay-Bildes erhalten
    overlay_höhe, overlay_breite, _ = overlay_bild.shape

    # Position des Overlay-Bildes
    x_offset, y_offset = overlay_info["position"]

    # Overlay-Bild auf dem Hintergrundbild platzieren
    hintergrund[y_offset:y_offset+overlay_höhe, x_offset:x_offset+overlay_breite] = overlay_bild

# Ergebnis anzeigen
cv2.imshow("Overlay-Ergebnis", hintergrund)
cv2.waitKey(0)
cv2.destroyAllWindows()
