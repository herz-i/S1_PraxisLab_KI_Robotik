#######################################################################################
### Trage hier den Port aus myBlockly ein.                                          ###
#######################################################################################

port = '/dev/tty.usbserial-588D0017891'

#######################################################################################
### Trage hier deine abgelesenen Punkte ein.                                        ###
#######################################################################################

punkt_A = [20,20,20,20,20,20]       # Wichtig! Das Format muss gleich bleiben, ersetze nur die 0 mit deinen Winkeln!

punkt_B = [10,10,10,10,10,10]       # [J1, J2, J3, J4, J5, J6]

#######################################################################################
### Versuche hier die Geschwindigkeit und die Anzahl der Wiederholungen zu ändern.  ###
#######################################################################################

# Trage hier einen Geschwindigkeitswert zwischen 0 und 100 ein. 
geschwindigkeit = 20        # Tipp! Starte zunächst langsamer und erhöhe schrittweise die Geschwindigkeit!

# Wie oft sollen die zwei Punkte angefahren werden? (Max. 10)
anzahl_wdh = 3

#######################################################################################
### Ändere ab hier nichts mehr! Ansonsten funktioniert dein Programm danach nicht!  ###
#######################################################################################

import time
from src.robot_control import Cobot

robot = Cobot(port=port)
robot.power_on()
robot.home_position()
print("Roboter initialisiert. Starte Programm in 5 Sekunden.")
time.sleep(5)

for i in range(anzahl_wdh):
    print("Führe Wiederholung ",i+1," von insgesamt ",anzahl_wdh," Wiederholungen aus.")
    robot.send_angles(punkt_A, geschwindigkeit)
    time.sleep(2)
    robot.send_angles(punkt_B, geschwindigkeit)
    time.sleep(2)