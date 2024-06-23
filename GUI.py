import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
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


screenshot_prev_path = "Assets\\map_screenshot_prev.png"
screenshot_next_path = "Assets\\map_screenshot_next.png"
screenshot_path = "Assets\\map_screenshot.png"

class Application(tk.Tk):
    X_POS_MIN = 0
    X_POS_MAX = 100
    Y_POS_MIN = 0
    Y_POS_MAX = 100

    def __init__(self, X_POS_MAX, Y_POS_MAX):
        super().__init__()
        self.X_POS_MAX = X_POS_MAX
        self.Y_POS_MAX = Y_POS_MAX
        self.title("GUI Application")
        self.geometry("400x500")
        self.running = False        
        self.create_widgets()
        self.map_path = None  # Variable to store the path to the map
        self.map = None
        self.map_window = None  # Variable to store the map window
        self.map_image = None  # Variable to store the map image
        self.map_label = None  # Label to display the map image
        self.game_field = None
        self.position_detector = None
        self.rotation_angle = 0
        self.camera = None
        self.screenshot_path = screenshot_path
        self.region = None

        self.withdraw()  # Hide the main window initially
        self.show_start_window()
        
    def create_widgets(self):
        # Button to start
        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.pack(pady=10)
        
        # Button to end
        self.end_button = tk.Button(self, text="End", command=self.end)
        self.end_button.pack(pady=10)
        
        # Button for next round
        self.next_round_button = tk.Button(self, text="Next Round", command=self.next_round)
        self.next_round_button.pack(pady=10)
        
        # Dropdown menu for skip X rounds
        self.skip_rounds_frame = tk.Frame(self)
        self.skip_rounds_frame.pack(pady=10)
        
        self.skip_label = tk.Label(self.skip_rounds_frame, text="Skip")
        self.skip_label.pack(side=tk.LEFT)
        
        self.rounds_var = tk.IntVar(value=1)
        self.skip_rounds_dropdown = ttk.Combobox(self.skip_rounds_frame, textvariable=self.rounds_var)
        self.skip_rounds_dropdown['values'] = list(range(1, self.get_char_list_length()))  # Dropdown values from 1 to 10
        self.skip_rounds_dropdown.pack(side=tk.LEFT)
        
        self.rounds_label = tk.Label(self.skip_rounds_frame, text="rounds")
        self.rounds_label.pack(side=tk.LEFT)
        
        self.skip_button = tk.Button(self.skip_rounds_frame, text="Skip", command=self.skip_rounds)
        self.skip_button.pack(side=tk.LEFT)
        
        # Button to start initialization and show popup
        self.start_init_button = tk.Button(self, text="StartInit", command=self.show_popup)
        self.start_init_button.pack(pady=10)
    
    
    def start_init(self, start_window):
        if self.map_path:
            print(f"Preprocessing map: {self.map_path}")
            self.map = Map(self.map_path)    

            # ToDo: Unbedingt wieder einkommentieren! Nur für leichteres Testen aus.      
            self.show_opencv_window()  
            self.show_map_window()

            self.initialize_game()
            self.show_popup()
            self.show_camera_popup()

            start_window.destroy()           
            self.deiconify()  # Show the main window
        else:
            messagebox.showwarning("No Map Selected", "Please select a map file before starting.")

    def initialize_game(self):        
        grid = GitterErkennung( cv2.imread(self.map_path),debug=False)
        if self.rotation_angle is not 0 and self.rotation_angle is not 180:            
            game_field_width,game_field_height = grid.return_dimensions
        else:
            game_field_height,game_field_width = grid.return_dimensions
        self.game_field = GameField(game_field_height,game_field_width,self.map)
        print(f"(Height,Width) : ({game_field_height,game_field_width})")
        self.position_detector = PositionDetection(game_field_width,game_field_height)


    def prepare_camera(self):
        print("Detecting screen region...")

        self.corners = []     

        if self.region is None:
            print("\nPlease select the top-left point of the camera image without any figure.")
            x1, y1 = self.get_click_position()
            print("\nSelect the bottom-right point of the camera image without any figure.")
            x2, y2 = self.get_click_position()
            left, top = min(x1, x2), min(y1, y2)
            width, height = abs(x2 - x1), abs(y2 - y1)
            self.region = {"left": left, "top": top, "width": width, "height": height}


    def get_click_position(self) -> Tuple[int, int]:
        print("Bitte klicke, um eine Position zu wählen...")
        pos = None
        while pos is None:
            if mouse.is_pressed(button='left'):
                pos = mouse.get_position()
                while mouse.is_pressed(button='left'):
                    pass
        return pos
        
        
# ------------------------------------------------------------------------------ GameLogic ------------------------------------------------------------------------------------- #
    
    def start(self):
        if not self.map_path:
            messagebox.showwarning("No Map Selected", "Please select a map file before starting.")
            return
        self.running = True
        print("Game started")
    
    def end(self):
        self.running = False
        print("Ended")
        self.quit()
    
    def next_round(self):
        if self.running:
            print("Next Round")
    
    def skip_rounds(self):
        rounds_to_skip = self.rounds_var.get()
        print(f"Skipped {rounds_to_skip} rounds")
    

    def detect_automatically(self):
        region = self.camera.clicked_points
        self.take_screenshot(screenshot_path)
        screenshot = cv2.imread(screenshot_path)
        self.camera.transform_image(screenshot)
        cv2.imshow("Screenshot", screenshot)
        cv2.waitKey(0)
        print(f"Stelle eine neue Figur aufs Spielfeld und bestätige mit ENTER.")
        input()
        self.take_screenshot(screenshot_path, region)
        screenshot_next = cv2.imread(screenshot_path)
        screenshot_next = self.camera.transform_image(screenshot_next)
        cv2.imshow("Next Screenshot", screenshot_next)
        cv2.waitKey(0)

        position = self.position_detector.detectPosition(screenshot_next, screenshot)

        cv2.imshow("Next Screenshot", screenshot_next)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        x_pos, y_pos = position

        print(f"(x,y) = {x_pos,y_pos}")

        # Fülle die erkannten Werte in die Textboxen ein
        self.x_pos_entry.delete(0, tk.END)
        self.x_pos_entry.insert(0, str(x_pos))
        self.y_pos_entry.delete(0, tk.END)
        self.y_pos_entry.insert(0, str(y_pos))
        self.size_entry.delete(0, tk.END)
        self.size_entry.insert(0, str(1))  # Assuming size is always 1




# ------------------------------------------------------------------------------ Helper ------------------------------------------------------------------------------------- #
   
    def update_map_size(self, event=None):
        scale_factor = self.slider.get()
        self.map.resize_map(scale_factor)
        self.update_map_image()
    
    def update_map_image(self):
        # Verwende das skalierte und rotierte Bild aus dem OpenCV-Fenster
        bgr_image = self.scaled_image
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(rgb_image)
        self.map_image = ImageTk.PhotoImage(image_pil)

        self.map_label.config(image=self.map_image)
        self.map_label.image = self.map_image  # Verhindert das Garbage Collection Problem

    def select_map_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.map_path = file_path
            print(f"Selected map file: {self.map_path}")

    def get_char_list_length(self):
        print("get_char_list_length")
        return 5  # Placeholder value
    

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.corners) < 4:
                self.corners.append((x, y))
                print(f"Corner {len(self.corners)}: ({x}, {y})")
            else:
                print("All 4 corners have already been selected.")


    def take_screenshot(self, save_path, region):
        with mss.mss() as sct:
            # Berechne die Begrenzungsbox aus den Eckpunkten
            left = min(region, key=lambda t: t[0])[0]
            top = min(region, key=lambda t: t[1])[1]
            right = max(region, key=lambda t: t[0])[0]
            bottom = max(region, key=lambda t: t[1])[1]
            width = right - left
            height = bottom - top

            bounding_box = {
                "top": top,
                "left": left,
                "width": width,
                "height": height
            }

            screenshot = sct.grab(bounding_box)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)


# ------------------------------------------------------------------------------ GUI ------------------------------------------------------------------------------------- #

    def show_start_window(self):
        start_window = tk.Toplevel(self)
        start_window.title("Select Map")
        start_window.geometry("300x150")

        tk.Label(start_window, text="Select a map file to start the game:").pack(pady=10)
        select_button = tk.Button(start_window, text="Select Map", command=self.select_map_file)
        select_button.pack(pady=10)
        start_button = tk.Button(start_window, text="Continue", command=lambda: self.start_init(start_window))
        start_button.pack(pady=10)

    def show_map_window(self):
        if self.map_window is not None:
            self.map_window.destroy()
        self.map_window = tk.Toplevel(self)
        self.map_window.title("Map Display")
        self.map_window.geometry("800x600")

        self.map_label = tk.Label(self.map_window)
        self.map_label.pack()
        
        self.update_map_image()

    
    def show_opencv_window(self):
        def on_trackbar(val):
            update_image()

        def update_image():
            scale_factor = cv2.getTrackbarPos("Scale", "Adjust Map") / 100
            self.rotation_angle = cv2.getTrackbarPos("Rotate", "Adjust Map")
            self.rotation_angle = [0, 90, 180, 270][self.rotation_angle]  # Nur die erlaubten Winkel

            # Skaliere das Bild
            scaled_image = cv2.resize(self.original_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
            
            # Rotationszentrum
            h, w = scaled_image.shape[:2]
            center = (w // 2, h // 2)

            # Rotationsmatrix
            rotation_matrix = cv2.getRotationMatrix2D(center, self.rotation_angle, 1.0)

            # Berechne die neue Bounding Box Größe
            abs_cos = abs(rotation_matrix[0, 0])
            abs_sin = abs(rotation_matrix[0, 1])
            bound_w = int(h * abs_sin + w * abs_cos)
            bound_h = int(h * abs_cos + w * abs_sin)

            # Anpassung der Rotationsmatrix für das neue Bounding Box
            rotation_matrix[0, 2] += bound_w / 2 - center[0]
            rotation_matrix[1, 2] += bound_h / 2 - center[1]
            rotated_image = cv2.warpAffine(scaled_image, rotation_matrix, (bound_w, bound_h))

            cv2.imshow("Adjust Map", rotated_image)
            self.scaled_image = rotated_image

        # Lesen und Anzeigen des Originalbilds
        self.original_image = cv2.imread(self.map_path)
        self.scaled_image = self.original_image.copy()
        
        cv2.namedWindow("Adjust Map")
        cv2.imshow("Adjust Map", self.original_image)

        cv2.createTrackbar("Scale", "Adjust Map", 100, 200, on_trackbar)
        cv2.createTrackbar("Rotate", "Adjust Map", 0, 3, on_trackbar)  # Slider auf Werte 0 bis 3 beschränken

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    
    def show_popup(self):
        popup = tk.Toplevel(self)
        popup.title("StartInit Popup")
        popup.geometry("300x600")

        # Box for new figure
        figure_frame = tk.LabelFrame(popup, text="New Figure")
        figure_frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(figure_frame, text="x_pos:").grid(row=0, column=0, sticky="e")
        self.x_pos_entry = tk.Entry(figure_frame)
        self.x_pos_entry.grid(row=0, column=1)
        self.x_pos_entry.insert(0, "0")
        self.x_pos_entry.bind("<FocusOut>", self.validate_x_pos)

        tk.Label(figure_frame, text="y_pos:").grid(row=1, column=0, sticky="e")
        self.y_pos_entry = tk.Entry(figure_frame)
        self.y_pos_entry.grid(row=1, column=1)
        self.y_pos_entry.insert(0, "0")
        self.y_pos_entry.bind("<FocusOut>", self.validate_y_pos)

        tk.Label(figure_frame, text="Größe:").grid(row=2, column=0, sticky="e")
        self.size_entry = tk.Entry(figure_frame)
        self.size_entry.grid(row=2, column=1)

        tk.Label(figure_frame, text="Type:").grid(row=3, column=0, sticky="e")
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(figure_frame, textvariable=self.type_var)
        self.type_dropdown['values'] = ["NPC", "Friend", "Enemy"]
        self.type_dropdown.grid(row=3, column=1)

        tk.Label(figure_frame, text="Initiative:").grid(row=4, column=0, sticky="e")
        self.initiative_entry = tk.Entry(figure_frame)
        self.initiative_entry.grid(row=4, column=1)

        add_figure_button = tk.Button(figure_frame, text="Add", command=self.add_new_figure)
        add_figure_button.grid(row=5, columnspan=2, pady=10)

        # Button for detecting position automatically
        detect_button = tk.Button(figure_frame, text="Detect Automatically", command=self.detect_automatically)
        detect_button.grid(row=6, columnspan=2, pady=10)

        # Box for adding event
        event_frame = tk.LabelFrame(popup, text="Add Event")
        event_frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(event_frame, text="x_pos:").grid(row=0, column=0, sticky="e")
        self.event_x_pos_entry = tk.Entry(event_frame)
        self.event_x_pos_entry.grid(row=0, column=1)
        self.event_x_pos_entry.insert(0, "0")
        self.event_x_pos_entry.bind("<FocusOut>", self.validate_event_x_pos)

        tk.Label(event_frame, text="y_pos:").grid(row=1, column=0, sticky="e")
        self.event_y_pos_entry = tk.Entry(event_frame)
        self.event_y_pos_entry.grid(row=1, column=1)
        self.event_y_pos_entry.insert(0, "0")
        self.event_y_pos_entry.bind("<FocusOut>", self.validate_event_y_pos)

        tk.Label(event_frame, text="Größe:").grid(row=2, column=0, sticky="e")
        self.event_size_entry = tk.Entry(event_frame)
        self.event_size_entry.grid(row=2, column=1)

        tk.Label(event_frame, text="Type:").grid(row=3, column=0, sticky="e")
        self.event_type_var = tk.StringVar()
        self.event_type_dropdown = ttk.Combobox(event_frame, textvariable=self.event_type_var)
        self.event_type_dropdown['values'] = ["Trap", "Fire"]
        self.event_type_dropdown.grid(row=3, column=1)

        add_event_button = tk.Button(event_frame, text="Add", command=self.add_event)
        add_event_button.grid(row=4, columnspan=2, pady=10)

        # Close button for popup
        close_button = tk.Button(popup, text="OK", command=popup.destroy)
        close_button.pack(pady=10)


    def show_camera_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Camera Setup")
        popup.geometry("300x150")

        tk.Label(popup, text="Please select the region for the camera!").pack(pady=10)
        select_button = tk.Button(popup, text="Select", command=self.prepare_camera)
        select_button.pack(pady=10)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

   
        



    def validate_x_pos(self, event):
        value = int(self.x_pos_entry.get())
        if value < self.X_POS_MIN or value > self.X_POS_MAX:
            self.x_pos_entry.delete(0, tk.END)
            self.x_pos_entry.insert(0, "0")
            print(f"x_pos must be between {self.X_POS_MIN} and {self.X_POS_MAX}")

    def validate_y_pos(self, event):
        value = int(self.y_pos_entry.get())
        if value < self.Y_POS_MIN or value > self.Y_POS_MAX:
            self.y_pos_entry.delete(0, tk.END)
            self.y_pos_entry.insert(0, "0")
            print(f"y_pos must be between {self.Y_POS_MIN} and {self.Y_POS_MAX}")

    def validate_event_x_pos(self, event):
        value = int(self.event_x_pos_entry.get())
        if value < self.X_POS_MIN or value > self.X_POS_MAX:
            self.event_x_pos_entry.delete(0, tk.END)
            self.event_x_pos_entry.insert(0, "0")
            print(f"Event x_pos must be between {self.X_POS_MIN} and {self.X_POS_MAX}")

    def validate_event_y_pos(self, event):
        value = int(self.event_y_pos_entry.get())
        if value < self.Y_POS_MIN or value > self.Y_POS_MAX:
            self.event_y_pos_entry.delete(0, tk.END)
            self.event_y_pos_entry.insert(0, "0")
            print(f"Event y_pos must be between {self.Y_POS_MIN} and {self.Y_POS_MAX}")

    def slider_released(self, event):
        value = self.slider.get()
        print(f"Slider value: {value}")

    def add_new_figure(self):
        x_pos = int(self.x_pos_entry.get())
        y_pos = int(self.y_pos_entry.get())
        size = int(self.size_entry.get())
        figure_type = self.type_var.get()
        initiative = int(self.initiative_entry.get())
        print(f"Added New Figure: x_pos={x_pos}, y_pos={y_pos}, Größe={size}, Type={figure_type}, Initiative={initiative}")

    def add_event(self):
        x_pos = int(self.event_x_pos_entry.get())
        y_pos = int(self.event_y_pos_entry.get())
        size = int(self.event_size_entry.get())
        event_type = self.event_type_var.get()
        print(f"Added Event: x_pos={x_pos}, y_pos={y_pos}, Größe={size}, Type={event_type}")

    def game_loop(self):
        if self.running:
            # Placeholder for game logic
            print("Game loop iteration")


#following code is the call for the GUI in game.py
if __name__ == "__main__":
    app = Application(30,40)
    app.mainloop()
