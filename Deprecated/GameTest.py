# from typing import Tuple
# from typing import Optional, Dict
# from GameField import *
# from Cell import *
# from Figure import *
# from Event import Event
# from Item import *
# from Map import *
# from PositionDetection import *
# from ImageTransformer import *
# from GitterErkennung import *

# # --------------------------------------------------------------- BILDPFADE ---------------------------------------------------------------#
# map_disk_path = "Assets\\encounter.webp"
# overlay_trap = "Assets\\overlay_trap.png"

# # --------------------------------------------------------------- VORBEREITUNG ---------------------------------------------------------------#
# map = Map(map_disk_path)
# image_transformer = ImageTransformer()

# map.rotate_map(90)
# map.resize_map()
# map.display_map("Map")
# cv2.waitKey(0)

# # ------------------------------------------------------------ SPIELFELD INITIALISIEREN -------------------------------------------------------#
# # 1.    Anzahl der Objekte festlegen
# game_field_height = 40 
# game_field_width = 50 
# event_count = 2
# item_count = 2
# figure_sequence = []

# game_field = GameField(game_field_height,game_field_width,map)

# figure_sequence.append(game_field.add_figure("P1",Figure_Type.PLAYER,(0,0),1))

# figure_sequence.append(game_field.add_figure("E1",Figure_Type.ENEMY,(4,4),1))
# print("Figuren hinzugefügt")

# # 5.	Events verteilen
# # ToDo: Events Randomized verteilen --> Felder ausschließen wo Spieler stehen
# # ToDo: Event Klasse nochmal neu überdenken
# # ToDo: VisuStates der Events anlegen

# game_field.add_event(Event_Type.Trap,(6,6),1)
# game_field.add_event(Event_Type.Fire,(5,5),1)
# print("Events hinzugefügt")

# # 6.	Items verteilen
# # ToDo: Items Randomized verteilen --> Felder ausschließen wo Spieler stehen

# # --------------------------------------------------------------- GAME-LOOP -----------------------------------------------------------------#
# finished = False
# round = 0
# all_figures_count = len(figure_sequence)
# selected_figure = 0

# if all_figures_count:
#     while(not finished):
#         selected_figure = figure_sequence[round % all_figures_count]
#         start_pos = selected_figure.position  
#         print(f"Aktuelle Position: {selected_figure.position}")
#         map.figure_radius(start_pos,selected_figure.size)


#         end_pos = (5+round,5+round)
#         game_field.move_figure(selected_figure,start_pos,end_pos)   
#         map.remove_overlay("Assets\\player_radius.png",start_pos,selected_figure.size*5)      
            
#         print(f"Figur {selected_figure.id} wurde bewegt. Neue Position: {selected_figure.position}")

#         map.display_map("Map")
#         cv2.waitKey(0)
#         round += 1



