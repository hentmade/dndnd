from GameField import *
from Cell import *
from Figure import *
from Event import *
from Item import *
from ImageProcessor import *
from ImageTransformer import *
import pyautogui
import mouse
import mss


region = None

def place_figures(figure_type, region=None):
    save_path="Assets\\map_with_figure_screenshot.png"
    i = 0
    while True:        
        answer = input("Möchtest du neue Figuren auf das Brett stellen? (J/N): ").strip().upper()
        if answer == "N":
            break
        elif answer == "J":
            region = take_screenshot(without_figure_image_path,region)
            transformed_map_without_image = camera_imgTransformer.transform_image(without_figure_image_path)
            cv2.imshow('CameraFigure1',transformed_map_without_image)
            cv2.waitKey()
            print("Stelle eine neue Figur aufs Spielfeld und bestätige mit ENTER.")
            input()
            region = take_screenshot(with_figure_image_path,region)
            transformed_map_with_image = camera_imgTransformer.transform_image(with_figure_image_path)
            cv2.imshow('CameraFigure2',transformed_map_with_image)
            cv2.waitKey()
            # ToDo Max: PositionDetection(transformed_image1,transformed_image1,(50,40))
            # FIGUR DRAUFSTELLEN --> SCREENSHOT MIT FIGUR             
            position = (i,0) 
            figure_sequence.append(game_field.add_figure(f'Figure_{i}',figure_type,position,1))
            i = i + 1
        else:
            print("Ungültige Eingabe. Bitte gib 'J' für Ja oder 'N' für Nein ein.")

    return region


def take_screenshot(save_path="Assets\\map_screenshot.png", region=None):
    if region is None:
        print("Bitte wähle den oberen linken Punkt des Kamera-Bildes OHNE Figur.")
        x1, y1 = get_click_position()
        print(f"Erster Punkt gewählt: ({x1}, {y1})")
        print("Wähle den unteren rechten Punkt des Kamera-Bildes OHNE Figur.")
        x2, y2 = get_click_position()
        print(f"Zweiter Punkt gewählt: ({x2}, {y2})")
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        region = {
        "left": left,
        "top": top,
        "width": width,
        "height": height
            }
    print(f"Region zum Screenshot: {region}")
    # Screenshot der angegebenen Region machen
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)
    print(f"Screenshot gespeichert als {save_path}")
    return region
    # screenshot = pyautogui.screenshot(region=region)
    # # Screenshot speichern
    # screenshot.save(save_path)
    # print(f"Screenshot gespeichert als {save_path}")
     

def get_click_position():
    print("Bitte klicke, um eine Position zu wählen...")
    pos = None
    while pos is None:
        if mouse.is_pressed(button='left'):
            pos = mouse.get_position()
            while mouse.is_pressed(button='left'):
                pass
    return pos


# ----------------------------------------------------- VORBEREITUNG -----------------------------------------------------
# Bildpfad angeben
beamer_image_path = "Assets\\encounter.webp"
background_image_path = "Assets\\background.jpg"
camera_image_path = "Assets\\background_with_figure.jpg"
without_figure_image_path = "Assets\\map_without_figure_screenshot.png"
with_figure_image_path = "Assets\\map_with_figure_screenshot.png"

# Instanz von ImageProcessor erstellen
beamer_imgProcessor = ImageProcessor(beamer_image_path)
camera_imgTransformer = ImageTransformer()


# Bild um X Grad drehen
beamer_imgProcessor.rotate_image(90)
# Bild auf Beamergröße skalieren
beamer_imgProcessor.resize_image()
# Bild anzeigen in Window Main


print("---- PRESS ENTER TO START ----")
input()

beamer_imgProcessor.display_image("Map")
cv2.waitKey(0)
# Screenshot Kamerabild ohne Figur machen und speichern
# ToDo - Test: Mit Kamerabild
#take_screenshot(without_figure_image_path)


#transformed_map_without_image = camera_imgTransformer.transform_image(without_figure_image_path)
#cv2.imshow('Camera',transformed_map_without_image)

# ToDo: Hier muss die GITTERERKENNUNG rein und die Zellen in x und y Richtung liefern


# -------------------------------------------------- SPIELFELD INITIALISIEREN --------------------------------------------------
# ToDo: Interaktive Eingabe der Counts


# 1.    Anzahl der Objekte festlegen
game_field_height = 40 
game_field_width = 50 
player_count = 2
enemy_count = 2
event_count = 2
item_count = 2
figure_sequence = []


# 2.    Über Height / Width das Spielfeld erstellen und initialisieren
game_field = GameField(game_field_height,game_field_width) 

# 3. Player Figuren placen
region = place_figures(Figure_Type.PLAYER)

# 4. Enemy Figuren placen
region = place_figures(Figure_Type.ENEMY,region)

# 3.    Player Figuren anlegen
# for i in range(1,player_count+1):      
#     position = (i,0)   
#     figure_sequence.append(game_field.add_figure(f'Player_{i}',Figure_Type.PLAYER,position,1))    
#     # ToDo: Umzuschreiben zu While Schleife solange keine neuen Figuren draufgesetzt werden 


# 4.    Gegner Figuren anlegen
# for i in range(1,enemy_count+1):
#     position = (10+i,9)   
#     figure_sequence.append(game_field.add_figure('Enemy_{i}',Figure_Type.ENEMY,position,1))
#     # ToDo: Umzuschreiben zu While Schleife solange keine neuen Figuren draufgesetzt werden 


# 5.	Events verteilen
# ToDo: Events Randomized verteilen
# ToDo: Event Klasse nochmal neu überdenken
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
    selected_figure = figure_sequence[round % (all_figures_count+1)]
    

    # 2.	Start- und Endposition der Figur einlesen
    start_pos = selected_figure.position  
    # ToDo: Die Start-Positionen müssen später über Kamera eingelesen werden
    print(f"\nStartposition {selected_figure.id} einlesen... ")
    input() 
    region = take_screenshot(without_figure_image_path,region)
    print(f"Aktuelle Position: {selected_figure.position}")
    print("Figur umstellen und mit ENTER bestätigen!")
    input()
    region = take_screenshot(without_figure_image_path,region)    
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
    # ToDo: Spielende festlegen
    round += 1


