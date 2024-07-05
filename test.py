import tkinter as tk

def approach_3():
    def close_window():
        map_window.destroy()
    def max_window():
        #doshit
        map_window.state('zoomed')
        print("F")
    def min_window():
        map_window.state('normal')
    # Create the main window
    map_window = tk.Tk()

    # Set the window size
    map_window.geometry("400x300")

    # Remove the default title bar
    map_window.overrideredirect(True)

    # Create a custom title bar
    title_bar = tk.Frame(map_window, bg='black', relief='raised', bd=2)
    title_bar.pack(fill=tk.X)

    # Add a title label to the custom title bar
    title_label = tk.Label(title_bar, text="Custom Title Bar - Approach 3", bg='black', fg='white')
    title_label.pack(side=tk.LEFT, padx=10)

    # Add a close button to the custom title bar
    close_button = tk.Button(title_bar, text='X', command=close_window, bg='black', fg='white', relief='flat')
    close_button.pack(side=tk.RIGHT, padx=5)

    # Add a maximize button to the custom title bar
    maximize_button = tk.Button(title_bar, text="[]", command=max_window,bg='black', fg='white', relief='flat')
    maximize_button.pack(side=tk.RIGHT, padx=5)

    # Add a maximize button to the custom title bar
    minimize_button = tk.Button(title_bar, text="_", command=min_window,bg='black', fg='white', relief='flat')
    minimize_button.pack(side=tk.RIGHT, padx=5)

    # Add content to the main window
    content = tk.Frame(map_window, bg='lightblue')
    content.pack(fill=tk.BOTH, expand=True)

    # Function to move the window
    def move_window(event):
        map_window.geometry(f'+{event.x_root}+{event.y_root}')

    # Bind the title bar to the move window function
    title_bar.bind('<B1-Motion>', move_window)

    # Run the application
    map_window.mainloop()

approach_3()
