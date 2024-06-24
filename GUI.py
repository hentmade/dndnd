import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
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
from pynput import mouse
import time


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
        self.start_window = None
        self.map_window = None  # Variable to store the map window
        self.map_image = None  # Variable to store the map image
        self.map_label = None  # Label to display the map image
        self.game_field = None
        self.position_detector = None
        self.rotation_angle = 0
        self.camera = None
        self.screenshot_path = screenshot_path
        self.region = None
        self.figures_tree = None
        self.selected_figure = 0
        self.round = 0
        self.withdraw()  # Hide the main window initially
        self.show_start_window()
     

        
   
    
    
    def start_init(self, start_window):
        if self.map_path:

            self.start_window.destroy()

            print(f"Preprocessing map: {self.map_path}")
            self.map = Map(self.map_path)    

            self.show_opencv_window()       

            self.initialize_game()

            self.show_camera_popup()
            self.wait_window(self.camera_popup)

            self.show_map_window()
            self.show_popup()
         
            self.deiconify()  # Show the main window
        else:
            messagebox.showwarning("No Map Selected", "Please select a map file before starting.")

    def initialize_game(self):        
        grid = GitterErkennung( cv2.imread(self.map_path),debug=False)
        if self.rotation_angle != 0 and self.rotation_angle != 180:            
            game_field_width,game_field_height = grid.return_dimensions
        else:
            game_field_height,game_field_width = grid.return_dimensions
        self.game_field = GameField(game_field_height,game_field_width,self.map)
        print(f"(Height,Width) : ({game_field_height,game_field_width})")
        self.position_detector = PositionDetection(game_field_width,game_field_height)


    def prepare_camera(self):
        print("Detecting screen region...") 

        if self.region is None:
            points = []
            print("\nPlease select the four corners of the region in the following order:")
            print("1. Top-Left")
            print("2. Top-Right")
            print("3. Bottom-Right")
            print("4. Bottom-Left")

            listener = mouse.Listener(on_click=lambda x, y, button, pressed: self.on_click(x, y, points, pressed))
            listener.start()

            while len(points) < 4:
                time.sleep(0.1)

            listener.stop()
            self.points = points
            print(f"Points selected: {points}")

            # Define the region based on the selected points
            left, top = min(p[0] for p in points), min(p[1] for p in points)
            right, bottom = max(p[0] for p in points), max(p[1] for p in points)
            self.region = {"left": left, "top": top, "width": right - left, "height": bottom - top}
            print(f"Region defined: {self.region}")

    


# ------------------------------------------------------------------------------ GameLogic ------------------------------------------------------------------------------------- #
    
    def start(self):
        if not self.map_path:
            messagebox.showwarning("No Map Selected", "Please select a map file before starting.")
            return
        self.running = True
        print("Game started")
        self.selected_figure = self.get_current_figure() 
        self.screenshot_prev = self.detect_one_position()      
        
        start_position = self.selected_figure.position
        

        print(f"Startposition {self.selected_figure.name}: {start_position} ")

        self.map.display_map("Map")
        cv2.waitKey(0)
        

    
    def get_current_figure(self):
        all_figures_count = len(self.game_field.figures)
        selected_figure = self.game_field.figures[self.round % all_figures_count]
        return selected_figure


    def end(self):
        self.running = False
        print("Ended")
        self.quit()
    
    def next_round(self):
        if self.running:
            print(f"Next Round {self.round}")

        self.screenshot_next = self.detect_one_position()
        end_position = self.position_detector.detectPosition(self.screenshot_next, self.screenshot_prev)
        print(f"Endposition {self.selected_figure.name}: {end_position} ")

        start_position = self.selected_figure.position

        self.game_field.move_figure(self.selected_figure,start_position,end_position)
        
        self.map.remove_overlay("Assets\\player_radius.png",start_position,self.selected_figure.size*5) 

        self.round +=1

        self.selected_figure = self.get_current_figure() 

        self.screenshot_prev = self.detect_one_position()      
        
        start_position = self.selected_figure.position

        print(f"Startposition {self.selected_figure.name}: {start_position} ")

        self.map.display_map("Map")
        cv2.waitKey(0)

       
    
    def skip_rounds(self):
        rounds_to_skip = self.rounds_var.get()
        print(f"Skipped {rounds_to_skip} rounds")
    
    def detect_one_position(self):
        self.take_screenshot(screenshot_path)
        screenshot = cv2.imread(screenshot_path)
        return screenshot
    

    def detect_position(self):
        self.take_screenshot(screenshot_path)
        screenshot = cv2.imread(screenshot_path)
        # cv2.imshow("Screenshot", screenshot)
        # cv2.waitKey(0)

        self.show_ok_popup()

        self.take_screenshot(screenshot_path)
        screenshot_next = cv2.imread(screenshot_path)
        # cv2.imshow("Next Screenshot", screenshot_next)
        # cv2.waitKey(0)

        position = self.position_detector.detectPosition(screenshot_next, screenshot)

        

        cv2.destroyAllWindows()

        
        return position


    def detect_automatically(self):
        position = self.detect_position()
        x_pos, y_pos = position

        print(f"(x,y) = {x_pos,y_pos}")

        # # Fülle die erkannten Werte in die Textboxen ein
        self.x_pos_entry.delete(0, tk.END)
        self.x_pos_entry.insert(0, str(x_pos))
        self.y_pos_entry.delete(0, tk.END)
        self.y_pos_entry.insert(0, str(y_pos))
        self.size_entry.delete(0, tk.END)
        self.size_entry.insert(0, str(1))  # Assuming size is always 1


    def add_new_figure(self):
        name = self.name_entry.get()
        figure_type_str = self.type_var.get()
        x_pos = self.x_pos_entry.get()
        y_pos = self.y_pos_entry.get()
        size = self.size_entry.get()
        initiative = self.initiative_entry.get()
        figure_type = None
        

        # Konvertiere die Felder in die entsprechenden Typen
        x_pos = int(x_pos)
        y_pos = int(y_pos)
        size = int(size)
        initiative = int(initiative)

        try:
            figure_type = Figure_Type[figure_type_str.upper()]
        except KeyError:
            messagebox.showerror("Ungültiger Typ", f"Der Typ '{figure_type_str}' ist ungültig.")
            return

        position = (x_pos, y_pos)

        # Überprüfen, ob alle Felder ausgefüllt sind
        if not name or not figure_type or not x_pos or not y_pos or not size or not initiative:
            messagebox.showwarning("Eingabefehler", "Bitte füllen Sie alle Felder aus, bevor Sie eine Spielfigur hinzufügen.")
            return
        print(f"Added New Figure: Name={name}, Type={figure_type}, Position={position}, Size={size}, Initiative={initiative}")
        
        # Füge die Figur zum Spielfeld hinzu
        self.game_field.add_figure(name, figure_type, position, size, initiative)

        # Aktualisiere die Figurenliste im Popup
        self.update_figures_tree()




    def add_event(self):
        x_pos = int(self.event_x_pos_entry.get())
        y_pos = int(self.event_y_pos_entry.get())
        size = int(self.event_size_entry.get())
        event_type_str = self.event_type_var.get()

        try:
            event_type = Event_Type[event_type_str.upper()]
        except KeyError:
            messagebox.showerror("Ungültiger Typ", f"Der Typ '{event_type_str}' ist ungültig.")
            return
        
        position = (x_pos, y_pos)


        if not x_pos or not y_pos or not size or not event_type:
            messagebox.showwarning("Eingabefehler", "Bitte füllen Sie alle Felder aus, bevor Sie ein Event hinzufügen.")
            return
        

        self.game_field.add_event(event_type,position,size)

        print(f"Added Event: x_pos={x_pos}, y_pos={y_pos}, Größe={size}, Type={event_type}")

        

    def game_loop(self):
        if self.running:
            # Placeholder for game logic
            print("Game loop iteration")

# ------------------------------------------------------------------------------ Helper ------------------------------------------------------------------------------------- #
   
    def on_click(self, x, y, points, pressed):
        if pressed:
            print(f"Point selected: ({x}, {y})")
            points.append((x, y))
        if len(points) >= 4:
            return False
        
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
        self.map_label.image = self.map_image  

    def select_map_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.map_path = file_path
            print(f"Selected map file: {self.map_path}")

    def get_char_list_length(self):
        print("get_char_list_length")
        return 5  # Placeholder value


    def take_screenshot(self, save_path):
        bbox = (self.region["left"], self.region["top"], 
                self.region["left"] + self.region["width"], 
                self.region["top"] + self.region["height"])
        screenshot = ImageGrab.grab(bbox)
        screenshot.save(save_path, "PNG")
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # cv2.imshow("Before Transformation",screenshot)
        # cv2.waitKey(0)

        # Transform the screenshot using the selected points
        transformed_image = self.transform_image(screenshot, self.points)
        cv2.imwrite(save_path, transformed_image)
        # cv2.imshow("After Transformation",transformed_image)
        # cv2.waitKey(0)


    def transform_image(self, image, points): 
        # Show image and get the clicked points for transformation
        if len(points) != 4:
            raise ValueError("Four points are required for the transformation.")

        # print(f"Original Points: {points}")
        # print(f"Image shape: {image.shape}")

        # Adjust points relative to the top-left corner of the region
        relative_points = [(p[0] - self.region["left"], p[1] - self.region["top"]) for p in points]

        #print(f"Relative Points: {relative_points}")

        original_pts = np.float32(relative_points)
        projected_pts = np.float32([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])

        #print(f"Projected Points: {projected_pts}")

        # Calculate transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(original_pts, projected_pts)
        #print(f"Transformation Matrix: {transformation_matrix}")

        # Transform picture with transformation matrix
        transformed_image = cv2.warpPerspective(image, transformation_matrix, (image.shape[1], image.shape[0]))

        # cv2.imshow("While Transformation", transformed_image)
        # cv2.waitKey(0)

        return transformed_image
    
    def update_figures_tree(self):
        if not hasattr(self, 'figures_tree'):
            return

        for i in self.figures_tree.get_children():
            self.figures_tree.delete(i)
        
        for figure in self.game_field.figures:
            self.figures_tree.insert("", "end", values=(figure.name, figure.type.value, figure.position,figure.initiative, figure.size))

        



# ------------------------------------------------------------------------------ GUI ------------------------------------------------------------------------------------- #

    def show_start_window(self):
        self.start_window = tk.Toplevel(self)
        self.start_window.title("Select Map")
        self.start_window.geometry("300x150")

        tk.Label(self.start_window, text="Select a map file to start the game:").pack(pady=10)
        select_button = tk.Button(self.start_window, text="Select Map", command=self.select_map_file)
        select_button.pack(pady=10)
        start_button = tk.Button(self.start_window, text="Continue", command=lambda: self.start_init(self.start_window))
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


    def create_widgets(self):

        # Figure list
        self.show_figures_button = tk.Button(self, text="Show Figures", command=self.show_figures_popup)
        self.show_figures_button.pack(pady=10)

        # Button to start initialization and show popup
        self.start_init_button = tk.Button(self, text="StartInit", command=self.show_popup)
        self.start_init_button.pack(pady=10)

        # Button to start
        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.pack(pady=10)

     
        
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
        
        # Button to end
        self.end_button = tk.Button(self, text="End", command=self.end)
        self.end_button.pack(pady=10)

        

    def show_figures_popup(self):
        if hasattr(self, 'figures_popup') and self.figures_popup.winfo_exists():
            self.figures_popup.deiconify()  # Bringe das Popup in den Vordergrund, falls es bereits existiert
            return

        self.figures_popup = tk.Toplevel(self)
        self.figures_popup.title("Figures List")
        self.figures_popup.geometry("400x300")

        self.figures_tree = ttk.Treeview(self.figures_popup, columns=("Name", "Type", "Position", "Size", "Initiative"), show="headings")
        self.figures_tree.heading("Name", text="Name")
        self.figures_tree.heading("Type", text="Type")
        self.figures_tree.heading("Position", text="Position")
        self.figures_tree.heading("Size", text="Size")
        self.figures_tree.heading("Initiative", text="Initiative")

        self.figures_tree.pack(fill=tk.BOTH, expand=True)
        self.update_figures_tree()

    def show_popup(self):
        popup = tk.Toplevel(self)
        popup.title("StartInit Popup")
        popup.geometry("300x600")

        # Box for new figure
        figure_frame = tk.LabelFrame(popup, text="New Figure")
        figure_frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(figure_frame, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(figure_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(figure_frame, text="x_pos:").grid(row=1, column=0, sticky="e")
        self.x_pos_entry = tk.Entry(figure_frame)
        self.x_pos_entry.grid(row=1, column=1)
        self.x_pos_entry.insert(0, "0")
        self.x_pos_entry.bind("<FocusOut>", self.validate_x_pos)

        tk.Label(figure_frame, text="y_pos:").grid(row=2, column=0, sticky="e")
        self.y_pos_entry = tk.Entry(figure_frame)
        self.y_pos_entry.grid(row=2, column=1)
        self.y_pos_entry.insert(0, "0")
        self.y_pos_entry.bind("<FocusOut>", self.validate_y_pos)

        tk.Label(figure_frame, text="Größe:").grid(row=3, column=0, sticky="e")
        self.size_entry = tk.Entry(figure_frame)
        self.size_entry.grid(row=3, column=1)

        tk.Label(figure_frame, text="Type:").grid(row=4, column=0, sticky="e")
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(figure_frame, textvariable=self.type_var)
        self.type_dropdown['values'] = ["Player", "Enemy", "Ally"]
        self.type_dropdown.grid(row=4, column=1)

        tk.Label(figure_frame, text="Initiative:").grid(row=5, column=0, sticky="e")
        self.initiative_entry = tk.Entry(figure_frame)
        self.initiative_entry.grid(row=5, column=1)

        add_figure_button = tk.Button(figure_frame, text="Add", command=self.add_new_figure)
        add_figure_button.grid(row=6, columnspan=2, pady=10)

        # Button for detecting position automatically
        detect_button = tk.Button(figure_frame, text="Detect Automatically", command=self.detect_automatically)
        detect_button.grid(row=7, columnspan=2, pady=10)

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
        self.camera_popup = tk.Toplevel(self)
        self.camera_popup.title("Camera Setup")
        self.camera_popup.geometry("300x150")

        tk.Label(self.camera_popup, text="Please select the region for the camera!").pack(pady=10)
        select_button = tk.Button(self.camera_popup, text="Select", command=self.prepare_camera)
        select_button.pack(pady=10)

        close_button = tk.Button(self.camera_popup, text="Close", command=self.camera_popup.destroy)
        close_button.pack(pady=10)


    def show_ok_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Bestätigung erforderlich")
        popup.geometry("300x100")
        
        label = tk.Label(popup, text="Stelle eine neue Figur aufs Spielfeld und bestätige mit OK.")
        label.pack(pady=10)

        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)

        # Warten, bis das Popup-Fenster geschlossen wird
        self.wait_window(popup)


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




#following code is the call for the GUI in game.py
if __name__ == "__main__":
    app = Application(30,40)
    app.mainloop()
