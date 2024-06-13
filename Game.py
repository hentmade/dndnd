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
import mouse
import mss
import os

# --------------------------------------------------------------- BILDPFADE ---------------------------------------------------------------#
beamer_image_path = "Assets\\encounter.webp"
screenshot_prev_path = "Assets\\map_screenshot_prev.png"
screenshot_next_path = "Assets\\map_screenshot_next.png"
overlay_trap = "Assets\\overlay_trap.png"

# --------------------------------------------------------------- FUNKTIONEN ---------------------------------------------------------------#
def place_figures(figure_type, region: Optional[dict] = None) -> dict:
    """
    Allows the user to place new figures of a specified type on a game board by capturing screenshots before and after placing each figure.
    
    Args:
        figure_type (FigureType): The type of figure to be placed on the game board.
        region (dict, optional): The region of the screen to capture for screenshots.

    Returns:
        dict: The region dictionary containing the 'left', 'top', 'width', and 'height' of the captured region.
    """
    i = 0
    region = take_screenshot(screenshot_prev_path, region)
    screenshot_prev = cv2.imread(screenshot_prev_path)
    screenshot_prev = image_transformer.transform_image(screenshot_prev)
    
    while True:
        answer = input(f"Möchtest du neue {figure_type.value}-Figuren auf das Brett stellen? (J/N): ").strip().upper()
        
        if answer == "N":
            break
        elif answer == "J":
            #cv2.imshow('Screenshot Previous', screenshot_prev)
            #cv2.waitKey(0)
            print(f"Stelle eine neue {figure_type.value}-Figur aufs Spielfeld und bestätige mit ENTER.")
            input()
            
            region = take_screenshot(screenshot_next_path, region)
            screenshot_next = cv2.imread(screenshot_next_path)
            screenshot_next = image_transformer.transform_image(screenshot_next)
            #cv2.imshow('Screenshot Next', screenshot_next)
            #cv2.waitKey(0)
            
            position = position_detector.detectPosition(screenshot_next, screenshot_prev)
            print(f"Position: {position}")
            
            figure_sequence.append(game_field.add_figure(f'{figure_type.value}_{i}', figure_type, position, 1))
            i += 1
            screenshot_prev = screenshot_next
        else:
            print("Ungültige Eingabe. Bitte gib 'J' für Ja oder 'N' für Nein ein.")
    
    print(f"Alle {figure_type.value}-Figuren platziert.")
    return region



def take_screenshot(save_path: str = "Assets\\map_screenshot.png", region: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    """
    Capture a screenshot of a specified region on the screen.

    Args:
        save_path (str): The file path where the screenshot will be saved. Default is "Assets\\map_screenshot.png".
        region (dict): A dictionary specifying the region to capture. If None, the user will be prompted to select the region.

    Returns:
        dict: A dictionary containing the 'left', 'top', 'width', and 'height' of the captured region.
    """
    if region is None:
        print("\nPlease select the top-left point of the camera image without any figure.")
        x1, y1 = get_click_position()
        print("\nSelect the bottom-right point of the camera image without any figure.")
        x2, y2 = get_click_position()
        left, top = min(x1, x2), min(y1, y2)
        width, height = abs(x2 - x1), abs(y2 - y1)
        region = {"left": left, "top": top, "width": width, "height": height}

    with mss.mss() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)

    return region



def get_click_position() -> Tuple[int, int]:
    """
    Waits for the user to click the left mouse button and returns the coordinates of the click position.
    
    Returns:
    Tuple[int, int]: A tuple containing the x and y coordinates of the mouse click position.
    """
    print("Bitte klicke, um eine Position zu wählen...")
    pos = None
    while pos is None:
        if mouse.is_pressed(button='left'):
            pos = mouse.get_position()
            while mouse.is_pressed(button='left'):
                pass
    return pos

# --------------------------------------------------------------- VORBEREITUNG ---------------------------------------------------------------#
map = Map(beamer_image_path)
image_transformer = ImageTransformer()

map.rotate_map(90)
map.resize_map()
map.display_map("Map")
cv2.waitKey(0)

# ToDo: Hier muss die GITTERERKENNUNG rein und die Zellen in x und y Richtung liefern

# ------------------------------------------------------------ SPIELFELD INITIALISIEREN -------------------------------------------------------#
# 1.    Anzahl der Objekte festlegen
game_field_height = 40 
game_field_width = 50 
event_count = 2
item_count = 2
figure_sequence = []

game_field = GameField(game_field_height,game_field_width)
position_detector = PositionDetection(game_field_width,game_field_height)

region = place_figures(Figure_Type.PLAYER)

region = place_figures(Figure_Type.ENEMY,region)

# 5.	Events verteilen
# ToDo: Events Randomized verteilen --> Felder ausschließen wo Spieler stehen
# ToDo: Event Klasse nochmal neu überdenken
# ToDo: VisuStates der Events anlegen
#  game_field.add_event("TRAP",(2,2),1)

# 6.	Items verteilen
# ToDo: Items Randomized verteilen --> Felder ausschließen wo Spieler stehen

# --------------------------------------------------------------- GAME-LOOP -----------------------------------------------------------------#
finished = False
round = 0
all_figures_count = len(figure_sequence)
selected_figure = 0

if all_figures_count:
    region = take_screenshot(screenshot_prev_path,region)
    screenshot_prev = cv2.imread(screenshot_prev_path)
    screenshot_prev = image_transformer.transform_image(screenshot_prev)
    while(not finished):
        selected_figure = figure_sequence[round % all_figures_count]
        start_pos = selected_figure.position  
        print(f"Aktuelle Position: {selected_figure.position}")
        print("Figur umstellen und mit ENTER bestätigen!")
        input()
        region = take_screenshot(screenshot_next_path,region)
        screenshot_next = cv2.imread(screenshot_next_path)
        screenshot_next = image_transformer.transform_image(screenshot_next)  
        end_pos = position_detector.detectPosition(screenshot_next,screenshot_prev)
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

        # 7.    Game Field neu zeichnen + Next Player
        # ToDo: VisuStates der betroffenen Zellen neu auslesen und den entsprechenden Overlay dem Overlay-Array hinzufügen
        #       --> Nach Vorbild OverlayPicture.py
        # ToDo: Spielende festlegen
        # ToDo: Overlay müssen auf eine Cell gefittet werden -->  map.add_overlay(cell.visuState,(100,100))

        cv2.destroyWindow("Map")
        map.display_map("Map")
        cv2.waitKey(0)
        round += 1
        screenshot_prev = screenshot_next


