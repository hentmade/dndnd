import cv2

class Overlay:
    def __init__(self, background):
        self.foreground= []
        self.background = background

    def putOverlay(self):
        if self.foreground is not None:
            for image in self.foreground:
                img = cv2.imread(image["path"])
                image_height, image_width, _ = img.shape
                x_offset, y_offset = image["position"]
                self.background[y_offset:y_offset+image_height, x_offset:x_offset+image_width] = img
            return self.background

    def addImage(self,path,position):
        self.foreground.append({"path": path, "position": position})
        
        
        
        
# Das wird in der VisualizeGamefield aufgerufen
background_path = "Assets\\encounter.webp"
image_path = "Assets\\overlay.png"

background = cv2.imread(background_path)

cv2.imshow("Initial", background)

overlay = Overlay(background)

cv2.waitKey(0)
cv2.destroyAllWindows()

for i in range(1,5):    

    position = (100+5*i,50+5*i) # Hier muss die Umrechnung Cell-Position --> Image Position stattfinden

    overlay.addImage(image_path,position)

    background_with_overlay = overlay.putOverlay()

    cv2.imshow("Overlay-Ergebnis", background_with_overlay)

    cv2.waitKey(0)

cv2.destroyAllWindows()