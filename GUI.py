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
#Create an instance of Tkinter Frame
win = Tk()

#Set the geometry of Tkinter Frame
win.geometry("700x350")

#Define a function for opening the Dialog box
def open_prompt():
   messagebox.showinfo("Message", "Click Okay to Proceed")

#Create a Label widget
Label(win, text= "Click to Open the MessageBox").pack(pady=15)

#Create a Button for opening a dialog Box
ttk.Button(win, text= "Open", command= open_prompt).pack()

win.mainloop()