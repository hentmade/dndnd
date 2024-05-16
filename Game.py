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
figure_sequence = []

# 2. Über Height / Width das Spielfeld erstellen und initialisieren

game_field = GameField(game_field_height,game_field_width)
game_field.field_corners = camera_imgProcessor.clicked_points  # ToDo: Angeklickte Punkte merken und immer in Gameloop anwenden!
game_field.initialize_GameField()


# 3. Player Figuren --> Schleife die durch player_count begrenzt ist
# ToDo:
#       a.	Erste Figur aufs Spielfeld stellen
#       b.	Figur erkennen über Background-Subtraction
#       c.	Position der Figur erkennen
#       d.	Figur benennen z.B. erste Player Figur --> Player_1  bis Player_X
#       e.	Type auf PLAYER stellen
#       f.	Add_Figure()
#       g.  Figur in Spielerreihenfolge aufnehmen

for i in range(1,player_count+1):
    figure_sequence.append(game_field.add_figure(f'Player_{i}',Figure_Type.PLAYER,(0,i),1))


# 4.	Selbe Schleife für Gegner Figuren  Schleife mit Anzahl Gegner X
#       a.	Erste Figur aufs Spielfeld stellen
#       b.	Figur erkennen über Background-Subtraction
#       c.	Position der Figur erkennen
#       d.	Figur benennen z.B. erste Gegner Figur  Enemy_1  bis Enemy_X
#       e.	Type auf PLAYER stellen
#       f.	Add_Figure()
for i in range(1,enemy_count+1):
    figure_sequence.append(game_field.add_figure('Enemy_{i}',Figure_Type.ENEMY,(10+i,9),1))


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
finished = False
round = 0
all_figures_count = player_count + enemy_count
selected_figure = 0


while(not finished):
    # 1.	Figur die dran ist auswählen
    # Nach der Reihenfolge Player_1 bis Player_X, danach Gegner_1 bis Gegner_X
    selected_figure = (Figure)(figure_sequence[round % all_figures_count])
    
    # 2.	Start- und Endposition der Figur einlesen
    start_pos = selected_figure.position  # ToDo: Die Start-Positionen müssen später über Kamera eingelesen werden
    end_pos = (5,5) # ToDo: Die End-Positionen müssen später über Kamera eingelesen werden --> statt start_pos+1
    
    # 3.	Figur bewegen 
    game_field.move_figure(selected_figure,start_pos,end_pos)
    

    # 4.	Cell.Trigger(new_position)-Funktion auslösen 
    #       --> Trigger Funktion ist vom Event selber, Zelle braucht noch eine CheckEvent() Funktion
    #       --> Zelle an der neuen Position auswerten
    #       --> Schauen ob an der Zelle ein Event
    #       --> Wenn Ja Trigger()
  

    # 5.	Aktionen ausführen
    #       a.	Item anklicken, wenn Spielerfigur im Abstand 1 zu dem Item steht
    # ToDo: Item-Klasse anpassen

    # 6.	VisuStates() neu setzen und anzeigen
    #       --> Funktion RefreshVisuStates(): Events etc. müssen die VisuStates verändern! 
    #       --> Visualisierung des Events auf Cell projizieren
    
    game_field.set_visu_state((0,10),VisuState.EARTH)
    game_field.visualize_GameField() # GameField visualisieren in Terminal

    # 7.	Next Player() 
    round += 1


