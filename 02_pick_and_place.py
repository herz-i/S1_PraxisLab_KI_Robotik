#######################################################################################
### Trage hier den Port aus myBlockly ein.                                          ###
#######################################################################################

port = '/dev/tty.usbserial-588D0017891'

#######################################################################################
### Trage hier deine abgelesenen Punkte ein.                                        ###
#######################################################################################

# Wichtig! Das Format muss gleich bleiben, ersetze nur die 0 mit deinen Winkeln!

punkt_aufheben = [-37.44, -84.81, 1.23, -5.27, -0.79, -80.33]           # Punkt 1

vorposition_aufheben = [-37.0, -56.77, 1.23, -32.08, -2.02, -75.58]     # Punkt 2

punkt_ablegen = [9.14, -77.43, 2.72, -18.28, -2.54, -31.99]             # Punkt 3

#######################################################################################
### Versuche hier die Geschwindigkeit und die Anzahl der Wiederholungen zu ändern.  ###
#######################################################################################

# Trage hier einen Geschwindigkeitswert zwischen 0 und 100 ein. 
geschwindigkeit = 20        # Tipp! Starte zunächst langsamer und erhöhe schrittweise die Geschwindigkeit!

# Wie oft sollen die drei Punkte angefahren werden? (Max. 10)
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
    robot.send_angles(vorposition_aufheben, geschwindigkeit)
    time.sleep(2)
    robot.send_angles(punkt_aufheben, geschwindigkeit)
    time.sleep(2)
    robot.control_gripper(1)
    time.sleep(2)
    robot.send_angles(vorposition_aufheben, geschwindigkeit)
    time.sleep(2)
    robot.send_angles(punkt_ablegen, geschwindigkeit)
    time.sleep(2)
    robot.control_gripper(0)
    time.sleep(2)
