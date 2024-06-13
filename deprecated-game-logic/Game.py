# 1. Beamerbild ausgeben
# 2. Kamerabild einlesen
# 3. Kamerabild gerade ziehen
# 4. Spielfeld initialisieren
# 5. Startposition der Figuren erkennen
# 6. Figuren erstellen und auf das virtuelle Spielfeld setzen 
#   --> Rundenbasiert jede Figur einzeln einlesen?
#   --> Wie unterscheiden zwischen Gegner und Verbündet?
# 7. Gegner / Events etc. randomisiert setzen oder hardcoden?
# 8. Rundenbasiert:
#   - Zug der Spielfigur
#   - Auswertung der Events
#   - Veränderung der Spielmap
#   - Speicherung des neuen Zustandes der Spielmap

from GameField import *
from Figure import *
from Event import *


# Initialisierung der Spielfiguren
# ToDo: 
# - Eindeutigere Tags / IDs? 
# - Anhand der Tags
#

# ToDo: Liste anlegen und dort alle Figuren reinspeichern
figure_player1 = Figure("Player_1",Figure_Tag.PLAYER,(1,1))
figure_ally1 = Figure("Ally_1",Figure_Tag.ALLY, (0, 0))
figure_enemy1 = Figure("Enemy_1", Figure_Tag.ENEMY,(5, 5))
figure_treasure1 = Figure("Treasure_1",Figure_Tag.OBJECT,(10,10))
figure_player2 = Figure("Player_2",Figure_Tag.PLAYER,(6,7))
figure_ally2 = Figure("Ally_2",Figure_Tag.ALLY, (8, 9))
figure_enemy2 = Figure("Enemy_2", Figure_Tag.ENEMY,(6, 6))
figure_treasure2 = Figure("Treasure_2",Figure_Tag.OBJECT,(10,10))

# Initialisierung der Events
event_trap = Event("Trap")
event_fireball = Event("Fire")

# Initialisierung des Spielfelds
# ToDo: Figuren Liste foreach durchiterieren und aufs Spielfeld adden
game_field = GameField(20, 20)
game_field.add_figure(figure_player1)
game_field.add_figure(figure_ally1)
game_field.add_figure(figure_enemy1)
game_field.add_figure(figure_treasure1)
game_field.add_figure(figure_player2)
game_field.add_figure(figure_ally2)
game_field.add_figure(figure_enemy2)
game_field.add_figure(figure_treasure2)
# ToDo: Events müssen auch schon getriggert werden, wenn eine Figur initial auf das Event-Feld gestellt wird
game_field.add_event((3, 3), event_trap)
game_field.add_event((6, 6), event_fireball)

print(f"Player 1 ID: {figure_player1.id} / Position: {figure_player1.position}")
print(f"Ally 1 ID: {figure_ally1.id} / Position: {figure_ally1.position}")
print(f"Enemy 1 ID: {figure_enemy1.id} / Position: {figure_enemy1.position}")
print(f"Treasure 1 ID: {figure_treasure1.id} / Position: {figure_treasure1.position}")
print(f"Player 2 ID: {figure_player2.id} / Position: {figure_player2.position}")
print(f"Ally 2 ID: {figure_ally2.id} / Position: {figure_ally2.position}")
print(f"Enemy 2 ID: {figure_enemy2.id} / Position: {figure_enemy2.position}")
print(f"Treasure 2 ID: {figure_treasure2.id} / Position: {figure_treasure2.position}")


# Spielrunden
# ToDo: 
#   - Startposition der Figur deren Runde gerade ist erkennen
#   - Um die Position der Figur Radius anzeigen
#   - Figur bewegen
#   - Endposition der Figur erkennen
#   - move_figure Methode aufrufen
#   - Eventuelle Events auslösen 
#   - Neue Spielfeldeigenschaften setzen: z.B. "überschwemmt", "brennend"
#   - Aufgrund der Eigenschaften das Spielfeld neu visualieren
game_field.move_figure(figure_player1.position, (0, 1))
game_field.move_figure(figure_enemy1.position, (3, 3))

print(f"\n\nPlayer 1 ID: {figure_player1.id} / Position: {figure_player1.position}")
print(f"Enemy 1 ID: {figure_enemy1.id} / Position: {figure_enemy1.position}")

# Visualisierungseigenschaften des Spielfelds
game_field.add_property((1, 1), Cell_Tag.BURNT)
game_field.add_property((3, 2), Cell_Tag.FLOODED)
game_field.add_property((2, 3), Cell_Tag.IMPASSABLE)
game_field.visualize()


