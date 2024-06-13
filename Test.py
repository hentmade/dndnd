from GameField import *
from Cell import *
from Figure import *
from Event import *
from Item import *
from Map import *
from ImageTransformer import *




# Initialisierung
game_field_height = 40 
game_field_width = 50 
player_count = 2
enemy_count = 2
event_count = 2
item_count = 2
figure_sequence = []
game_field = GameField(game_field_height,game_field_width)



# Figure - Player
for i in range(1,player_count+1):    
    position = (i,0)   
    figure_sequence.append(game_field.add_figure(f'Player_{i}',Figure_Type.PLAYER,position,1))
    

# Figure - Enemy
for i in range(1,enemy_count+1):
    position = (10+i,9)   
    figure_sequence.append(game_field.add_figure('Enemy_{i}',Figure_Type.ENEMY,position,1))


# Events
#game_field.add_event("TRAP",(5,5),1)


# Items



# Visu-State / Visu-Image
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


    start_pos = selected_figure.position

    print(f"\nStartposition {selected_figure.id} einlesen... ")
    input() 
    print(f"Aktuelle Position: {selected_figure.position}")

    print("Figur umstellen und mit ENTER bestätigen!")
    input()
    x,y = start_pos
    end_pos = (x + 1 , y + 1)
    
    # 3.	Figur bewegen 
    game_field.move_figure(selected_figure,start_pos,end_pos)

    print(f"Figur {selected_figure.id} wurde bewegt. Neue Position: {selected_figure.position}")
    print("Ready Next Player... (ENTER)")
    input()
    

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
    
    #game_field.set_visu_state((8,10),VisuState_Img.TRAP)
    #game_field.visualize_GameField() # GameField visualisieren in Terminal


    round += 1


