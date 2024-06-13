from typing import Tuple
from typing import Optional, Dict
from GameField import *
from Cell import *
from Figure import *
from Event import *
from Item import *
from Map import *
from PositionDetection import *
from ImageTransformer import *
from GitterErkennung import *
import mouse
import mss
import os

# --------------------------------------------------------------- BILDPFADE ---------------------------------------------------------------#
map_disk_path = "Assets\\encounter.webp"
overlay_trap = "Assets\\overlay_trap.png"

# --------------------------------------------------------------- VORBEREITUNG ---------------------------------------------------------------#
map = Map(map_disk_path)
image_transformer = ImageTransformer()

map.rotate_map(90)
map.resize_map()
map.display_map("Map")
cv2.waitKey(0)

# ------------------------------------------------------------ SPIELFELD INITIALISIEREN -------------------------------------------------------#
# 1.    Anzahl der Objekte festlegen
game_field_height = 40 
game_field_width = 50 
event_count = 2
item_count = 2
figure_sequence = []

game_field = GameField(game_field_height,game_field_width,map)

figure_sequence.append(game_field.add_figure("P1",Figure_Type.PLAYER,(0,0),1))

figure_sequence.append(game_field.add_figure("E1",Figure_Type.ENEMY,(4,4),1))
print("Figuren hinzugefügt")

# 5.	Events verteilen
# ToDo: Events Randomized verteilen --> Felder ausschließen wo Spieler stehen
# ToDo: Event Klasse nochmal neu überdenken
# ToDo: VisuStates der Events anlegen

game_field.add_event(Event_Type.TRAP,(2,2),1)
print("Events hinzugefügt")

# 6.	Items verteilen
# ToDo: Items Randomized verteilen --> Felder ausschließen wo Spieler stehen

# --------------------------------------------------------------- GAME-LOOP -----------------------------------------------------------------#
finished = False
round = 0
all_figures_count = len(figure_sequence)
selected_figure = 0

if all_figures_count:
    while(not finished):
        selected_figure = figure_sequence[round % all_figures_count]
        start_pos = selected_figure.position  
        print(f"Aktuelle Position: {selected_figure.position}")
        end_pos = (2,2)
        game_field.move_figure(selected_figure,start_pos,end_pos)
    
            
        print(f"Figur {selected_figure.id} wurde bewegt. Neue Position: {selected_figure.position}")
        print("Ready Next Player... (ENTER)")
        input()
        

        # 5.	Aktionen ausführen
        # ToDo: Item-Klasse anpassen
        # ToDo - Test: Figur vor Item stellen und Item auslösen bei Klick

        # 6.	VisuStates() neu setzen und anzeigen
        # ToDo: Nachdem Figuren bewegt und Events / Items getriggert wurden 
        #       --> VisuState der Zelle auslesen und anzeigen
        #       --> VisuState der Zelle muss noch festgelegt werden z.B. Event / Item wird als Overlay drübergelegt
        # ToDo: VisuStates für Items und Events etc. anlegen

        # 7.    Game Field neu zeichnen + Next Player
        # ToDo: VisuStates der betroffenen Zellen neu auslesen und den entsprechenden Overlay dem Overlay-Array hinzufügen
        #       --> Nach Vorbild OverlayPicture.py
        # ToDo: Spielende festlegen
        # ToDo: Overlay müssen auf eine Cell gefittet werden -->  map.add_overlay(cell.visuState,(100,100))

        cv2.destroyWindow("Map")
        map.display_map("Map")
        cv2.waitKey(0)
        round += 1



