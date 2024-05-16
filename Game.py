from gamelogic.GameField import *
from gamelogic.Cell import *
from gamelogic.Figure import *
from gamelogic.Event import *
from gamelogic.Item import *
from imageprocessing.ImageProcessor import *



# ----------------------------------------------------- VORBEREITUNG -----------------------------------------------------


# 1. Bild über Beamer projizieren
beamer_image_path = "Assets\\encounter.webp"
beamer_imgProcessor = ImageProcessor(beamer_image_path)


# 2. Bild über Kamera einlesen
camera_image_path = "Assets\\map_with_figure.jpg"
camera_imgProcessor = ImageProcessor(camera_image_path)


# 3. Bild vorverarbeiten und anzeigen
beamer_imgProcessor.rotate_image(90) # Bild um X Grad drehen 
beamer_imgProcessor.resize_image() # Bild auf Beamergröße skalieren
beamer_imgProcessor.display_image("Main") # Bild anzeigen in Window Main
transformed_image = camera_imgProcessor.transform_image() # Kamera-Bild transformieren und für Weiterverarbeitung vorbereiten
cv2.waitKey(0)

# 4. Grid erkennen und Cell-Size ermitteln 
# ToDo: Height und Width in Zellenanzahl ermitteln über Background-Subtractio

game_field_height = 20 # Hier muss die Zahl aus Background-Subtraction hinzugefügt werden!
game_field_width = 20 # 

#cv2.imshow('Channel',transformed_image) # Transformiertes Kamera-Bild in Window Channel anzeigen



# -------------------------------------------------- SPIELFELD INITIALISIEREN --------------------------------------------------

# Background-Subtraction liefert uns bestensfalls die Position der Figur als Position der Zelle
# Außerdem liefert uns Background-Subtraction im ersten Schritt erstmal die Anzahl der Zellen Höhe & Breite

# 1. Anzahl der Objekte festlegen
# ToDo: Interaktive Eingabe der Counts


player_count = 2
enemy_count = 2
event_count = 2
item_count = 2

# 2. Über Height / Width das Spielfeld erstellen und initialisieren

game_field = GameField(game_field_height,game_field_width)
game_field.field_corners = camera_imgProcessor.clicked_points  # ToDo: Angeklickte Punkte merken und immer in Gameloop anwenden!
game_field.initialize_GameField()


# 3. Player Figuren --> Schleife die durch player_count begrenzt ist
# ToDo:
#       a.	Erste Figur aufs Spielfeld stellen
#       b.	Figur erkennen über Background-Subtraction
#       c.	Position der Figur erkennen
#       d.	Figur benennen z.B. erste Player Figur  Player_1  bis Player_X
#       e.	Type auf PLAYER stellen
#       f.	Add_Figure()

game_field.add_figure('Player1',Figure_Type.PLAYER,(8,2),1)


# 4.	Selbe Schleife für Gegner Figuren  Schleife mit Anzahl Gegner X
#       a.	Erste Figur aufs Spielfeld stellen
#       b.	Figur erkennen über Background-Subtraction
#       c.	Position der Figur erkennen
#       d.	Figur benennen z.B. erste Gegner Figur  Enemy_1  bis Enemy_X
#       e.	Type auf PLAYER stellen
#       f.	Add_Figure()

game_field.add_figure('Enemy1',Figure_Type.ENEMY,(10,9),1)


# 5.	Events verteilen
#       a.	Schauen, dass dort Figure auf None steht
#       b.	Random ODER hardcoden

# ToDo: Events Randomized verteilen
game_field.add_event("TRAP",(2,2),1)


# 6.	Items verteilen
#       a.	Schauen, dass dort Figure auf None steht
#       b.	Random ODER hardcoden

# ToDo: Items Randomized verteilen



# 8.	VisuStates setzen
#       a.	Items anzeigen z.B. Schatztruhen, Fackeln
#       b.	Evtl. Events anzeigen

# ToDo: VisuStates für Items und Events etc. anlegen
game_field.set_visu_state((0,0),VisuState.FIRE)
game_field.set_visu_state((5,5),VisuState.WATER)
game_field.set_visu_state((0,10),VisuState.EARTH)


game_field.visualize_GameField() # GameField visualisieren in Terminal


# ----------------------------------------------------- GAME-LOOP -------------------------------------------------------

# -	Nach der Reihenfolge Player_1 bis Player_X 
# -	danach Gegner_1 bis Gegner_X

# 1.	Figur die dran ist auswählen
# 2.	Startposition der Figur einlesen
# 3.	Figur bewegen 
# 4.	Endposition der Figur einlesen
# 5.	Move_Figure(Start,Ende) ausführen
# 6.	Trigger()-Funktion auslösen
#       a.	Liest aus ob die Ziel-Zelle ein Event enthält 
#       b.	Event auslösen
# 7.	VisuStates() neu setzen und anzeigen
# 8.	Aktionen ausführen
#       a.	Item anklicken, wenn Spielerfigur im Abstand 1 zu dem Item steht
# 9.	VisuStates() neu setzen und anzeigen
# 10.	Next Player() 

