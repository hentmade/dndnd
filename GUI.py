import tkinter

import tkinter as tk

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
""" 
Required IOs:

Button next_round
Button add_new_figures
Button start
Button end

Dialog Box new_figure
    textbox x_pos
    textbox y_pos

Additional
    imageDisplay show_populated_map


Views

Initialisierung: Wir brauchen ein Fenster wo die Initialisierung stattfindet. Darunter fällt alles was bisher vor der GameLoop passiert. 

Hinzufügen der Spielerfiguren
Hinzufügen der Gegnerfiguren 
--> optional mit Beachtung der Reihenfolge, sprich die Figuren sind in der Reihenfolge dran die man ihnen zuschreibt (nennt sich in DND Initiative, die wird am Anfang ausgewürfelt mit einem 20-seitigen Würfel, wenn man die gewürfelte Zahl irgendwo eintragen kann und er daraufhin beginnend mit dem höchsten Würfelergebnis die Reihenfolge bildet wäre das ziemlich nice)
Hinzufügen der Events (Trap, Fire bisher nur implementiert) mit Positionsangabe (x,y)
Hinzufügen der Items mit Positionsangabe.
Button "Weiter" um eine View weiterzukommen und die Initialisierung abzuschließen
GameLoop: Hier sollte der Dungeon Master die Konsolenausgabe einfach sehen können bzw. einfach ein Log wo das Auslösen von Events hinterlegt ist und man die Spielfiguren weiterschalten kann / Runde beenden.

Ausgabe des Spielgeschehens (Konsolenausgabe)
Button zum Durchschalten der Figuren
Optional: Anzeige der Map für DM
Optional: Anzeige der Figurenreihenfolge
Optional: Hinzufügen von Gegnereinheiten


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