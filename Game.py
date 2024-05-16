from gamelogic.GameField import *
from gamelogic.Cell import *
from gamelogic.Figure import *
from gamelogic.Event import *
from gamelogic.Item import *
from imageprocessing.ImageProcessor import *
from imageprocessing.ImageTransformer import *

# ----------------------------------------------------- VORBEREITUNG -----------------------------------------------------


# Bildpfad angeben
beamer_image_path = "Assets\\encounter.webp"
background_image_path = "Assets\\background.jpg"
camera_image_path = "Assets\\background_with_figure.jpg"

# Instanz von ImageProcessor erstellen
beamer_imgProcessor = ImageProcessor(beamer_image_path)
camera_imgTransformer = ImageTransformer()

# Bild um X Grad drehen
beamer_imgProcessor.rotate_image(90)
# Bild auf Beamergröße skalieren
beamer_imgProcessor.resize_image()
# Bild anzeigen in Window Main
beamer_imgProcessor.display_image("Main")


# SCREENSHOT OHNE FIGUR
transformed_image1 = camera_imgTransformer.transform_image(background_image_path)
cv2.imshow('Channel1',transformed_image1)

cv2.waitKey(0)

# ToDo: Hier muss die GITTERERKENNUNG rein und die Zellen in x und y Richtung liefern

game_field_height = 40 # Hier muss die Zahl aus Background-Subtraction hinzugefügt werden!
game_field_width = 50 


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




# 3. Player Figuren --> Schleife die durch player_count begrenzt ist



for i in range(1,player_count+1):
    # FIGUR DRAUFSTELLEN
    # SCREENSHOT MIT FIGUR --> 
    transformed_image2 = camera_imgTransformer.transform_image(camera_image_path)
    cv2.imshow('Channel2',transformed_image2)
    
    # ToDo Max: PositionDetection(transformed_image1,transformed_image1,(50,40))
    position = (0,0)   

    figure_sequence.append(game_field.add_figure(f'Player_{i}',Figure_Type.PLAYER,position,1))
    
    # ToDo: WHile Schleife solange keine neuen Figuren draufgesetzt werden


# 4.	Selbe Schleife für Gegner Figuren --> Schleife mit Anzahl Gegner X

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
game_field.set_visu_state((10,10),VisuState_Img.TRAP)
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
    
    game_field.set_visu_state((8,10),VisuState_Img.TRAP)
    game_field.visualize_GameField() # GameField visualisieren in Terminal

    # 7.	Next Player() 
    round += 1


