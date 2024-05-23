from GameField import *
from Cell import *
from Figure import *
from Event import *
from Item import *
from ImageProcessor import *
from ImageTransformer import *


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

# Screenshot ohne Figur
transformed_image1 = camera_imgTransformer.transform_image(background_image_path)
cv2.imshow('Channel1',transformed_image1)
cv2.waitKey(0)


# ToDo: Hier muss die GITTERERKENNUNG rein und die Zellen in x und y Richtung liefern
game_field_height = 40 
game_field_width = 50 


# -------------------------------------------------- SPIELFELD INITIALISIEREN --------------------------------------------------

# ToDo: Interaktive Eingabe der Counts

# 1.    Anzahl der Objekte festlegen
player_count = 2
enemy_count = 2
event_count = 2
item_count = 2
figure_sequence = []

# 2.    Über Height / Width das Spielfeld erstellen und initialisieren
game_field = GameField(game_field_height,game_field_width) 

# 3.    Player Figuren anlegen
for i in range(1,player_count+1):
    transformed_image2 = camera_imgTransformer.transform_image(camera_image_path)
    cv2.imshow('Channel2',transformed_image2)
    
    # ToDo Max: PositionDetection(transformed_image1,transformed_image1,(50,40))
    #FIGUR DRAUFSTELLEN --> SCREENSHOT MIT FIGUR

    position = (i,0)   
    figure_sequence.append(game_field.add_figure(f'Player_{i}',Figure_Type.PLAYER,position,1))
    
    # ToDo: Umzuschreiben zu While Schleife solange keine neuen Figuren draufgesetzt werden 


# 4.    Gegner Figuren anlegen
for i in range(1,enemy_count+1):
    position = (10+i,9)   
    figure_sequence.append(game_field.add_figure('Enemy_{i}',Figure_Type.ENEMY,position,1))

    # ToDo: Umzuschreiben zu While Schleife solange keine neuen Figuren draufgesetzt werden 

# 5.	Events verteilen
# ToDo: Events Randomized verteilen
#  game_field.add_event("TRAP",(2,2),1)


# 6.	Items verteilen
# ToDo: Items Randomized verteilen


# 7.    Game Field zeichnen
#game_field.set_visu_state((10,10),VisuState_Img.TRAP)
#game_field.visualize_GameField() # GameField visualisieren in Terminal


# ----------------------------------------------------- GAME-LOOP -------------------------------------------------------
finished = False
round = 0
all_figures_count = player_count + enemy_count
selected_figure = 0


while(not finished):
    # 1.	Figur die dran ist auswählen
    # Nach der Reihenfolge Player_1 bis Player_X, danach Gegner_1 bis Gegner_X
    selected_figure = figure_sequence[round % all_figures_count]
    
    # 2.	Start- und Endposition der Figur einlesen
    start_pos = selected_figure.position  
    # ToDo: Die Start-Positionen müssen später über Kamera eingelesen werden
    print(f"\nStartposition {selected_figure.id} einlesen... ")
    input() 
    print(f"Aktuelle Position: {selected_figure.position}")
    print("Figur umstellen und mit ENTER bestätigen!")
    input()
    x,y = start_pos
    end_pos = (x + 1 , y + 1) 
    # ToDo: Die End-Positionen müssen später über Kamera eingelesen werden
    
    # 3.	Figur bewegen 
    game_field.move_figure(selected_figure,start_pos,end_pos)
    print(f"Figur {selected_figure.id} wurde bewegt. Neue Position: {selected_figure.position}")
    print("Ready Next Player... (ENTER)")
    input()

    # 4.	Cell.Trigger(new_position)-Funktion auslösen 
    # ToDo - Test: Figur auf Event bewegen und auslösen
    #       --> Trigger Funktion ist vom Event selber, Zelle braucht noch eine CheckEvent() Funktion
    #       --> Zelle an der neuen Position auswerten
    #       --> Schauen ob an der Zelle ein Event
    #       --> Wenn Ja Trigger()
  

    # 5.	Aktionen ausführen
    # ToDo: Item-Klasse anpassen
    # ToDo - Test: Figur vor Item stellen und Item auslösen bei Klick

    # 6.	VisuStates() neu setzen und anzeigen
    # ToDo: Nachdem Figuren bewegt und Events / Items getriggert wurden 
    #       --> VisuState der Zelle auslesen und anzeigen
    #       --> VisuState der Zelle muss noch festgelegt werden z.B. Event / Item wird als Overlay drübergelegt
    # ToDo: VisuStates für Items und Events etc. anlegen
    
    #game_field.set_visu_state((8,10),VisuState_Img.TRAP)
    #game_field.visualize_GameField() # GameField visualisieren in Terminal

    # 7.    Game Field neu zeichnen + Next Player
    # ToDo: VisuStates der betroffenen Zellen neu auslesen und den entsprechenden Overlay dem Overlay-Array hinzufügen
    #       --> Nach Vorbild OverlayPicture.py
    round += 1


