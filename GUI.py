import tkinter

import tkinter as tk

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
""" 
Required IOs:

Button next_round (read Position)
Button skip X rounds
Button add_new_figures
Button start
Button end

Dialog Box Init
    Dialog Box new_figure
        textbox x_pos
        textbox y_pos
        größe Optional
        enemy friend npc optional
        initiative

    Dialog Box add event
        pos
        size
        type (dropdown)

Additional
    diplay reihenfolge
    DM text Log
    imageDisplay show_populated_map
 """

import tkinter as tk
from tkinter import ttk

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
        
        self.create_widgets()
        
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
    
    def get_char_list_length(self):
        print("get_char_list_length")
        return 5#placeholder value
    
    def start(self):
        print("Started")
    
    def end(self):
        print("Ended")
        self.quit()
    
    def next_round(self):
        print("Next Round")
    
    def skip_rounds(self):
        rounds_to_skip = self.rounds_var.get()
        print(f"Skipped {rounds_to_skip} rounds")
    
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

        # Box for slider
        slider_frame = tk.LabelFrame(popup, text="Slider")
        slider_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.slider = tk.Scale(slider_frame, from_=0, to=5, resolution=0.01, orient="horizontal")
        self.slider.pack(padx=10, pady=10)
        self.slider.bind("<ButtonRelease-1>", self.slider_released)

        # Close button for popup
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


#following code is the call for the GUI in game.py
if __name__ == "__main__":
    app = Application(30,40)
    app.mainloop()

